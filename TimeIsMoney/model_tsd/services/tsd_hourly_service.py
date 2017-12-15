import datetime
from ..models import ItemRealmTimeSeriesDataHourly
from django.db import connection


class TSDHourlyService:
    def create(self, _item, _connected_realm, _data):
        tsd_hourly = ItemRealmTimeSeriesDataHourly()
        tsd_hourly.datetime = _data['datetime']
        tsd_hourly.item = _item
        tsd_hourly.connected_realm = _connected_realm
        tsd_hourly.market_price = _data['market_price']
        tsd_hourly.avg_price = _data['avg_price']
        tsd_hourly.quantity = _data['quantity']
        tsd_hourly.standard_deviation = _data['standard_deviation']
        #tsd_hourly.save()
        return tsd_hourly

    def deleteOldTSD(self):
        today = datetime.date.today()
        to_date = today - datetime.timedelta(days=15)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM %s WHERE `datetime`< '%s'" % (ItemRealmTimeSeriesDataHourly._meta.db_table, to_date))
        cursor.execute("OPTIMIZE TABLE %s" % ItemRealmTimeSeriesDataHourly._meta.db_table)
        return to_date

    def getRealmDailyData(self, _item_id, _connected_realm_id, _date):
        return ItemRealmTimeSeriesDataHourly.objects.filter(datetime__date=_date, item=_item_id, connected_realm=_connected_realm_id)

    def getRealmItemChartData(self, _item_id, _connected_realm_id):
        today = datetime.datetime.now()
        from_date = today - datetime.timedelta(days=14)
        tsd_list = ItemRealmTimeSeriesDataHourly.objects.filter(datetime__range=[from_date, today], item=_item_id, connected_realm=_connected_realm_id).order_by('datetime')
        return tsd_list


    def getRealmItemLastData(self, _item_id, _connected_realm_id):
        return ItemRealmTimeSeriesDataHourly.objects.filter(item=_item_id, connected_realm=_connected_realm_id).order_by('-datetime').first()
