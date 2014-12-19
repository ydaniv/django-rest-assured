from django.core.management import call_command
from django.db import models


class Stuff(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        app_label = 'tests'


import django

django.setup()

call_command('migrate')
