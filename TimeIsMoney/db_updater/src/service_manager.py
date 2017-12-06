from db_updater.src.realm_api_updater import RealmAPIUpdater
from db_updater.src.auction_api_updater import AuctionAPIUpdater
from db_updater.src.item_api_updater import ItemAPIUpdater
from db_updater.src.tsd_api_updater import TsdAPIUpdater

def createOrUpdateRealms(region):
    RealmAPIUpdater(region).main()

def deleteOldAuctions(region):
    AuctionAPIUpdater(region).deleteOldAuctions()

def updateAllAuctions(region):
    AuctionAPIUpdater(region).main()

def createOrUpdateItems(region):
    ItemAPIUpdater(region).main()

def tsdUpdater():
    TsdAPIUpdater().main()
