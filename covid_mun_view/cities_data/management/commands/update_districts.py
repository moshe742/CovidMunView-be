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
            agas_city = AgasCity.objects.filter(city=city.id)
            agas_city_filtered = agas_city.filter(code=int(row[2]))
            try:
                agas_city_filtered[0].districts = row[3]
                agas_city_filtered[0].main_streets = row[4]
                agas_city_filtered[0].save()
            except IndexError as e:
                logger.error(str(e))
                logger.info(str(agas_city))
                logger.info(row[2])
                logger.info(str(city))
                logger.info(row)
