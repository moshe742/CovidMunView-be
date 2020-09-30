import logging
from datetime import datetime

from django.http import JsonResponse
from django.views import View
from django.core import serializers

from cities_data.models import CovidData

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CovidCity(View):
    def get(self, request, city, start_date=None, end_date=None):
        logger.debug('start get')
        covid_by_city = CovidData.objects.filter(agas_city__city__code=city)
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            covid_by_city = covid_by_city.filter(date__gte=start_date)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            covid_by_city = covid_by_city.filter(date__lte=end_date)
        covid_by_area = covid_by_city.all()
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
