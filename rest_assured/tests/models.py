from django.core.management import call_command
from django.db import models


class Stuff(models.Model):

    class Meta:
        app_label = 'tests'

    name = models.CharField(max_length=200)

import django
django.setup()

call_command('migrate')
