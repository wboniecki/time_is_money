from utils.utils import Utils
from .models import Item


class ItemService:

    def getItemByItemId(self, _itemId):
        return Item.objects.filter(itemId=_itemId).first()

    def getItemList(self):
        items = Item.objects.all()
        item_list = []

        for item in items:
            item_list.append(item.itemId)

        return item_list

    def getAllItems(self):
        return Item.objects.all()

    def insert(self, json_data):
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
        return False