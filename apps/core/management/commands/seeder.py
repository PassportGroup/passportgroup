from django.core.management.base import BaseCommand
from apps.account.models import Account as PassportAccount
from apps.dashboard.models import PassportMail, PassportGroupTasks


MODE_REFRESH = 'refresh'
MODE_CLEAR = 'clear'
MODE_RESET = 'reset'


class Command(BaseCommand):
    help = "seeding database 🌱"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def truncate_db(self, hard=False):
        self.stdout.write('Truncating Database 🗑️🌱')
        if hard:
            PassportAccount.objects.all().delete()
        PassportMail.objects.all().delete()
        PassportGroupTasks.objects.all().delete()
        self.stdout.write('Truncating Completed! 🤩')

    def handle(self, *args, **options):
        self.stdout.write(self.help)
        if options['mode'] == MODE_CLEAR:
            self.truncate_db()
        elif options['mode'] == MODE_RESET:
            self.truncate_db(hard=True)
        else:
            self.truncate_db()
            self.stdout.write('Seeding Completed! 🤩')
