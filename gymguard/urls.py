
from django.contrib import admin
from django.urls import path

from users import views
from memberships import views as membership_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Trainer management
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainers/create/', views.create_trainer, name='create_trainer'),
    path(
        'trainers/toggle/<int:trainer_id>/',
        views.toggle_trainer,
        name='toggle_trainer'
    ),
    path(
        'trainers/my-members/',
        views.assigned_members,
        name='assigned_members'
    ),

    # Member management
    path('members/', views.member_list, name='member_list'),
    path('members/create/', views.create_member, name='create_member'),
    path(
        'members/toggle/<int:member_id>/',
        views.toggle_member,
        name='toggle_member'
    ),

    # Audit logs
    path('audit-logs/', views.audit_logs, name='audit_logs'),

    # Membership management
    path(
        'memberships/',
        membership_views.view_membership,
        name='view_membership'
    ),
    path(
        'memberships/update/<int:membership_id>/',
        membership_views.update_membership,
        name='update_membership'
    ),
    path(
        'memberships/create/',
        membership_views.create_membership,
        name='create_membership'
    ),
]
