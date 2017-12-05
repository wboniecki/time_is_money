from django.db import models
from django_mysql.models.fields import JSONField

class ItemRealmTimeSeriesDataDaily(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    item = models.ForeignKey('model_item.Item', on_delete=models.CASCADE)
    connected_realm = models.ForeignKey('model_realm.ConnectedRealm', on_delete=models.CASCADE)
    last_hourly = models.ForeignKey('ItemRealmTimeSeriesDataHourly')
    # min market price
    min_market_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # max market price
    max_market_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # avg market price
    avg_market_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # min price
    min_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # max pirce
    max_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # avg price
    avg_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # open market price
    open_market_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # end market price
    end_market_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # min quantity
    min_quantity = models.IntegerField(default=0)
    # max quantity
    max_quantity = models.IntegerField(default=0)
    # avg quantity
    avg_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'item_realm_tsd'
        indexes = [
            models.Index(fields=['connected_realm', 'date'])
        ]

class ItemRealmTimeSeriesDataHourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    item = models.ForeignKey('model_item.Item', on_delete=models.CASCADE)
    connected_realm = models.ForeignKey('model_realm.ConnectedRealm', on_delete=models.CASCADE)
    # market price
    market_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # avg price
    avg_price = models.DecimalField(max_digits=13, decimal_places=4, default=0)
    # quantity
    quantity = models.IntegerField(default=0)
    # standard deviation
    standard_deviation = models.DecimalField(max_digits=13, decimal_places=4, default=0)

    class Meta:
        db_table = 'item_realm_tsd_hourly'
        indexes = [
            models.Index(fields=['connected_realm', 'datetime'])
        ]
