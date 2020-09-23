from django.http import JsonResponse
from django.views import View

from cities_data.models import CovidData


class CovidCity(View):
    def get(self, request):
        covid_by_area = CovidData.objects.all()
        res = []
        for area in covid_by_area:
            d = dict(
                town_code=area.town_code,
                agas_code=area.agas_code,
                date=area.date,
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
                agas=area.agas,
                city=area.city,
            )
            res.append(d)
        return JsonResponse(res)