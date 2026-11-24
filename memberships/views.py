
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

from .models import Membership
from users.audit import log_action


def has_role(user, roles):
    return (
        hasattr(user, 'profile')
        and user.profile.active
        and user.profile.role in roles
    )


@login_required
def view_membership(request):
    if not has_role(
        request.user,
        ['member', 'trainer', 'receptionist', 'admin']
    ):
        return HttpResponseForbidden("Access Denied")

    role = request.user.profile.role

    if role == 'member':
        memberships = Membership.objects.filter(member=request.user)

    elif role == 'trainer':
        memberships = Membership.objects.filter(trainer=request.user)

    else:
        memberships = Membership.objects.all()

    return render(request, 'membership_list.html', {
        'memberships': memberships.select_related('member', 'trainer')
    })


@login_required
def update_membership(request, membership_id):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    membership = get_object_or_404(Membership, id=membership_id)

    trainers = User.objects.filter(
        profile__role='trainer',
        profile__active=True
    )

    if request.method == 'POST':
        plan = request.POST.get('plan', '').strip()
        trainer_id = request.POST.get('trainer', '')

        if not plan or len(plan) > 30:
            return render(request, 'update_membership.html', {
                'membership': membership,
                'trainers': trainers,
                'error': 'Enter a plan name between 1 and 30 characters.'
            })

        trainer = None

        if trainer_id:
            trainer = get_object_or_404(trainers, id=trainer_id)

        membership.plan = plan
        membership.trainer = trainer
        membership.active = request.POST.get('active') == 'on'
        membership.save()

        log_action(
            request,
            'MEMBERSHIP_UPDATED',
            f'Membership updated for {membership.member.username}'
        )

        return redirect('view_membership')

    return render(request, 'update_membership.html', {
        'membership': membership,
        'trainers': trainers
    })


@login_required
def create_membership(request):
    if not has_role(request.user, ['admin', 'receptionist']):
        return HttpResponseForbidden("Access Denied")

    members = User.objects.filter(profile__role='member')

    trainers = User.objects.filter(
        profile__role='trainer',
        profile__active=True
    )

    if request.method == 'POST':
        member_id = request.POST.get('member')
        trainer_id = request.POST.get('trainer', '')
        plan = request.POST.get('plan', '').strip()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not member_id or not plan or not start_date or not end_date:
            return render(request, 'create_membership.html', {
                'members': members,
                'trainers': trainers,
                'error': 'Please fill in all required fields.'
            })

        if len(plan) > 30 or end_date < start_date:
            return render(request, 'create_membership.html', {
                'members': members,
                'trainers': trainers,
                'error': 'Enter a valid plan and date range.'
            })

        member = get_object_or_404(members, id=member_id)

        trainer = None

        if trainer_id:
            trainer = get_object_or_404(trainers, id=trainer_id)

        if Membership.objects.filter(member=member).exists():
            return render(request, 'create_membership.html', {
                'members': members,
                'trainers': trainers,
                'error': 'This member already has a membership.'
            })

        membership = Membership.objects.create(
            member=member,
            trainer=trainer,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            active=True
        )

        log_action(
            request,
            'MEMBERSHIP_CREATED',
            f'Membership created for {member.username}'
        )

        return redirect('view_membership')

    return render(request, 'create_membership.html', {
        'members': members,
        'trainers': trainers
    })
