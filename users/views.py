from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

        return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

@login_required
@require_POST
def user_logout(request):
    logout(request)
    return redirect('login')
