import logging, urllib.error
from labels import labels
from model_item.models import Item
from model_item.item_service import ItemService
from model_item.serializer import ItemSerilizer
from db_updater.src.updater_interface import UpdaterInterface
from model_auction.models import Auction
from django.db import connection

# Init the logger instance
log = logging.getLogger('item_update')
label = labels.DBU

class ItemAPIUpdater(UpdaterInterface):

    def getItemApiLink(self, itemId):
        return 'https://'+self.region+'.api.battle.net/wow/item/'+itemId+'?locale='+self.getLocale()+'&apikey='+self.getApiKey()

    def insert(self, itemId):
        if self.isRegionValid():
            url = self.getItemApiLink(itemId)
            newItem = None
            try:
                newItem = self.getApiLinkData(url)
            except urllib.error.URLError as e:
                log.error(label['@DBU7'] % url)
                log.error(e)
            if newItem != None:
                if self.insertItemToDatabase(newItem):
                    # success
                    return True
                else:
                    # error
                    pass
        else:
            log.error(label['@DBU6'])
        return False

    def insertItemToDatabase(self, json_data):
        if 'id' in json_data:
            item = Item()

            item.itemId = int(json_data['id'])
            if 'name' in json_data:
                item.name = json_data['name']
            if 'sellPrice' in json_data:
                item.sellPrice = json_data['sellPrice']
            if 'icon' in json_data:
                item.icon = json_data['icon']
            if 'quality' in json_data:
                item.quality = json_data['quality']
            if 'itemClass' in json_data:
                item.itemClass = json_data['itemClass']
            if 'itemSubClass' in json_data:
                item.itemSubClass = json_data['itemSubClass']
            if 'inventoryType' in json_data:
                item.inventoryType = json_data['inventoryType']

            item.save()
            return True
            # data = {
            #     'itemId': itemId,
            #     'name': name,
            #     'sellPrice': sellPrice,
            #     'icon': icon,
            #     'quality': quality,
            #     'itemClass': itemClass,
            #     'itemSubClass': itemSubClass,
            #     'inventoryType': inventoryType
            # }

            # serializer = ItemSerilizer(data=data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return True
            # else:
            #     log.debug(data)
            #     log.error(label['@DBU9'] % 'Items')
        return False

    def main(self):
        if self.isRegionValid():
            #items = AuctionEu.objects.distinct('item')
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT `item` FROM %s" % Auction._meta.db_table)

            if cursor:
                auctionItems = cursor.fetchall()
                item_service = ItemService()

                itemsIds = item_service.getItemList()
                created = 0
                log.debug('Inserting...')
                for auctionItem in auctionItems:
                    if not auctionItem[0] in itemsIds:
                        # Insert
                        url = self.getItemApiLink(str(auctionItem[0]))
                        newItem = None
                        try:
                            newItem = self.getApiLinkData(url)
                        except urllib.error.URLError as e:
                            log.error(label['@DBU7'] % url)
                            log.error(e)
                        if newItem != None:
                            if item_service.insert(newItem):
                                created += 1
                            else:
                                # error
                                pass
                    else:
                        pass
                        # Item exist in database
                log.info('Inserted %s items' % str(created))
        else:
            log.error(label['@DBU6'])