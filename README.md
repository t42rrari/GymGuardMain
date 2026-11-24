GymGuard

GymGuard is a gym management system we're building for our CS2413 Information Security project at UNB.

The project mainly focuses on Role-Based Access Control (RBAC), where different users have different permissions based on their roles. We have four roles: Admin, Receptionist, Trainer and Member.

We're using Django (Python) for the backend, HTML for the frontend and SQLite for the database.

How to Run the Project

These steps are for Windows using VS Code and Command Prompt (CMD).

1. Clone the repository

git clone https://github.com/t42rrari/GymGuardMain.git
cd GymGuardMain

2. Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate.bat

3. Install the required packages

pip install -r requirements.txt

4. Set the Django secret key

for /f "delims=" %i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set "DJANGO_SECRET_KEY=%i"

5. Set up the database

python manage.py migrate

7. Run the server

python manage.py runserver

Open the website at:

http://127.0.0.1:8000/login/

Notes

You'll need to run migrations to create your local database.

You can create test users and assign roles through Django Admin.

You'll need to activate the virtual environment and set the Django secret key again whenever you open a new CMD terminal.
