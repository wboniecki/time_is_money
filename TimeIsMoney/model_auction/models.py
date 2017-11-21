from django.db import models
from django_mysql.models.fields import JSONField

from model_realm.models import Realm

class Auction(models.Model):
    id = models.BigAutoField(primary_key=True)
    isActive = models.BooleanField(default=True)
    auc = models.IntegerField()
    item = models.IntegerField()
    owner = models.CharField(max_length=60)
    ownerRealm = models.CharField(max_length=60)
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        realm = Realm.objects.filter(name=self.ownerRealm).first()
        if realm:
            super(Auction, self).save()
        else:
            return


    class Meta:
        db_table = 'auction'
        indexes = [
            models.Index(fields=['ownerRealm', 'auc']),
            models.Index(fields=['ownerRealm', 'owner']),
            models.Index(fields=['ownerRealm'])
        ]

class AuctionDailyStats(models.Model):
    date = models.DateField(auto_now=True, auto_now_add=False)
    connected_realm = models.ForeignKey('model_realm.ConnectedRealm', on_delete=models.CASCADE)
    created = models.IntegerField(default=0)
    updated = models.IntegerField(default=0)
    deprecated = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    class Meta:
        db_table = 'auc_daily_stat'
        indexes = [
            models.Index(fields=['date', 'connected_realm'])
        ]

class AuctionUpdateTimeStat(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    connected_realm = models.ForeignKey('model_realm.ConnectedRealm', on_delete=models.CASCADE)
    crud_count = models.IntegerField(default=0)
    time_start = models.TimeField(auto_now=False, auto_now_add=False)
    time_stop = models.TimeField(auto_now=False, auto_now_add=False)
    class Meta:
        db_table = 'auc_update_time_stat'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['connected_realm', 'date'])
        ]
