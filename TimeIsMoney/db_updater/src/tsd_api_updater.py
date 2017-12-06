from model_realm.services import RealmService
from model_item.item_service import ItemService

class TsdAPIUpdater:
    def main(self):
        # TODO: Pobierz mape aktywnych realmów (connected_realm, realms[])
        realm_service = RealmService()
        item_service = ItemService()
        connected_realms_tab = realm_service.getActiveRealmsConnectedRealmId()
        # Get itemId price list map
        #item_list = item_service.getItemList()
        # for item in item_list:
        #     item_sell_price = item_service.getItemSellPrice(item)
        # for connected_realms_id in connected_realms_tab:

