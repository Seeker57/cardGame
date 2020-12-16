from django.core.management.base import BaseCommand
from cardGame.models import Player
from django.core import serializers

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('fileName', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        for fileName in kwargs['fileName']:
            out = open(fileName, "w")
            XMLSerializer = serializers.get_serializer("xml")
            xml_serializer = XMLSerializer()
            players = Player.objects.all()
            xml_serializer.serialize(players, stream=out)

        self.stdout.write(self.style.SUCCESS('Данные об игроках успешно выгружены в файл "{0}"'.format(fileName)))