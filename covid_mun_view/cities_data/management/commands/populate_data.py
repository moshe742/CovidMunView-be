import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from cities_data.models import CovidData, City, AgasCity


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--cities')
        parser.add_argument('--agases')
        parser.add_argument('--both')
        parser.add_argument('--csv')

    def handle(self, *args, **options):
        if options['csv']:
            with open(options['csv']) as f:
                input_data = f.readlines()
        csv_data = csv.reader(input_data[1:])

        for row in csv_data:
            city = City(name=row[0], code=row[1])
            try:
                city.save()
            except IntegrityError:
                city = City.objects.filter(code=row[1]).first()
            agas = AgasCity(districts=row[3], code=row[2], main_streets=row[4], city=city)
            agas.save()
