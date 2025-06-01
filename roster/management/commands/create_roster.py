from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from user.models import AuthUser, WorkingDetail
from roster.models import Roster, RosterDetail

class Command(BaseCommand):
    help = 'Creates tomorrow\'s rosters for all active employees'

    def handle(self, *args, **options):
        tomorrow = timezone.now().date() + timedelta(days=1)
        active_employees = AuthUser.objects.filter(is_active=True)

        for employee in active_employees:
            try:
                working_detail = employee.working_detail
                shift = working_detail.shift
                if not shift:
                    continue
            except WorkingDetail.DoesNotExist:
                continue

            roster, _ = Roster.objects.get_or_create(
                employee=employee,
                date=tomorrow,
                defaults={'created_by': None}
            )

            already_exists = RosterDetail.objects.filter(roster=roster, shift=shift).exists()
            if not already_exists:
                RosterDetail.objects.create(
                    roster=roster,
                    shift=shift,
                    created_by=None
                )
        self.stdout.write(self.style.SUCCESS('Tomorrow\'s rosters created successfully.'))