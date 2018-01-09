import logging
import multiprocessing
import datetime
from labels import labels
#from django.db import transaction
from model_auction.auction_service import AuctionService
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

    def dailyMain(self):
        # Daily calculated always next day (ex. date from 10.01 calc 11.01)
        log.debug(label['@DBU1'])
        log.debug(label['@DBU24'] % 'TSD DAILY')
        today = datetime.date.today()
        yesterday = today-datetime.timedelta(days=1)
        #print(yesterday)
        realm_service = RealmService()
        tsd_hourly_service = TSDHourlyService()
        tsd_daily_service = TSDDailyService()
        connected_realms_tab = realm_service.getActiveRealmsConnectedRealmId()
        total_bulk = 0
        for connected_realms_id in connected_realms_tab:
            tsd_hourly = tsd_hourly_service.getRealmAllDailyData(connected_realms_id, yesterday)
            if not tsd_hourly:
                print("Warning! No hourly TSD in db.")
                continue
            tsd_hourly_list = []
            tsd_hourly_item_maplist = []
            for each in tsd_hourly:
                if not each.item_id in tsd_hourly_item_maplist:
                    tsd_hourly_item_maplist.append(each.item_id)
                    item_tsd = [each]
                    tsd_hourly_list.insert(tsd_hourly_item_maplist.index(each.item_id), item_tsd)
                else:
                    tsd_hourly_list[tsd_hourly_item_maplist.index(each.item_id)].append(each)
            result = [tsd_daily_service.create(each, tsd_hourly_list[tsd_hourly_item_maplist.index(each)], yesterday, connected_realms_id) for each in tsd_hourly_item_maplist]
            result_bulk = int(len(result) / 500)
            result_bulk_list = [[] for _ in range(result_bulk)]
            for i, each in enumerate(result):
                result_bulk_list[i % result_bulk].append(each)
            for result_bulk_sublist in result_bulk_list:
                total_bulk += len(result_bulk_sublist)
                tsd_daily_service.batchInsert(result_bulk_sublist)
        log.debug(label['@DBU38'] % ('TSD DAILY', str(total_bulk)))
        log.debug(label['@DBU2'])


    def hourlyMain(self):
        log.debug(label['@DBU1'])
        log.debug(label['@DBU24'] % 'TSD HOURLY')
        realm_service = RealmService()
        connected_realm_service = ConnectedRealmService()
        item_service = ItemService()
        auction_service = AuctionService()
        tsd_hourly_service = TSDHourlyService()
        connected_realms_tab = realm_service.getActiveRealmsConnectedRealmId()
        # Get itemId price list map
        item_list = item_service.getAllItems()
        # IMPORTANT! BELOW SET MAX ALLOW AMOUT OF PROCCESS (depending on CPU cores)
        max_proc = 3
        item_proc_list = [[] for _ in range(max_proc)]
        for i, item in enumerate(item_list):
            item_proc_list[i % max_proc].append(item)
        total = 0
        total_bulk = 0
        for connected_realms_id in connected_realms_tab:
            out_q = multiprocessing.Queue()
            realms = realm_service.getRealmNamesByConnectedRealmId(connected_realms_id)
            auctions = []
            for realm in realms:
                auctions += auction_service.getAllRealmActiveAuctionsList(realm)
            if len(auctions) > 0:
                calculation = Calculation(auctions)
                log.debug(label['@DBU39'] % str(connected_realms_id))
                log.debug(label['@DBU41'] % str(len(auctions)))
                connected_realm = connected_realm_service.getConnectedRealm(connected_realms_id)
                calculations = [multiprocessing.Process(target=self.hourlyProcCalculation, args=(item_sublist, calculation, out_q)) for item_sublist in item_proc_list]
                for p in calculations:
                    p.start()
                result = []
                for i in range(max_proc):
                    result += out_q.get()
                for p in calculations:
                    p.join()

                result_bulk = int(len(result)/500)
                result_bulk_list = [[] for _ in range(result_bulk)]
                for i, each in enumerate(result):
                    result_bulk_list[i % result_bulk].append(each)
                total_bulk = 0
                for result_bulk_sublist in result_bulk_list:
                    total_bulk += len(result_bulk_sublist)
                    tsd_hourly_service.batchInsert(result_bulk_sublist, connected_realm.id)

                if total_bulk != len(item_list):
                    log.warning("Missing %d items in bulk insert" % (len(item_list)-total_bulk))
            else:
                log.warning(label['@DBU41'] % str(len(auctions)))
            log.debug(label['@DBU40'] % str(connected_realms_id))
            total += total_bulk
        log.debug(label['@DBU38'] % ('TSD HOURLY', str(total)))
        log.debug(label['@DBU2'])

    def hourlyProcCalculation(self, items, calculation, out_q):
        calc_table = []
        for item in items:
            item_vendor_sellprice = Utils.unifyPrice(item.sellPrice)
            calc = calculation.calc(item.itemId, item_vendor_sellprice)
            calc_table.append([item, calc])
        out_q.put(calc_table)

    def deleteOldTSD(self):
        log.debug(label['@DBU37'])
        log.debug(label['@DBU35'] % 'TSD Hourly')
        tsd_hourly_service = TSDHourlyService()
        old_date = tsd_hourly_service.deleteOldTSD()
        log.info(label['@DBU36'] % 'TSD Hourly')
        log.info(label['@DBU42'] % old_date)


