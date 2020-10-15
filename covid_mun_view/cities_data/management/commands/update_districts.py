import logging
import csv

from django.core.management.base import BaseCommand, CommandError

from cities_data.models import (
    AgasCity,
    City
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('/home/moshe/street_map.csv') as f:
            file_data = f.readlines()

        csv_data = csv.reader(file_data)

        # 0- city name, 1- city code, 2- agas code, 3- districts, 4- main streets
        for row in csv_data:
            city = City.objects.get(code=row[1])
            agas_city = AgasCity.objects.filter(city=city)
            agas_city_filtered = agas_city.filter(code=row[2])
            try:
                agas_city_filtered[0].districts = row[3]
                agas_city_filtered[0].main_streets = row[4] if row[4] else 'unknown'
                logger.info(f'districts: {agas_city_filtered[0].districts}')
                agas_city_filtered[0].save(force_update=True)
            except IndexError:
                logger.error(f"agas {row[2]} in city {row[1]} doesn't exist")
                logger.info(f'creating agas {row[2]} in city {row[1]}')
                main_streets = row[4] if row[4] else 'unknown'
                agas_city_new = AgasCity(districts=row[3], main_streets=main_streets, code=row[2], city=city)
                agas_city_new.save()
