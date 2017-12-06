from model_realm.services import RealmService, ConnectedRealmService
from model_item.item_service import ItemService
from model_tsd.calculation import Calculation
from model_tsd.services.tsd_daily_service import TSDDailyService
from model_tsd.services.tsd_hourly_service import TSDHourlyService
from utils.utils import Utils

class TsdAPIUpdater:
    def main(self):
        # TODO: Pobierz mape aktywnych realmów (connected_realm, realms[])
        realm_service = RealmService()
        connected_realm_service = ConnectedRealmService()
        item_service = ItemService()
        calculation = Calculation()
        tsd_daily_service = TSDDailyService()
        tsd_hourly_service = TSDHourlyService()

        connected_realms_tab = realm_service.getActiveRealmsConnectedRealmId()
        # Get itemId price list map
        item_list = item_service.getAllItems()
        #print(item_price_list)
        for connected_realms_id in connected_realms_tab:
            for item in item_list:
                item_vendor_sellprice = Utils.unifyPrice(item.sellPrice)
                connected_realm = connected_realm_service.getConnectedRealm(connected_realms_id)
                calc = calculation.calc(item.itemId, item_vendor_sellprice, connected_realms_id)
                tsd_hourly = tsd_hourly_service.create(item, connected_realm, calc)
                tsd_daily_service.createOrUpdate(item, connected_realm, tsd_hourly, calc)
        #item_list = item_service.getItemList()
        # for item in item_list:
        #     item_sell_price = item_service.getItemSellPrice(item)


