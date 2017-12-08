import logging
from labels import labels
from django.db import transaction
from model_realm.services import RealmService, ConnectedRealmService
from model_item.item_service import ItemService
from model_tsd.calculation import Calculation
from model_tsd.services.tsd_daily_service import TSDDailyService
from model_tsd.services.tsd_hourly_service import TSDHourlyService
from utils.utils import Utils

# Init the logger instance
log = logging.getLogger('tsd_update')
label = labels.DBU

class TsdAPIUpdater:

    def commit_tsd_objects(self, _object_list):
        with transaction.atomic():
            for tsd in _object_list:
                tsd.save()

    def main(self):
        log.debug(label['@DBU1'])
        log.debug(label['@DBU24'] % 'TSD HOURLY')
        realm_service = RealmService()
        connected_realm_service = ConnectedRealmService()
        item_service = ItemService()
        calculation = Calculation()
        tsd_daily_service = TSDDailyService()
        tsd_hourly_service = TSDHourlyService()

        connected_realms_tab = realm_service.getActiveRealmsConnectedRealmId()
        # Get itemId price list map
        item_list = item_service.getAllItems()
        counter = 0
        total = 0
        tsd_hourly_objects = []
        tsd_daily_objects = []
        for connected_realms_id in connected_realms_tab:
            log.debug(label['@DBU39'] % str(connected_realms_id))
            for item in item_list:
                item_vendor_sellprice = Utils.unifyPrice(item.sellPrice)
                connected_realm = connected_realm_service.getConnectedRealm(connected_realms_id)
                calc = calculation.calc(item.itemId, item_vendor_sellprice, connected_realms_id)
                tsd_hourly = tsd_hourly_service.create(item, connected_realm, calc)
                tsd_hourly_objects.append(tsd_hourly)
                tsd_daily_objects.append(tsd_daily_service.createOrUpdate(item, connected_realm, calc))
                if counter > 1000:
                    counter = 0
                    self.commit_tsd_objects(tsd_hourly_objects)
                    tsd_hourly_objects = []
                    self.commit_tsd_objects(tsd_daily_objects)
                    tsd_daily_objects = []
                counter += 1
                total += 1
            self.commit_tsd_objects(tsd_hourly_objects)
            self.commit_tsd_objects(tsd_daily_objects)
            log.debug(label['@DBU40'] % str(connected_realms_id))
        log.debug(label['@DBU38'] % ('TSD HOURLY', str(counter)))
        log.debug(label['@DBU2'])


    def deleteOldTSD(self):
        log.debug(label['@DBU37'])
        log.debug(label['@DBU35'] % 'TSD Hourly')
        tsd_hourly_service = TSDHourlyService()
        deleted = tsd_hourly_service.deleteOldTSD()
        log.info(label['@DBU36'] % 'TSD Hourly')


