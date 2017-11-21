'''
wboniecki 2017-11-05
Model class of Realm table from database
Realm table contains info about model.realm like is model.realm active, model.realm region and last auctions update
Best way to edit some records is use /admin site
'''
from django.db import models
from django_mysql.models.fields import JSONField
from django.db.models.signals import pre_save

class Realm(models.Model):
    # TODO: Nowy podział na us i eu, usuwa region
    regions = (
        ('eu', 'eu'),
        ('us', 'us'),
    )
    region = models.CharField(
        max_length=2,
        choices=regions,
    )
    locale = models.CharField(max_length=5, blank=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=60)
    lastModified = models.CharField(max_length=60, default='0', blank=True)
    dateModified = models.DateTimeField(auto_now=False, auto_now_add=False)
    isActive = models.BooleanField(blank=True, default=False)
    status = models.BooleanField(blank=True, default=True)
    populations = (
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', "high"),
    )
    population = models.CharField(max_length=20)
    connected_realm = models.ForeignKey('ConnectedRealm')
    dateChecked = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'realm'

def preSaveRec(sender, instance, *args, **kwargs):
    if instance.region == 'eu':
        instance.locale = 'en_GB'
    elif instance.region == 'us':
        instance.locale = 'en_US'


pre_save.connect(preSaveRec, sender=Realm)

class ConnectedRealm(models.Model):
    realms = JSONField()
    status = models.BooleanField(blank=True, default=True)
    class Meta:
        db_table = 'connected_realm'
