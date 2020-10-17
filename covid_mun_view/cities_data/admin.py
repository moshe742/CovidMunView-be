from django.contrib import admin

from cities_data.models import (
    City,
    AgasCity,
    CovidData,
    CityData,
)


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class AgasCityAdmin(admin.ModelAdmin):
    list_display = ['city', 'code', 'districts', 'main_streets']


class CovidDataAdmin(admin.ModelAdmin):
    list_display = ['date', 'agas_city', 'ministry_id']


class CityDataAdmin(admin.ModelAdmin):
    list_display = ['date', 'city', 'ministry_id']


admin.site.register(City, CityAdmin)
admin.site.register(AgasCity, AgasCityAdmin)
admin.site.register(CovidData, CovidDataAdmin)
admin.site.register(CityData, CityDataAdmin)
