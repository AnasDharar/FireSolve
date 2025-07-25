# Generated by Django 5.2 on 2025-07-19 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_current_streak_userprofile_ultimate_streak_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='codechef_last_solved',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='codeforces_last_solved',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='leetcode_last_solved',
            field=models.DateField(blank=True, null=True),
        ),
    ]
