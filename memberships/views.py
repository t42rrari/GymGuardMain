from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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

    return render(request, 'membership_list.html', {'memberships': memberships})

@login_required
def update_membership(request, membership_id):
    if not hasattr(request.user, 'profile'):
        return HttpResponseForbidden("Access Denied")

    role = request.user.profile.role

    if role != 'admin' and role != 'receptionist':
        return HttpResponseForbidden("Access Denied")

    membership = get_object_or_404(Membership, id=membership_id)

    if request.method == 'POST':
        plan = request.POST.get('plan', '').strip()

        if not plan or len(plan) > 30:
            return render(request, 'update_membership.html', {
                'membership': membership,
                'error': 'Enter a plan name between 1 and 30 characters.'
            })

        membership.plan = plan
        membership.active = request.POST.get('active') == 'on'
        membership.save()

        return redirect('view_membership')

    return render(request, 'update_membership.html', {'membership': membership})
