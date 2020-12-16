from django.core.management.base import BaseCommand
from cardGame.models import Player

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('fileName', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        for fileName in kwargs['fileName']:
            Player.objects.to_csv(fileName, delimiter=';')

        self.stdout.write(self.style.SUCCESS('Данные об игроках успешно выгружены в файл "{0}"'.format(fileName)))