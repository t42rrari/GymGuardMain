# GymGuard
 
A gym management website we built for our CS 2413 Information Security final project (Fall 2026). It's a Django app with four kinds of users (Member, Trainer, Receptionist, Admin), and the whole point of it is to see what it takes to keep those roles locked into what they're actually allowed to do.
 
**Team:** Taskina H Prova, Pavitra Srivastava, Johnny Wu Tsang, S M Sakib Zubair
**Repo:** https://github.com/t42rrari/GymGuardMain
 
---
 
## Contents
 
1. [Introduction](#1-introduction)
2. [Methodology](#2-methodology)
3. [Evaluation and Results](#3-evaluation-and-results)
4. [Conclusion](#4-conclusion)
5. [Running it yourself](#running-it-yourself)
6. [References](#references)
---
 
## 1. Introduction
 
### The problem
 
A gym system holds a surprising amount of personal data: names, phone numbers, membership plans, which trainer is working with whom. If it's built carelessly, a member can open pages meant for staff, a receptionist can do things only an admin should, and when something goes wrong nobody can tell who did it.
 
That's what we looked at: **broken access control** (people reaching stuff outside their role) and **lack of accountability** (no record of who did what). Broken access control sits at the top of the OWASP Top 10 for a reason. It's the most common way real web apps end up leaking data.
 
### How people usually deal with it
 
- **Role-based access control (RBAC).** Every user gets a role, and every page or action checks that role on the server before doing anything. Django's built-in auth system and its permission decorators are a common starting point.
- **Server-side checks, not hidden buttons.** Hiding a link in the UI isn't security. The view itself has to refuse the request.
- **Audit logging.** Recording logins, failed logins and sensitive actions (with user, time and IP) so incidents can be investigated. The OWASP Logging Cheat Sheet covers what's worth logging.
- **Safe defaults for accounts and sessions.** Hashed passwords, password validators, CSRF tokens, and deactivating accounts rather than deleting them.
### What we did
 
We built GymGuard with RBAC enforced in every view, an audit log that records security-relevant events, CSRF protection on forms, and inactive accounts blocked at login. Then we tested it by trying to break it. [Edit this paragraph so it matches the exact before/after you're presenting.]
 
---
 
## 2. Methodology
 
### Environment
 
| Thing | What we used |
|---|---|
| Language / framework | Python 3.14, Django 6.1.3 |
| Database | SQLite (the default Django one) |
| OS | Windows 11 [edit if different] |
| Browser for testing | [Chrome / Firefox, version] |
| Other tools | [e.g. Burp Suite, curl, Postman, only if you actually used them] |
| Version control | Git + GitHub |
 
Dependencies are pinned in `requirements.txt` (Django, asgiref, sqlparse, tzdata). The secret key is read from the `DJANGO_SECRET_KEY` environment variable instead of being hard-coded in `settings.py`.
 
### The method and why we picked it
 
**Role-based access control, checked in the views.** We have a `Profile` model that attaches a role to each Django user, and a small `has_role()` helper that every view calls before it does anything. Wrong role gets an access-denied page. We chose this over something fancier because the app only has four roles, and RBAC is easy to reason about, easy to test, and is the standard answer to this problem.
 
**Audit logging.** An `AuditLog` table stores the user, action, details, IP address and timestamp. Logins (success, failure, blocked) and logouts are logged, and only Admins can read the logs. We chose to log failed logins as well as successful ones because that's where attacks usually show up first.
 
**Other protections:**
- CSRF protection on forms (Django middleware plus `@csrf_protect` on login)
- Logout only works via POST
- Django's password validators are switched on
- Accounts are deactivated with a toggle instead of deleted, and inactive accounts can't log in
### How we tested it
 
[Rewrite this to match what you really did. Delete anything you didn't do.]
 
1. **Role checks:** log in as each role and try to open every URL (`/trainers/`, `/members/`, `/memberships/`, `/audit-logs/`, etc.) to see who gets in and who gets the access-denied page.
2. **Direct URL access:** type restricted URLs in while logged out, and while logged in as the wrong role.
3. **ID tampering:** change the IDs in URLs like `/memberships/update/<id>/` to check that a user can't touch records they shouldn't.
4. **Login abuse:** wrong passwords, inactive accounts, and an account with no profile. Then check the audit log caught them.
5. **Automated tests:** `python manage.py test`
---
 
## 3. Evaluation and Results
 
### Before the fix
 
[Describe the vulnerable version. What could a normal user do that they shouldn't?]
 
![Before: describe what this screenshot shows](screenshots/before-1.png)
 
*What this shows:* [one or two sentences, e.g. "A Member account opening the full member list."]
 
### After the fix
 
[Describe the same test on the fixed version.]
 
![After: describe what this screenshot shows](screenshots/after-1.png)
 
*What this shows:* [e.g. "The same Member account now gets the access-denied page."]
 
### Audit log evidence
 
![Audit log](screenshots/audit-log.png)
 
*What this shows:* [e.g. "Failed login attempts and blocked inactive-account logins appearing with IP and timestamp."]
 
### Summary
 
| Test | Before | After |
|---|---|---|
| Member opens staff pages | [result] | [result] |
| Wrong-role direct URL access | [result] | [result] |
| Failed login recorded | [result] | [result] |
| Inactive account login | [result] | [result] |
 
### Source code
 
Everything is in this repo: https://github.com/t42rrari/GymGuardMain
 
---
 
## 4. Conclusion
 
### What we set out to do and what we found
 
We wanted to build a small multi-role web app and make its access control actually hold up. By enforcing roles on the server in every view and logging security events, [summarise your main findings here in 2 or 3 sentences].
 
### Who did what
 
| Person | What they did |
|---|---|
| [Name 1] | [e.g. Django setup, login, roles] |
| [Name 2] | [e.g. membership management] |
| [Name 3] | [e.g. audit logging] |
| [Name 4] | [e.g. security testing, report] |
 
[If someone didn't contribute, say so here plainly. The guideline requires it.]
 
### Challenges
 
- [e.g. Merge conflicts when everyone pushed at once]
- [e.g. Getting the role checks consistent across every view]
- [e.g. Keeping the database and secret key out of the repo]
### What's not done
 
- Class bookings
- MySQL (we stayed on SQLite)
- Rate limiting or account lockout after repeated failed logins
- A nicer frontend
---
 
## Running it yourself
 
You need Python 3.12 or newer. Commands below are for Windows PowerShell. On Mac/Linux, swap in `python3`, `source venv/bin/activate` and `export`.
 
**1. Clone the repo**
 
```powershell
git clone https://github.com/t42rrari/GymGuardMain.git
cd GymGuardMain
```
 
**2. Make a virtual environment and install the packages**
 
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
 
**3. Set the secret key.** The app won't start without it, and you have to redo this in every new terminal.
 
```powershell
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
 
**4. Set up the database**
 
```powershell
python manage.py migrate
```
 
**5. Create accounts.** Either make your own admin:
 
```powershell
python manage.py createsuperuser
```
 
or load the demo accounts from `seed.sql` (admin, trainer1, receptionist1, member1). Windows users can skip steps 4 and 5 by running `run.bat` after setting the secret key.
 
**6. Start the server**
 
```powershell
python manage.py runserver
```
 
Open http://127.0.0.1:8000/login/
 
> If you made your own accounts through `/admin/`, every user needs a **Profile** with a role. Without one, they can't log in.
 
### Running the tests
 
```powershell
python manage.py test
```
 
### Project layout
 
```
gymguard/       project settings and URLs
users/          login, roles, dashboards, trainer/member management, audit log
memberships/    membership create / view / update
seed.sql        demo accounts
run.bat         one-click setup for Windows
```
 
---
 
## References
 
- OWASP Foundation. *A01:2021 – Broken Access Control.* https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- OWASP Foundation. *Logging Cheat Sheet.* https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- Django Software Foundation. *Using the Django authentication system.* https://docs.djangoproject.com/en/stable/topics/auth/
- Django Software Foundation. *Cross Site Request Forgery protection.* https://docs.djangoproject.com/en/stable/ref/csrf/
- [Add any papers or articles you actually used: title, authors, URL.]
 
