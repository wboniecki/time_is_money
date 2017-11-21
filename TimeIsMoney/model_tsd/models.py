from django.db import models
from django_mysql.models.fields import JSONField

class ItemRealmTimeSeriesData(models.Model):
    item = models.ForeignKey('model_item.Item', on_delete=models.CASCADE)
    connected_realm = models.ForeignKey('model_realm.ConnectedRealm', on_delete=models.CASCADE)
    class Meta:
        db_table = 'item_realm_tsd'
