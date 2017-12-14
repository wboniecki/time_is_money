from model_auction.auction_service import AuctionService
from model_item.item_service import ItemService
from utils.utils import Utils
from .tsd_calculation import TSDCalculation
from .calculation import Calculation
import datetime

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
        for item in items:
            item_vendor_sellprice = Utils.unifyPrice(item.sellPrice)
            #print(item.itemId)
            calculation = calc.calc(item.itemId, item_vendor_sellprice)
        stop = datetime.datetime.now()
        print("STOP NUMPY CALC: %s" % stop.time())
        duration = (stop - start).total_seconds()
        print("TOTAL NUMPY CALC: %s" % duration)

        calc = Calculation(auctions)
        start = datetime.datetime.now()
        print("START OLD CALC: %s" % start.time())
        for item in items:
            item_vendor_sellprice = Utils.unifyPrice(item.sellPrice)
            calculation = calc.calc(item.itemId, item_vendor_sellprice, 44)
        stop = datetime.datetime.now()
        print("STOP OLD CALC: %s" % stop.time())
        duration = (stop - start).total_seconds()
        print("TOTAL OLD CALC: %s" % duration)
        print("--------------------------")