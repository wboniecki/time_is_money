from django.db import models
from django_mysql.models.fields import JSONField

class Auction(models.Model):
    isActive = models.BooleanField(default=True)
    auc = models.IntegerField()
    item = models.IntegerField()
    owner = models.CharField(max_length=20)
    ownerRealm = models.CharField(max_length=50)
    bid = models.CharField(max_length=255)
    # Buyout can be NULL (only BID)
    buyout = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField()
    timeLeft = models.CharField(max_length=20)
    rand = models.IntegerField()
    seed = models.CharField(max_length=60)
    context = models.IntegerField()
    # Additional data
    bonusLists = JSONField(null=True)
    modifiers = JSONField(null=True)
    petSpeciesId = models.IntegerField(null=True)
    petBreadId = models.IntegerField(null=True)
    petLevel = models.IntegerField(null=True)
    petQualityId = models.IntegerField(null=True)

    class Meta:
        abstract = True

