from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, AuditLog


class GymGuardSecurityTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin-test',
            password='StrongPass123!'
        )
        Profile.objects.create(user=self.admin, role='admin')

        self.member = User.objects.create_user(
            username='member-test',
            password='StrongPass123!'
        )
        Profile.objects.create(user=self.member, role='member')

    def test_login_rejects_invalid_password(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'admin-test', 'password': 'wrong'}
        )
        self.assertEqual(response.status_code, 401)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_member_cannot_view_audit_logs(self):
        self.client.login(
            username='member-test',
            password='StrongPass123!'
        )
        response = self.client.get(reverse('audit_logs'))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_view_audit_logs(self):
        self.client.login(
            username='admin-test',
            password='StrongPass123!'
        )
        response = self.client.get(reverse('audit_logs'))
        self.assertEqual(response.status_code, 200)

    def test_logout_requires_post(self):
        self.client.login(
            username='admin-test',
            password='StrongPass123!'
        )
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)

    def test_login_form_enforces_csrf(self):
        secure_client = Client(enforce_csrf_checks=True)

        response = secure_client.post(
            reverse('login'),
            {'username': 'admin-test', 'password': 'StrongPass123!'}
        )
        self.assertEqual(response.status_code, 403)

    def test_successful_login_is_audited(self):
        self.client.post(
            reverse('login'),
            {'username': 'admin-test', 'password': 'StrongPass123!'}
        )

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.admin,
                action='LOGIN'
            ).exists()
        )