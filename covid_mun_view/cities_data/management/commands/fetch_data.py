from datetime import date, timedelta
from time import sleep

import requests

from django.core.management.base import BaseCommand, CommandError

from cities_data.models import CovidData, City, Agas


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--all')

    def handle(self, *args, **options):
        cities = City.objects.all()
        agases = Agas.objects.all()

        url = 'https://data.gov.il'
        path = '/api/3/action/datastore_search'
        payload = {'resource_id': 'd07c0771-01a8-43b2-96cc-c6154e7fa9bd'}
        if not options['all']:
            today = date.today() + timedelta(days=-3)
            date_to_check = today.strftime('%Y/%m/%d')
            payload['q'] = date_to_check

        res = requests.get(f'{url}{path}', params=payload)
        res_json = res.json()
        records = res_json['result']['records']
        while records:
            for record in records:
                covid_data = CovidData(
                    ministry_id=record['_id'],
                    town_code=record['town_code'],
                    agas_code=record['agas_code'],
                    date=record['date'],
                    accumulated_tests=record['accumulated_tests'],
                    new_tested_on_date=record['new_tested_on_date'],
                    accumulated_cases=record['accumulated_cases'],
                    new_cases_on_date=record['new_cases_on_date'],
                    accumulated_recoveries=record['accumulated_recoveries'],
                    new_recoveries_on_date=record['new_recoveries_on_date'],
                    accumulated_hospitalized=record['accumulated_hospitalized'],
                    new_hospitalized_on_date=record['new_hospitalized_on_date'],
                    accumulated_deaths=record['accumulated_deaths'],
                    new_deaths_on_date=record['new_deaths_on_date'],
                    agas=agases[record['agas_code']],
                    city=cities[record['city_code']],
                )
                covid_data.save()
            sleep(5)
            self.stdout(f"getting the next batch from {res_json['result']['_links']['next']}")
            res = requests.get(f"{url}{res_json['result']['_links']['next']}")
            res_json = res.json()
            records = res_json['result']['records']
        self.stdout('all done!')
