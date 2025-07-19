from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import UserProfile  # adjust import

class Command(BaseCommand):
    help = "Reset streaks for users who missed yesterday"

    def handle(self, *args, **options):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)
        profiles = UserProfile.objects.all()

        updated = 0
        for profile in profiles:
            changed = False

            for platform in ["codechef", "codeforces", "leetcode"]:
                streak_field = f"{platform}_streak"
                last_field = f"{platform}_last_solved"
                streak_val = getattr(profile, streak_field)
                last_date = getattr(profile, last_field)

                if streak_val > 0 and (last_date is None or last_date < yesterday):
                    setattr(profile, streak_field, 0)
                    changed = True
                    setattr(profile, "ultimate_streak", 0)  # Reset ultimate streak as well
            
            if changed:
                profile.save(update_fields=[
                    'codechef_streak', 'codeforces_streak', 'leetcode_streak', 'ultimate_streak'
                ])
                updated += 1
                print(f"Streaks for {profile.user.username} have been reset successfully.")

        self.stdout.write(self.style.SUCCESS(f"Reset {updated} profiles."))
