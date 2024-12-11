from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import serializers
from datetime import timedelta, date


from .models import Book, Loan
from .serializer import (
    UserLoginSerializer,
    UserRegisterSerializer,
    BookSerializer,
    LoanSerializer,
)


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer


class UserLogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {"message": "User logged out successfully!"},
                    status=status.HTTP_205_RESET_CONTENT,
                )
            except Exception as e:
                return Response(
                    {"error": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST
        )


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Book.objects.all()
        genre = self.request.query_params.get("genre", None)
        author = self.request.query_params.get("author", None)

        if genre:
            queryset = queryset.filter(genre=genre)
        if author:
            queryset = queryset.filter(author=author)

        return queryset


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            return Loan.objects.filter(user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]

        if not book.is_available:
            raise serializers.ValidationError("Book is not available.")

        book.is_available = False
        book.save()

        start_date = date.today()
        due_date = start_date + timedelta(days=14)
        serializer.save(
            user=self.request.user, start_date=start_date, due_date=due_date
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.return_date:
            instance.book.is_available = True
            instance.book.save()

    def retrieve_overdue(self, request):
        overdue_loans = Loan.objects.filter(
            user=request.user,
            return_date__isnull=True,
            start_date__lt=date.today() - timedelta(days=14),
        )
        serializer = self.get_serializer(overdue_loans, many=True)
        return Response(serializer.data)
