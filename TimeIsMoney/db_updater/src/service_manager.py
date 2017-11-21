from db_updater.src.realm_api_updater import RealmAPIUpdater
from db_updater.src.auction_api_updater import AuctionAPIUpdater
from db_updater.src.item_api_updater import ItemAPIUpdater

def createOrUpdateRealms(region):
    RealmAPIUpdater(region).main()

def updateConnectedRealm(region):
    RealmAPIUpdater(region).main()

def createAllAuctions(region):
    #AuctionService(region).create()
    AuctionAPIUpdater(region).main()

def updateAllAuctions(region):
    AuctionAPIUpdater(region).main()
    #AuctionService(region).update()

# TODO: test purpose
def createOrUpdateItems(region):
    ItemAPIUpdater(region).main()

# def insertItem(region, itemId):
#     return ItemService(region).insert(itemId)