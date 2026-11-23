# GymGuard

This is our CS2413 Information Security project. We're making a gym management website using Django with four user roles: Member, Trainer, Receptionist and Admin.

## How to Run

1. Clone the repo
git clone https://github.com/t42rrari/GymGuardMain.git
cd GymGuardMain
```
2. Set up the virtual environment (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Install Django and the other packages**

```powershell
pip install -r requirements.txt
```

**4. Set the secret key**

```powershell
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**5. Set up the database**

```powershell
python manage.py migrate
```

**6. Create an admin account**

```powershell
python manage.py createsuperuser
```

**7. Start the website**

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/login/

## How to Test

- Go to http://127.0.0.1:8000/admin/ and log in with your superuser account.
- Create some test users.
- Add a Profile for each user and choose their role.
- Log in using those accounts to test the different dashboards.

## What's Done

- Login and logout
- Four user roles
- Separate dashboards for each role
- Role-based access restrictions
- Members can view their own membership
- Receptionists and Admins can view all memberships
- Receptionists and Admins can create and update memberships
- User management through Django Admin
- SQLite database setup

## What's Left

- Class bookings
- Trainer management
- Audit logs
- Security testing
- Frontend improvements
- MySQL integration (if needed)

## Notes

- The database isn't uploaded, so everyone needs to create their own test accounts.
- Set the secret key again whenever you open a new terminal.
- The project is still being worked on.