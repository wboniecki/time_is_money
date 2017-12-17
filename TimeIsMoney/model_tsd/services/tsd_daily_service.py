import datetime
from ..models import ItemRealmTimeSeriesDataDaily
from .tsd_hourly_service import TSDHourlyService
from model_item.item_service import ItemService
from model_realm.services import RealmService

class TSDDailyService:
    def createOrUpdate(self, _item, _connected_realm, _data):
        today = datetime.date.today()
        tsd_hourly_service = TSDHourlyService()
        daily_exist = True
        avg_market_price_sum = 0
        tsd_len_mp = 0
        avg_price_sum = 0
        tsd_len_avg =0
        avg_quantity_sum = 0
        tsd_len_quan = 0
        tsd_hourly_set = tsd_hourly_service.getRealmDailyData(_item.id, _connected_realm.id, today)
        for tsd_hourly in tsd_hourly_set:
            if tsd_hourly.market_price > 0:
                avg_market_price_sum += tsd_hourly.market_price
                tsd_len_mp += 1
            if tsd_hourly.avg_price > 0:
                avg_price_sum += tsd_hourly.avg_price
                tsd_len_avg += 1
            if tsd_hourly.quantity > 0:
                avg_quantity_sum += tsd_hourly.quantity
                tsd_len_quan += 1

        tsd = self._getTSDDaily(today, _item.id, _connected_realm.id)
        if not tsd:
            daily_exist = False
            tsd = ItemRealmTimeSeriesDataDaily()
        if not daily_exist:
            tsd.date = today
        if not daily_exist or tsd.min_market_price == 0 or tsd.min_market_price > _data['market_price']:
            tsd.min_market_price = _data['market_price']
        if tsd.max_market_price < _data['market_price']:
            tsd.max_market_price = _data['market_price']

        if daily_exist:
            if tsd_len_mp > 0:
                tsd.avg_market_price = round(avg_market_price_sum/tsd_len_mp, 4)
        else:
            tsd.avg_market_price = _data['market_price']

        if not daily_exist or tsd.min_price == 0 or tsd.min_price > _data['min_price']:
            tsd.min_price = _data['min_price']
        if tsd.max_price < _data['max_price']:
            tsd.max_price = _data['max_price']

        if daily_exist:
            if tsd_len_avg > 0:
                tsd.avg_price = round(avg_price_sum/tsd_len_avg, 4)
        else:
            tsd.avg_price = _data['avg_price']

        if not daily_exist or tsd.open_market_price == 0:
            tsd.open_market_price = _data['market_price']
        if _data['market_price'] > 0:
            tsd.end_market_price = _data['market_price']
        if not daily_exist or tsd.min_quantity > _data['quantity']:
            tsd.min_quantity = _data['quantity']
        if tsd.max_quantity < _data['quantity']:
            tsd.max_quantity = _data['quantity']

        if daily_exist:
            if tsd_len_quan > 0:
                tsd.avg_quantity = int(avg_quantity_sum/tsd_len_quan)
        else:
            tsd.avg_quantity = _data['quantity']

        #if tsd.connected_realm is None:
        tsd.connected_realm = _connected_realm
        #if tsd.item is None:
        tsd.item = _item
        #if tsd.last_hourly is None:
        #tsd.last_hourly = _last_hourly

        #tsd.save()
        return tsd

    def _getTSDDaily(self, _date, _dbitem_id, _connected_realm_id):
        tsd = ItemRealmTimeSeriesDataDaily.objects.filter(date=_date, item=_dbitem_id, connected_realm=_connected_realm_id).first()
        if tsd:
            return tsd
        return False