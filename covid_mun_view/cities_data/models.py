from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50)
    town_code = models.SmallIntegerField(default=-1)


class Agas(models.Model):
    name = models.CharField(max_length=100)
    agas_code = models.IntegerField(default=-1)


class CovidData(models.Model):
    ministry_id = models.IntegerField()
    town_code = models.SmallIntegerField(default=-1)
    agas_code = models.IntegerField(default=-1)
    date = models.DateField()
    accumulated_tested = models.IntegerField(default=-1)
    new_tested_on_date = models.BooleanField()
    accumulated_cases = models.IntegerField(default=-1)
    new_cases_on_date = models.BooleanField()
    accumulated_recoveries = models.IntegerField(default=-1)
    new_recoveries_on_date = models.BooleanField()
    accumulated_hospitalized = models.IntegerField(default=-1)
    new_hospitalized_on_date = models.BooleanField()
    accumulated_deaths = models.IntegerField(default=-1)
    new_deaths_on_date = models.BooleanField()
    agas = models.ForeignKey(Agas, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
