
@echo off
echo ==============================
echo Starting GymGuard
echo ==============================

echo Applying migrations...
python manage.py migrate

if errorlevel 1 (
    echo Migration failed!
    pause
    exit /b 1
)

echo Seeding demo accounts...
python -c "import sqlite3; db=sqlite3.connect('db.sqlite3'); db.executescript(open('seed.sql').read()); db.close()"

if errorlevel 1 (
    echo Database seeding failed!
    pause
    exit /b 1
)

echo Starting server...
python manage.py runserver

pause
