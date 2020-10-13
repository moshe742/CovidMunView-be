import logging
from datetime import datetime

from django.http import JsonResponse
from django.views import View
from django.core import serializers

from cities_data.models import CovidData, AgasCity, City

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CovidAgasView(View):
    def get(self, request):
        agases = AgasCity.objects.select_related('city').all()
        res = []
        for agas in agases:
            d = {
                'districts': agas.districts,
                'main_streets': agas.main_streets,
                'agas_code': agas.code,
                'city_code': agas.city.code,
                'city': agas.city.name
            }
            res.append(d)
        return JsonResponse(res, safe=False)


class CovidCityView(View):
    def get(self, request):
        cities = City.objects.all()
        res = []
        for city in cities:
            d = {
                'name': city.name,
                'code': city.code,
            }
            res.append(d)
        return JsonResponse(res, safe=False)


class CovidDataView(View):
    def get(self, request, city, start_date=None, end_date=None):
        logger.debug('start get')
        num_of_agases_at_city = 0
        covid_by_city = CovidData.objects.select_related('agas_city').select_related('agas_city__city').filter(agas_city__city__code=city).order_by('-date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            covid_by_city = covid_by_city.filter(date__gte=start_date)
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            covid_by_city = covid_by_city.filter(date__lte=end_date)
        elif start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            covid_by_city = covid_by_city.filter(date=start_date)
        else:
            num_of_agases_at_city = AgasCity.objects.filter(city__code=city).count()

        covid_by_area = covid_by_city
        if num_of_agases_at_city:
            covid_by_area = covid_by_area[:num_of_agases_at_city]
        # data = serializers.serialize('json', covid_by_area)
        res = []
        for area in covid_by_area:
            d = dict(
                city_code=area.agas_city.city.code,
                agas_code=area.agas_city.code,
                date=area.date.strftime('%d/%m/%Y'),
                accumulated_tested=area.accumulated_tested,
                new_tested_on_date=area.new_tested_on_date,
                accumulated_cases=area.accumulated_cases,
                new_cases_on_date=area.new_cases_on_date,
                accumulated_recoveries=area.accumulated_recoveries,
                new_recoveries_on_date=area.new_recoveries_on_date,
                accumulated_hospitalized=area.accumulated_hospitalized,
                new_hospitalized_on_date=area.new_hospitalized_on_date,
                accumulated_deaths=area.accumulated_deaths,
                new_deaths_on_date=area.new_deaths_on_date,
                agas=area.agas_city.districts,
                city=area.agas_city.city.name,
            )
            res.append(d)
        logger.debug('end get')
        return JsonResponse(res, safe=False)
