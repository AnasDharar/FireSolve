from django.db import models
from django.contrib.auth.models import User
# from PIL import Image  # For the profile picture

class UserProfile(models.Model):
    # ForeignKey to the default User model
    user = models.OneToOneField(User, on_delete=models.CASCADE) #This is named user_id in database
    
    # Basic Info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    
    # Profile Picture (using Pillow for image handling)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Graduation Info
    year_of_graduation = models.IntegerField(null=True, blank=True)
    branch = models.CharField(max_length=100,null=True, blank=True)
    degree = models.CharField(max_length=100,null=True, blank=True)
    college_name = models.CharField(max_length=255,null=True, blank=True)
    
    # Streak Info
    ultimate_streak = models.IntegerField(default=0,null=True, blank=True)


    codechef_streak = models.IntegerField(default=0,null=True, blank=True)
    codechef_last_solved = models.DateField(null=True, blank=True)
    
    codeforces_streak = models.IntegerField(default=0,null=True, blank=True)
    codeforces_last_solved = models.DateField(null=True, blank=True)

    leetcode_streak = models.IntegerField(default=0,null=True, blank=True)
    leetcode_last_solved = models.DateField(null=True, blank=True)
    
    # Platform IDs
    codechef_id = models.CharField(max_length=100, blank=True, null=True)
    codeforces_id = models.CharField(max_length=100, blank=True, null=True)
    leetcode_id = models.CharField(max_length=100, blank=True, null=True)
    gfg_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.username}"

    # Resize profile picture if it’s too big
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)