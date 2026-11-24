"""
URL configuration for gymguard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views
from memberships import views as membership_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('memberships/', membership_views.view_membership, name='view_membership'),
    path('memberships/update/<int:membership_id>/', membership_views.update_membership, name='update_membership'),
    path('memberships/create/', membership_views.create_membership, name='create_membership'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
