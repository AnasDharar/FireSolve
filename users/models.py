from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codechef_username = models.CharField(max_length=100)
    codeforces_username = models.CharField(max_length=100)
    leetcode_username = models.CharField(max_length=100)
    streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"
