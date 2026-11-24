from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.db import transaction
from users.models import Profile
from .models import Membership

@login_required
def view_membership(request):
    if not hasattr(request.user, 'profile'):
        return HttpResponseForbidden("Access Denied")

    role = request.user.profile.role

    if role == 'member':
        memberships = Membership.objects.filter(member=request.user)

    elif role == 'receptionist' or role == 'admin':
        memberships = Membership.objects.all()

    else:
        return HttpResponseForbidden("Access Denied")

    return render(request, 'membership_list.html', {
        'memberships': memberships
    })



@login_required
def update_membership(request, membership_id):
    if not hasattr(request.user, 'profile'):
        return HttpResponseForbidden("Access Denied")

    role = request.user.profile.role

    if role != 'admin' and role != 'receptionist':
        return HttpResponseForbidden("Access Denied")

    membership = get_object_or_404(Membership, id=membership_id)

    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            membership.member.delete()
            return redirect('view_membership')

        plan = request.POST.get('plan', '').strip()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not plan or len(plan) > 30:
            return render(request, 'update_membership.html', {
                'membership': membership,
                'error': 'Enter a valid membership plan.'
            })

        if not start_date or not end_date or end_date < start_date:
            return render(request, 'update_membership.html', {
                'membership': membership,
                'error': 'Enter valid start and end dates.'
            })

        membership.plan = plan
        membership.start_date = start_date
        membership.end_date = end_date
        membership.active = request.POST.get('active') == 'on'
        membership.save()

        return redirect('view_membership')

    return render(request, 'update_membership.html', {
        'membership': membership
    })

@login_required
def create_membership(request):
    if not hasattr(request.user, 'profile'):
        return HttpResponseForbidden("Access Denied")

    role = request.user.profile.role

    if role != 'admin' and role != 'receptionist':
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        plan = request.POST.get('plan', '').strip()
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')

        if not all([first_name, last_name, email, password, plan,
                    start_date, end_date]):
            return render(request, 'create_membership.html', {
                'error': 'Please fill in all fields.'
            })

        if (len(first_name) > 150 or len(last_name) > 150
                or len(email) > 150 or len(plan) > 30):
            return render(request, 'create_membership.html', {
                'error': 'One of the fields is too long.'
            })

        if '@' not in email:
            return render(request, 'create_membership.html', {
                'error': 'Enter a valid email.'
            })

        if len(password) < 8:
            return render(request, 'create_membership.html', {
                'error': 'Password must be at least 8 characters.'
            })

        if end_date < start_date:
            return render(request, 'create_membership.html', {
                'error': 'End date cannot be before start date.'
            })

        if User.objects.filter(username__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
            return render(request, 'create_membership.html', {
                'error': 'This email is already registered.'
            })

        with transaction.atomic():
            member = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            Profile.objects.create(
                user=member,
                role='member'
            )

            Membership.objects.create(
                member=member,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                active=True
            )

        return redirect('view_membership')

    return render(request, 'create_membership.html')
