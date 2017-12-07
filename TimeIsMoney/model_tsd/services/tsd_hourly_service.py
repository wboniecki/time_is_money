import datetime
from ..models import ItemRealmTimeSeriesDataHourly


class TSDHourlyService:
    def create(self, _item, _connected_realm, _data):
        tsd_hourly = ItemRealmTimeSeriesDataHourly()
        tsd_hourly.datetime = datetime.datetime.now()
        tsd_hourly.item = _item
        tsd_hourly.connected_realm = _connected_realm
        tsd_hourly.market_price = _data['market_price']
        tsd_hourly.avg_price = _data['avg_price']
        tsd_hourly.quantity = _data['quantity']
        tsd_hourly.standard_deviation = _data['standard_deviation']
        #tsd_hourly.save()
        return tsd_hourly

    def deleteOldTSD(self):
        today =datetime.date.today()
        from_date = datetime.date(2017,1,1)
        to_date = today - datetime.timedelta(days=14)
        tsd_set = ItemRealmTimeSeriesDataHourly.objects.filter(datetime__range=[from_date, to_date])
        counter = 0
        for tsd in tsd_set:
            tsd.delete()
            counter += 1
        return counter

    def getRealmDailyData(self, _item_id, _connected_realm_id, _date):
        return ItemRealmTimeSeriesDataHourly.objects.filter(datetime__date=_date, item=_item_id, connected_realm=_connected_realm_id)
