from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Platform(models.Model): #this is just used to identify the platform of the problem with id
    name = models.CharField(max_length=50, unique=True)  # Codeforces, CodeChef

    def __str__(self):
        return self.name

# id |  name
# ------------- 
#  1 |  Codechef
#  2 |  Codeforces

class Problem(models.Model): #this is used to store the problem details
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    problem_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ('platform', 'problem_id')
    
    def __str__(self):
        return f"{self.platform.name} - {self.problem_id}: {self.title}"
#  id |  platform_id |  problem_id |  title
#   1 |  1           |  1023A      |  Sample Problem

class POTDStatus(models.Model): #a new row is made whenever user solved a problem.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    assigned_date = models.DateField()

    class Meta:
        unique_together = ('user', 'problem')
    def __str__(self):
        return f"{self.user.username} solved {self.problem.title}
# id |  user_id |  problem_id |  assigned_date |  solved_date
#  1 |  1       |  1          |  2023-10-01    |  2023-10-02