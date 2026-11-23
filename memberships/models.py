from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Membership(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.member.username

