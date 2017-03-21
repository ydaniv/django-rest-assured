from django.db import models
from rest_framework.reverse import reverse


class Stuff(models.Model):
    name = models.CharField(max_length=200)
    answer = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        app_label = 'tests'

    def get_absolute_url(self):
        return reverse('stuff-detail', [self.pk])


class RelatedStuff(models.Model):
    thing = models.ForeignKey(Stuff)

    class Meta:
        app_label = 'tests'


class ManyRelatedStuff(models.Model):
    stuff = models.ManyToManyField(Stuff)

    class Meta:
        app_label = 'tests'
