from model_auction.auction_service import AuctionService
from model_item.item_service import ItemService
from utils.utils import Utils
from .tsd_calculation import TSDCalculation
from .calculation import Calculation
import datetime
import multiprocessing

def calc_test():
    auction_service = AuctionService()
    auctions = auction_service.getAllRealmActiveAuctionsList("Burning Legion")
    if len(auctions) > 0:
        calc = TSDCalculation(auctions)
        start = datetime.datetime.now()
        print("START: %s" % start.time())
        print(calc.calc(27684, 3.0000))
        stop = datetime.datetime.now()
        print("STOP: %s" % stop.time())
        duration = (stop - start).total_seconds()
        print("TOTAL: %s" % duration)

        calc = Calculation(auctions)
        start = datetime.datetime.now()
        print("START: %s" % start.time())
        print(calc.calc(27684, 3.0000, 44))
        stop = datetime.datetime.now()
        print("STOP: %s" % stop.time())
        duration = (stop - start).total_seconds()
        print("TOTAL: %s" % duration)

        item_service = ItemService()
        items = item_service.getAllItems()
        print("--------------------------")
        print(len(auctions))
        calc = TSDCalculation(auctions)
        start = datetime.datetime.now()
        print("START NUMPY CALC: %s" % start.time())
        max_proc = 6
        item_list = [[] for _ in range(max_proc)]
        for i, item in enumerate(items):
            item_list[i % max_proc].append(item)
        calculations = [multiprocessing.Process(target=single_proc, args=(item_sublist, calc)) for item_sublist in item_list]
        for p in calculations:
            p.start()
        for p in calculations:
            p.join()
        stop = datetime.datetime.now()
        print("STOP NUMPY CALC: %s" % stop.time())
        duration = (stop - start).total_seconds()
        print("TOTAL NUMPY CALC: %s" % duration)
        print(len(calculations))

        calc = Calculation(auctions)
        start = datetime.datetime.now()
        print("START OLD CALC: %s" % start.time())
        max_proc = 6
        item_list = [[] for _ in range(max_proc)]
        for i, item in enumerate(items):
            item_list[i % max_proc].append(item)
        calculations = [multiprocessing.Process(target=single_proc_old, args=(item_sublist, calc)) for item_sublist in item_list]
        for p in calculations:
            p.start()
        for p in calculations:
            p.join()
        stop = datetime.datetime.now()
        print("STOP OLD CALC: %s" % stop.time())
        duration = (stop - start).total_seconds()
        print("TOTAL OLD CALC: %s" % duration)
        print("--------------------------")

def single_proc(items, calc):
    for item in items:
        item_vendor_sellprice = Utils.unifyPrice(item.sellPrice)
        calculation = calc.calc(item.itemId, item_vendor_sellprice)

def single_proc_old(items, calc):
    for item in items:
        item_vendor_sellprice = Utils.unifyPrice(item.sellPrice)
        calculation = calc.calc(item.itemId, item_vendor_sellprice, 44)