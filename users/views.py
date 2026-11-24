
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Profile, AuditLog
from .audit import log_action
from memberships.models import Membership


def has_role(user, roles):
    return (
        hasattr(user, 'profile')
        and user.profile.active
        and user.profile.role in roles
    )


@login_required
def dashboard(request):
    if not has_role(request.user, ['admin', 'trainer', 'receptionist', 'member']):
        return render(request, 'access_denied.html', status=403)

    role = request.user.profile.role

    if role == 'admin':
        return render(request, 'admin_dashboard.html')

    elif role == 'trainer':
        memberships = Membership.objects.filter(
            trainer=request.user,
            active=True
        ).select_related('member')

        return render(request, 'trainer_dashboard.html', {
            'memberships': memberships
        })

    elif role == 'receptionist':
        return render(request, 'receptionist_dashboard.html')

    elif role == 'member':
        memberships = Membership.objects.filter(member=request.user)

        return render(request, 'member_dashboard.html', {
            'memberships': memberships
        })

    return render(request, 'access_denied.html', status=403)


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            if not hasattr(user, 'profile') or not user.profile.active:
                log_action(
                    request,
                    'LOGIN_BLOCKED',
                    f'Inactive or unconfigured account: {username}'
                )

                return render(request, 'login.html', {
                    'error': 'Your account is inactive or not configured.'
                })

            login(request, user)

            log_action(request, 'LOGIN_SUCCESS', 'User logged in')

            return redirect('dashboard')

        log_action(
            request,
            'LOGIN_FAILED',
            f'Failed login attempt for username: {username}'
        )

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


@login_required
@require_POST
def user_logout(request):
    log_action(request, 'LOGOUT', 'User logged out')
    logout(request)
    return redirect('login')


@login_required
def trainer_list(request):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    trainers = User.objects.filter(
        profile__role='trainer'
    ).select_related('profile')

    return render(request, 'trainer_list.html', {
        'trainers': trainers
    })


@login_required
def create_trainer(request):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '').strip()
        specialty = request.POST.get('specialty', '').strip()

        if not username or not email or not password:
            return render(request, 'create_trainer.html', {
                'error': 'Please fill in all required fields.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'create_trainer.html', {
                'error': 'Username already exists.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'create_trainer.html', {
                'error': 'Email already exists.'
            })

        if len(phone) > 20 or len(specialty) > 100:
            return render(request, 'create_trainer.html', {
                'error': 'Phone or specialty is too long.'
            })

        try:
            validate_password(password)
        except ValidationError as error:
            return render(request, 'create_trainer.html', {
                'error': ' '.join(error.messages)
            })

        trainer = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=trainer,
            role='trainer',
            phone=phone,
            specialty=specialty
        )

        log_action(
            request,
            'TRAINER_CREATED',
            f'Trainer account created: {username}'
        )

        messages.success(request, 'Trainer created successfully.')

        return redirect('trainer_list')

    return render(request, 'create_trainer.html')


@login_required
@require_POST
def toggle_trainer(request, trainer_id):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    trainer = get_object_or_404(
        User,
        id=trainer_id,
        profile__role='trainer'
    )

    trainer.profile.active = not trainer.profile.active
    trainer.profile.save()

    action = 'TRAINER_ACTIVATED' if trainer.profile.active else 'TRAINER_DEACTIVATED'

    log_action(
        request,
        action,
        f'Trainer: {trainer.username}'
    )

    return redirect('trainer_list')


@login_required
def member_list(request):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    members = User.objects.filter(
        profile__role='member'
    ).select_related('profile', 'membership')

    return render(request, 'member_list.html', {
        'members': members
    })


@login_required
def create_member(request):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '').strip()

        if not username or not email or not password:
            return render(request, 'create_member.html', {
                'error': 'Please fill in all required fields.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'create_member.html', {
                'error': 'Username already exists.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'create_member.html', {
                'error': 'Email already exists.'
            })

        if len(phone) > 20:
            return render(request, 'create_member.html', {
                'error': 'Phone number is too long.'
            })

        try:
            validate_password(password)
        except ValidationError as error:
            return render(request, 'create_member.html', {
                'error': ' '.join(error.messages)
            })

        member = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=member,
            role='member',
            phone=phone
        )

        log_action(
            request,
            'MEMBER_CREATED',
            f'Member account created: {username}'
        )

        messages.success(request, 'Member created successfully.')

        return redirect('member_list')

    return render(request, 'create_member.html')


@login_required
@require_POST
def toggle_member(request, member_id):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    member = get_object_or_404(
        User,
        id=member_id,
        profile__role='member'
    )

    member.profile.active = not member.profile.active
    member.profile.save()

    action = 'MEMBER_ACTIVATED' if member.profile.active else 'MEMBER_DEACTIVATED'

    log_action(
        request,
        action,
        f'Member: {member.username}'
    )

    return redirect('member_list')


@login_required
def audit_logs(request):
    if not has_role(request.user, ['admin']):
        return HttpResponseForbidden("Access Denied")

    logs = AuditLog.objects.select_related('user').all()

    return render(request, 'audit_logs.html', {
        'logs': logs
    })


@login_required
def assigned_members(request):
    if not has_role(request.user, ['trainer']):
        return HttpResponseForbidden("Access Denied")

    memberships = Membership.objects.filter(
        trainer=request.user
    ).select_related('member')

    return render(request, 'trainer_dashboard.html', {
        'memberships': memberships
    })
