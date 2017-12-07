import datetime
from ..models import ItemRealmTimeSeriesDataDaily
from .tsd_hourly_service import TSDHourlyService
from model_item.item_service import ItemService
from model_realm.services import RealmService

class TSDDailyService:
    def createOrUpdate(self, _item, _connected_realm, _last_hourly, _data):
        today = datetime.date.today()
        tsd_hourly_service = TSDHourlyService()
        avg_market_price_sum = 0
        avg_price_sum = 0
        avg_quantity_sum = 0
        tsd_hourly_set = tsd_hourly_service.getRealmDailyData(_item.id, _connected_realm.id, today)
        for tsd_hourly in tsd_hourly_set:
            avg_market_price_sum += tsd_hourly.market_price
            avg_price_sum += tsd_hourly.avg_price
            avg_quantity_sum += tsd_hourly.quantity

        tsd = self._getTSDDaily(today, _item.id, _connected_realm.id)
        if not tsd:
            tsd = ItemRealmTimeSeriesDataDaily()
        if not tsd.date:
            tsd.date = today
        if not tsd.min_market_price or tsd.min_market_price > _data['market_price']:
            tsd.min_market_price = _data['market_price']
        if tsd.max_market_price < _data['market_price']:
            tsd.max_market_price = _data['market_price']
        tsd.avg_market_price = round(avg_market_price_sum/len(tsd_hourly_set), 4)
        if not tsd.min_price or tsd.min_price > _data['min_price']:
            tsd.min_price = _data['min_price']
        if tsd.max_price < _data['max_price']:
            tsd.max_price = _data['max_price']
        tsd.avg_price = round(avg_price_sum/len(tsd_hourly_set), 4)
        if not tsd.open_market_price:
            tsd.open_market_price = _data['market_price']
        tsd.end_market_price = _data['market_price']
        if not tsd.min_quantity or tsd.min_quantity > _data['quantity']:
            tsd.min_quantity = _data['quantity']
        if tsd.max_quantity < _data['quantity']:
            tsd.max_quantity = _data['quantity']
        tsd.avg_quantity = round(avg_quantity_sum/len(tsd_hourly_set), 4)
        #if tsd.connected_realm is None:
        tsd.connected_realm = _connected_realm
        #if tsd.item is None:
        tsd.item = _item
        #if tsd.last_hourly is None:
        tsd.last_hourly = _last_hourly

        #tsd.save()
        return tsd

    def _getTSDDaily(self, _date, _dbitem_id, _connected_realm_id):
        tsd = ItemRealmTimeSeriesDataDaily.objects.filter(date=_date, item=_dbitem_id, connected_realm=_connected_realm_id).first()
        if tsd:
            return tsd
        return False