# AcademIQ API Server

An API server for AcademIQ project.

## Setting Up the Project

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```console
git clone https://github.com/k0jumba/AcademIQ.git
```

### 2. Set Up a Virtual Environment

Create a virtual environment to isolate the project dependencies.

Run from `AcademIQ/ApiServer/`

```console
python -m venv ./academiq-env
env-name\Scripts\activate
```

### 3. Install Requirements

Install the project dependencies from the `requirements.txt` file.

Run from `AcademIQ/ApiServer/`

```console
pip install -r requirements.txt
```

### 4. Set Up the .env File

Create a `.env` file in the project root directory. You can use the provided `.env.example` file as a template.

Run from `AcademIQ/ApiServer/`

```console
copy .env.example .env
```

Edit the `.env` file to include your configuration settings.

### 5. Apply Migrations

Run the following command to apply database migrations.

Run from `AcademIQ/ApiServer/academiq/`

```console
python manage.py migrate
```

### 6. Load fixtures [Optional]

If you want to qucikly set up some testing data, run the following command to load the fixtures.

Run from `AcademIQ/ApiServer/academiq/`

```console
load_fixtures.cmd
```

***Accounts:***
| username  | password       |
| --------- | -------------- |
| admin     | academiq123    |
| educator1 | academiq123    |
| student1  | academiq123    |
| student2  | academiq123    |

### 7. Run the Development Server

Start the development server to run the project locally.

Run from `AcademIQ/ApiServer/academiq/`

```console
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your web browser to see the project in action.
