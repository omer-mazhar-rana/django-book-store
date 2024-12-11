from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import timedelta

from .models import User, Book, Loan


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "isbn",
            "publication_year",
            "genre",
            "is_available",
        ]


class LoanSerializer(serializers.ModelSerializer):
    due_date = serializers.SerializerMethodField()
    fine = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ["id", "user", "book", "start_date", "return_date", "due_date", "fine"]

    def get_due_date(self, obj):
        return obj.start_date + timedelta(days=14)

    def get_fine(self, obj):
        if obj.return_date and obj.return_date > (obj.start_date + timedelta(days=14)):
            overdue_days = (
                obj.return_date - (obj.start_date + timedelta(days=14))
            ).days
            return overdue_days * 100
        return 0
