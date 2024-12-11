# Project Setup Instructions

## Prerequisites

Ensure that you have Python and pip installed. If not, download and install Python from [python.org](https://www.python.org/).

## 1. Clone the Repository

If you haven't cloned the repository yet, do so by running:

```bash
git clone <repository-url>
cd <repository-folder>
```

Create a virtual environment by running:

```bash
python -m venv venv

```

## 2. Set up a virtual environment

Activate the virtual environment through commands given below:

On Windows

```bash
venv\Scripts\activate

```

On Mac

```bash
source venv/bin/activate
```

## 3. Install dependencies

Install dependencies using command:

```bash
source pip install -r requirements.txt
```

## 4. Apply database migrations

Apply the database migration using command:

```bash
python manage.py migrate
```

## 5. Run the development server

Run the development server using command:

```bash
python manage.py runserver
```

## 6. Access API documentation

Access documentation of the APIs on url given below:

```bash
http://localhost:8000/swagger/
```

## In a nut-sehll:

1. **Clone the repository** and navigate to the project directory.
2. **Set up a virtual environment** and activate it.
3. **Install dependencies** using `pip install -r requirements.txt`.
4. **Apply database migrations** with `python manage.py migrate`.
5. **Run the development server** using `python manage.py runserver`.
6. **Access API documentation** at `http://localhost:8000/swagger`.
