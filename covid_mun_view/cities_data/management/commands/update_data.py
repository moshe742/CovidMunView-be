from time import sleep

import requests

from django.core.management.base import BaseCommand, CommandError

from cities_data.models import CovidData, City, AgasCity


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('column', nargs=1)

    def handle(self, *args, **options):
        payload = {'resource_id': 'd07c0771-01a8-43b2-96cc-c6154e7fa9bd'}
        column = options['column']
