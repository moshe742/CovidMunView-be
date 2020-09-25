from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    code = models.SmallIntegerField(unique=True)

    def __str__(self):
        return f'{self.name}: {self.code}'


class AgasCity(models.Model):
    districts = models.CharField(max_length=100, default='unknown')
    main_streets = models.CharField(max_length=300, null=True, blank=True)
    code = models.IntegerField(default=-1)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.districts}: {self.code}, {self.city}'


class CovidData(models.Model):
    ministry_id = models.IntegerField()
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
    agas_city = models.ForeignKey(AgasCity, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.ministry_id}- {self.date}, {self.agas_city}'
