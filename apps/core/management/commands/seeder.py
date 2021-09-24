from django.core.management.base import BaseCommand
from apps.account.models import Account as AccountReport

MODE_REFRESH = 'refresh'

MODE_CLEAR = 'clear'

# python manage.py seeder --mode=clear/refresh


class Command(BaseCommand):
    help = "seeding database🌱"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def truncate_db(self):
        self.stdout.write('Truncating Database 🗑️ 🌱')
        AccountReport.objects.all().delete()
        self.stdout.write('Truncating Completed!🤩')

    def handle(self, *args, **options):
        self.stdout.write(self.help)
        if options['mode'] == MODE_CLEAR:
            self.truncate_db()
        else:
            self.truncate_db()
            self.stdout.write('Seeding Completed!🤩')
