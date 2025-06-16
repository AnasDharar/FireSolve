from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class POTDStatus(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     platform = models.CharField(max_length=20, choices=[
#         ('codeforces', 'Codeforces'),
#         ('codechef', 'CodeChef'),
#     ])
#     problem_id = models.CharField(max_length=100)
    
#     assigned_date = models.DateField()  # When this was the POTD
#     solved_date = models.DateField()    # When user solved it

#     solved_on_time = models.BooleanField()  # True = same day, False = late

#     class Meta:
#         unique_together = ('user', 'platform', 'problem_id')  # Avoid duplicates