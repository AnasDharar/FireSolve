# Generated by Django 5.2.4 on 2025-07-25 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='total_solved',
            field=models.IntegerField(default=0),
        ),
    ]
