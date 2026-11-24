from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from users.models import Profile
from .models import Membership


class MembershipAccessTests(TestCase):

    def setUp(self):
        self.member = User.objects.create_user(
            username='member',
            password='StrongPass123!'
        )
        Profile.objects.create(user=self.member, role='member')

        self.other = User.objects.create_user(
            username='other',
            password='StrongPass123!'
        )
        Profile.objects.create(user=self.other, role='member')

        Membership.objects.create(
            member=self.member,
            plan='Basic',
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31)
        )

    def test_member_only_sees_own_membership(self):
        self.client.login(
            username='other',
            password='StrongPass123!'
        )

        response = self.client.get(reverse('view_membership'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Basic')

    def test_member_cannot_create_membership(self):
        self.client.login(
            username='member',
            password='StrongPass123!'
        )

        response = self.client.get(reverse('create_membership'))
        self.assertEqual(response.status_code, 403)