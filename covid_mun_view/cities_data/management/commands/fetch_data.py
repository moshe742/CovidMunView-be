from datetime import datetime, date, timedelta
from time import sleep

import requests

from django.core.management.base import BaseCommand, CommandError

from cities_data.models import CovidData, City, AgasCity


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--all', action='count', default=0)
        parser.add_argument('--date', nargs=1)

    def run_queries(self, payload):
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
            sleep(2)
            self.stdout.write(f"getting the next batch from {res_json['result']['_links']['next']}")
            res = requests.get(f"{url}{res_json['result']['_links']['next']}")
            res_json = res.json()
            records = res_json['result']['records']
        self.stdout.write(f'all done with date {payload["q"]}')

    def handle(self, *args, **options):
        payload = {'resource_id': 'd07c0771-01a8-43b2-96cc-c6154e7fa9bd'}

        if options['all'] < 1 and not options['date']:
            first_record = CovidData.objects.first()
            dates_range = [first_record.date + timedelta(num) for num in range(1, (date.today() - first_record.date).days)]
            for day in dates_range:
                payload['q'] = day.strftime('%Y/%m/%d')
                self.run_queries(payload)
        elif options['date']:
            date_to_fetch = datetime.strptime(options['date'][0], '%Y-%m-%d')
            payload['q'] = date_to_fetch.strftime('%Y/%m/%d')
            self.run_queries(payload)
        elif options['all'] > 0:
            self.run_queries(payload)
