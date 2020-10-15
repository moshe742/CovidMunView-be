import csv

from django.core.management.base import BaseCommand, CommandError

from cities_data.models import (
    AgasCity,
    City
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('/home/moshe/street_map.csv') as f:
            file_data = f.readlines()

        csv_data = csv.reader(file_data)
        next(csv_data)

        # 0- city name, 1- city code, 2- agas code, 3- districts, 4- main streets
        for row in csv_data:
            city = City.objects.get(code=row[1])
            agas_city = AgasCity.objects.filter(city=city).filter(code=row[2])
            print(f'{agas_city.count()}, row 2: {row[2]}')
            agas_city[0].districts = row[3]
            agas_city[0].main_streets = row[4]
            agas_city[0].save()
