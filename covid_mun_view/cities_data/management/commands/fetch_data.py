from datetime import datetime, date, timedelta
from time import sleep

import requests

from django.core.management.base import BaseCommand, CommandError

from cities_data.models import (
    CovidData,
    City,
    AgasCity,
    CityData,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true')
        parser.add_argument('--date', nargs=1)
        parser.add_argument('--data_type', nargs=1)

    def add_covid_data(self, record):
        tested_on_date = True if record['new_tested_on_date'] == 'TRUE' else False
        cases_on_date = True if record['new_cases_on_date'] == 'TRUE' else False
        recoveries_on_date = True if record['new_recoveries_on_date'] == 'TRUE' else False
        hospitalize_on_date = True if record['new_hospitalized_on_date'] == 'TRUE' else False
        deaths_on_date = True if record['new_deaths_on_date'] == 'TRUE' else False

        city = City.objects.filter(code=record['town_code']).first()

        if not city:
            city = City(name=record['town'], code=record['town_code'])
            city.save()
        agas_code = record['agas_code'] if record['agas_code'] else -1

        agas_city = AgasCity.objects.filter(city=city,
                                            code=agas_code).first()

        if not agas_city:
            agas_city = AgasCity(districts='unknown', main_streets='unknown',
                                 code=agas_code, city=city)
            agas_city.save()

        date_stats = datetime.strptime(record['date'], '%Y/%m/%d')
        covid_data = CovidData(
            ministry_id=record['_id'],
            date=date_stats,
            new_tested_on_date=tested_on_date,
            new_cases_on_date=cases_on_date,
            new_recoveries_on_date=recoveries_on_date,
            new_hospitalized_on_date=hospitalize_on_date,
            new_deaths_on_date=deaths_on_date,
            agas_city=agas_city,
        )
        if '<' not in record['accumulated_tested']:
            covid_data.accumulated_tested = record['accumulated_tested']
        if '<' not in record['accumulated_cases']:
            covid_data.accumulated_cases = record['accumulated_cases']
        if '<' not in record['accumulated_recoveries']:
            covid_data.accumulated_recoveries = record['accumulated_recoveries']
        if '<' not in record['accumulated_hospitalized']:
            covid_data.accumulated_hospitalized = record['accumulated_hospitalized']
        if '<' not in record['accumulated_deaths']:
            covid_data.accumulated_deaths = record['accumulated_deaths']
        covid_data.save()

    def add_city_data(self, record):
        pass

    def run_queries(self, data_type, date_=None):
        url = 'https://data.gov.il'
        path = '/api/3/action/datastore_search'
        payload = {
            'covid': {'resource_id': 'd07c0771-01a8-43b2-96cc-c6154e7fa9bd'},
            'city': {'resource_id': '8a21d39d-91e3-40db-aca1-f73f7ab1df69'}
        }
        date_format = {
            'covid': '%Y/%m/%d',
            'city': '%Y-%m-%d'
        }
        if date_:
            payload[data_type]['q'] = date_.strftime(date_format[data_type])
        res = requests.get(f'{url}{path}', params=payload[data_type])
        res_json = res.json()
        records = res_json['result']['records']
        while records:
            for record in records:
                self.add_covid_data(record)
            sleep(1)
            self.stdout.write(f"getting the next batch from {res_json['result']['_links']['next']}")
            res = requests.get(f"{url}{res_json['result']['_links']['next']}")
            res_json = res.json()
            records = res_json['result']['records']
        self.stdout.write(f'all done with date {payload["q"]}')

    def handle(self, *args, **options):
        if options['date']:
            date_to_fetch = datetime.strptime(options['date'][0], '%Y-%m-%d')
            self.run_queries(options['data_type'], date_to_fetch)
        elif options['all']:
            self.run_queries(options['data_type'])
        else:
            first_record = CovidData.objects.first()
            dates_range = [first_record.date + timedelta(num) for num in
                           range(1, (date.today() - first_record.date).days)]
            for day in dates_range:
                self.run_queries('covid', day)
            first_record = CityData.objects.first()
            dates_range = [first_record.date + timedelta(num) for num in
                           range(1, (date.today() - first_record.date).days)]
            for day in dates_range:
                self.run_queries('city', day)
