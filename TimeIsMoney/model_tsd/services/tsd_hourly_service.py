import datetime
from ..models import ItemRealmTimeSeriesDataHourly
from django.db import connection
from contextlib import closing


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

    def batchInsert(self, _data, _connected_realm_id):
        pre_sql = 'INSERT INTO %s (datetime, market_price, avg_price, quantity, standard_deviation, connected_realm_id, item_id, max_price, min_price) VALUES {}' % ItemRealmTimeSeriesDataHourly._meta.db_table
        sql = pre_sql.format(
            ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s)'] * len(_data))
        )
        params = []
        for each in _data:
            params.extend([each[1]['datetime'],
                           each[1]['market_price'],
                           each[1]['avg_price'],
                           each[1]['quantity'],
                           each[1]['standard_deviation'],
                           _connected_realm_id,
                           each[0].id,
                           each[1]['max_price'],
                           each[1]['min_price']])
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql, params)


    def deleteOldTSD(self):
        today = datetime.date.today()
        to_date = today - datetime.timedelta(days=15)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM %s WHERE `datetime`< '%s'" % (ItemRealmTimeSeriesDataHourly._meta.db_table, to_date))
        cursor.execute("OPTIMIZE TABLE %s" % ItemRealmTimeSeriesDataHourly._meta.db_table)
        return to_date

    def getRealmDailyData(self, _item_id, _connected_realm_id, _date):
        return ItemRealmTimeSeriesDataHourly.objects.filter(datetime__date=_date, item=_item_id, connected_realm=_connected_realm_id)

    def getRealmAllDailyData(self, _connected_realm_id, _date):
        return ItemRealmTimeSeriesDataHourly.objects.filter(datetime__date=_date, connected_realm=_connected_realm_id)

    def getRealmItemChartData(self, _item_id, _connected_realm_id):
        today = datetime.datetime.now()
        from_date = today - datetime.timedelta(days=14)
        tsd_list = ItemRealmTimeSeriesDataHourly.objects.filter(datetime__range=[from_date, today], item=_item_id, connected_realm=_connected_realm_id).order_by('datetime')
        return tsd_list


    def getRealmItemLastData(self, _item_id, _connected_realm_id):
        return ItemRealmTimeSeriesDataHourly.objects.filter(item=_item_id, connected_realm=_connected_realm_id).order_by('-datetime').first()
