from time import sleep
from datetime import datetime

import requests

from django.core.management.base import BaseCommand, CommandError

from cities_data.models import CovidData, City, AgasCity


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('column', nargs=1)

    def handle(self, *args, **options):
        payload = {'resource_id': 'd07c0771-01a8-43b2-96cc-c6154e7fa9bd'}
        column = options['column'][0]
        url = 'https://data.gov.il'
        path = '/api/3/action/datastore_search'
        res = requests.get(f'{url}{path}', params=payload)
        res_json = res.json()
        records = res_json['result']['records']
        while records:
            for record in records:
                tested_on_date = True if record['new_tested_on_date'] == 'TRUE' else False
                cases_on_date = True if record['new_cases_on_date'] == 'TRUE' else False
                recoveries_on_date = True if record['new_recoveries_on_date'] == 'TRUE' else False
                hospitalize_on_date = True if record['new_hospitalized_on_date'] == 'TRUE' else False
                deaths_on_date = True if record['new_deaths_on_date'] == 'TRUE' else False

                city = City.objects.filter(code=record['town_code']).first()

                if not city:
                    self.stdout.write(f'city not found! {city}')
                    return

                agas_code = record['agas_code'] if record['agas_code'] else -1

                agas_city = AgasCity.objects.filter(city=city,
                                                    code=agas_code).first()

                if not agas_city:
                    self.stdout.write(f'agas_city not found! {agas_city}')
                    return

                covid_data_row = CovidData.objects.get(ministry_id=record['_id'])
                if '<' not in record[column]:
                    setattr(covid_data_row, column, record[column])
                covid_data_row.save()
            sleep(1)
            self.stdout.write(f"getting the next batch from {res_json['result']['_links']['next']}")
            res = requests.get(f"{url}{res_json['result']['_links']['next']}")
            res_json = res.json()
            records = res_json['result']['records']
        self.stdout.write(f'all done!')
