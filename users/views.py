
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST


@login_required
def dashboard(request):
    if not hasattr(request.user, 'profile'):
        return render(request, 'access_denied.html', status=403)

    role = request.user.profile.role

    if role == 'admin':
        return render(request, 'admin_dashboard.html')
    elif role == 'trainer':
        return render(request, 'trainer_dashboard.html')
    elif role == 'receptionist':
        return render(request, 'receptionist_dashboard.html')
    elif role == 'member':
        return render(request, 'member_dashboard.html')

    return render(request, 'access_denied.html', status=403)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


@login_required
@require_POST
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def manage_users(request):
    if not hasattr(request.user, 'profile'):
        return HttpResponseForbidden("Access Denied")

    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied")

    users = User.objects.select_related('profile').all()
    search = request.GET.get('search', '').strip()

    if search:
        users = users.filter(email__icontains=search)

    return render(request, 'manage_users.html', {
        'users': users,
        'search': search
    })


@login_required
@require_POST
def delete_user(request, user_id):
    if not hasattr(request.user, 'profile'):
        return HttpResponseForbidden("Access Denied")

    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("Access Denied")

    user = get_object_or_404(User, id=user_id)

    if user == request.user or user.is_superuser:
        return HttpResponseForbidden("Cannot delete this account")

    user.delete()

    return redirect('manage_users')
