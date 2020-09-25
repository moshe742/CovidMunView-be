from django.contrib import admin

from cities_data.models import City, AgasCity, CovidData

# Register your models here.
admin.site.register(City)
admin.site.register(AgasCity)
admin.site.register(CovidData)
