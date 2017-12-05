import datetime
from .models import ItemRealmTimeSeriesData
from model_item.item_service import ItemService
from model_realm.services import RealmService

class TSDDailyService:
    def create(self, _itemId, _realmName):
        new_tsd = ItemRealmTimeSeriesData()
        new_tsd.date = datetime.date.today()
        item_service = ItemService()
        new_tsd.item = item_service.getItemDBId(_itemId)
        realm_service = RealmService()
        new_tsd.connected_realm = realm_service.getRealmConnectedRealmId(_realmName)

        new_tsd.save()

    def _getTSD(self, _date, _itemId, _realmName):
        item_service = ItemService()
        realm_service = RealmService()
        return ItemRealmTimeSeriesData.objects.filter(date=_date, item=item_service.getItemDBId(_itemId), connected_realm=realm_service.getRealmConnectedRealmId(_realmName)).first()

    def update(self, _itemId, _realmName, withJSON=False):

        tsd = self._getTSD(datetime.date.today(), _itemId, _realmName)

        if tsd:
            # TSD exist
            if withJSON:
                pass
            else:
                pass

