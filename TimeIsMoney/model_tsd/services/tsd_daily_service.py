import datetime, decimal
from ..models import ItemRealmTimeSeriesDataDaily
from .tsd_hourly_service import TSDHourlyService
from django.db import connection
from contextlib import closing
from model_item.item_service import ItemService
from model_realm.services import RealmService

class TSDDailyService:

    def batchInsert(self, _data):
        # [date, min_marketprice, max_marketprice, avg_marketprice, min_price, max_price, avg_price, open_mp, end_mp, min_quan, max_quan, avg_quan, connected_realm_id, item_id]
        pre_sql = 'INSERT INTO %s (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) VALUES {}' \
                  % (ItemRealmTimeSeriesDataDaily._meta.db_table,
                     'date',
                     'min_market_price',
                     'max_market_price',
                     'avg_market_price',
                     'min_price',
                     'max_price',
                     'avg_price',
                     'open_market_price',
                     'end_market_price',
                     'min_quantity',
                     'max_quantity',
                     'avg_quantity',
                     'connected_realm_id',
                     'item_id')
        sql = pre_sql.format(
            ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'] * len(_data))
        )
        params = []
        for each in _data:
            params.extend([
                each['date'],
                each['min_market_price'],
                each['max_market_price'],
                each['avg_market_price'],
                each['min_price'],
                each['max_price'],
                each['avg_price'],
                each['open_market_price'],
                each['end_market_price'],
                each['min_quantity'],
                each['max_quantity'],
                each['avg_quantity'],
                each['connected_realm_id'],
                each['item_id'],
            ])
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql, params)

    def create(self, _item_id, _hourly, _day, _connected_realm_id):
        # [today, min_marketprice, max_marketprice, avg_marketprice, min_price, max_price, avg_price, open_mp, end_mp, min_quan, max_quan, avg_quan, cr_id, item_id
        min_market_price = 0
        max_market_price = 0
        avg_market_price = 0
        min_price = 0
        max_price = 0
        avg_price = 0
        open_market_price = 0
        end_market_price = 0
        min_quantity = 0
        max_quantity = 0
        avg_quantity = 0

        market_price_list = []
        quantity_list = []
        avg_price_list = []
        min_price_list = []
        max_price_list = []

        open_time = False
        end_time = False
        for tsd in _hourly:
            if not open_time and not end_time:
                open_time = tsd.datetime
                end_time = tsd.datetime
            if tsd.datetime <= open_time:
                open_time = tsd.datetime
                open_market_price = tsd.market_price
            if tsd.datetime >= end_time:
                end_time = tsd.datetime
                end_market_price = tsd.market_price
            if tsd.market_price != 0:
                market_price_list.append(tsd.market_price)
            if tsd.quantity != 0:
                quantity_list.append(tsd.quantity)
            if tsd.avg_price != 0:
                avg_price_list.append(tsd.avg_price)
            if tsd.avg_price != 0:
                avg_price_list.append(tsd.avg_price)
            if tsd.max_price != 0:
                max_price_list.append(tsd.max_price)
            if tsd.min_price != 0:
                min_price_list.append(tsd.min_price)
        if len(market_price_list) > 0:
            min_market_price = min(market_price_list)
            max_market_price = max(market_price_list)
            avg_market_price = round(sum(market_price_list)/len(market_price_list), 4)
        if len(min_price_list) > 0:
            min_price = min(min_price_list)
        if len(max_price_list) > 0:
            max_price = max(max_price_list)
        if len(avg_price_list) > 0:
            avg_price = round(sum(avg_price_list)/len(avg_price_list), 4)
        if len(quantity_list) > 0:
            min_quantity = min(quantity_list)
            max_quantity = max(quantity_list)
            avg_quantity = int(sum(quantity_list)/len(quantity_list))

        return {"date": _day,
                "min_market_price": min_market_price,
                "max_market_price": max_market_price,
                "avg_market_price": avg_market_price,
                "min_price": min_price,
                "max_price": max_price,
                "avg_price": avg_price,
                "open_market_price": open_market_price,
                "end_market_price": end_market_price,
                "min_quantity": min_quantity,
                "max_quantity": max_quantity,
                "avg_quantity": avg_quantity,
                "connected_realm_id": _connected_realm_id,
                "item_id": _item_id}

    # def createOrUpdate(self, _item, _connected_realm, _data):
    #     today = datetime.date.today()
    #     tsd_hourly_service = TSDHourlyService()
    #     daily_exist = True
    #     avg_market_price_sum = 0
    #     tsd_len_mp = 0
    #     avg_price_sum = 0
    #     tsd_len_avg =0
    #     avg_quantity_sum = 0
    #     tsd_len_quan = 0
    #     tsd_hourly_set = tsd_hourly_service.getRealmDailyData(_item.id, _connected_realm.id, today)
    #     for tsd_hourly in tsd_hourly_set:
    #         if tsd_hourly.market_price > 0:
    #             avg_market_price_sum += tsd_hourly.market_price
    #             tsd_len_mp += 1
    #         if tsd_hourly.avg_price > 0:
    #             avg_price_sum += tsd_hourly.avg_price
    #             tsd_len_avg += 1
    #         if tsd_hourly.quantity > 0:
    #             avg_quantity_sum += tsd_hourly.quantity
    #             tsd_len_quan += 1
    #     if _data['market_price'] > 0:
    #         avg_market_price_sum += decimal.Decimal(_data['market_price'])
    #         tsd_len_mp += 1
    #     if _data['avg_price'] > 0:
    #         avg_price_sum += decimal.Decimal(_data['avg_price'])
    #         tsd_len_avg += 1
    #     if _data['quantity'] > 0:
    #         avg_quantity_sum += _data['quantity']
    #         tsd_len_quan += 1
    #
    #     tsd = self.getTSDDaily(today, _item.id, _connected_realm.id)
    #     if not tsd:
    #         daily_exist = False
    #         tsd = ItemRealmTimeSeriesDataDaily()
    #     if not daily_exist:
    #         tsd.date = today
    #     if not daily_exist or tsd.min_market_price == 0 or tsd.min_market_price > _data['market_price']:
    #         tsd.min_market_price = _data['market_price']
    #     if tsd.max_market_price < _data['market_price']:
    #         tsd.max_market_price = _data['market_price']
    #
    #     if daily_exist:
    #         if tsd_len_mp > 0:
    #             tsd.avg_market_price = round(avg_market_price_sum/tsd_len_mp, 4)
    #     else:
    #         tsd.avg_market_price = _data['market_price']
    #
    #     if not daily_exist or tsd.min_price == 0 or tsd.min_price > _data['min_price']:
    #         tsd.min_price = _data['min_price']
    #     if tsd.max_price < _data['max_price']:
    #         tsd.max_price = _data['max_price']
    #
    #     if daily_exist:
    #         if tsd_len_avg > 0:
    #             tsd.avg_price = round(avg_price_sum/tsd_len_avg, 4)
    #     else:
    #         tsd.avg_price = _data['avg_price']
    #
    #     if not daily_exist or tsd.open_market_price == 0:
    #         tsd.open_market_price = _data['market_price']
    #     if _data['market_price'] > 0:
    #         tsd.end_market_price = _data['market_price']
    #     if not daily_exist or tsd.min_quantity > _data['quantity']:
    #         tsd.min_quantity = _data['quantity']
    #     if tsd.max_quantity < _data['quantity']:
    #         tsd.max_quantity = _data['quantity']
    #
    #     if daily_exist:
    #         if tsd_len_quan > 0:
    #             tsd.avg_quantity = int(avg_quantity_sum/tsd_len_quan)
    #     else:
    #         tsd.avg_quantity = _data['quantity']
    #
    #     #if tsd.connected_realm is None:
    #     tsd.connected_realm = _connected_realm
    #     #if tsd.item is None:
    #     tsd.item = _item
    #     #if tsd.last_hourly is None:
    #     #tsd.last_hourly = _last_hourly
    #
    #     #tsd.save()
    #     return tsd
    #
    # def getTSDDaily(self, _date, _connected_realm_id):
    #     return ItemRealmTimeSeriesDataDaily.objects.filter(date=_date, connected_realm=_connected_realm_id)

    def getRealmItemChartData(self, _item_id, _connected_realm_id):
        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=365)
        tsd_list = ItemRealmTimeSeriesDataDaily.objects.filter(date__range=[from_date, today], item=_item_id, connected_realm=_connected_realm_id)
        return tsd_list