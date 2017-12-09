import math, datetime
from model_auction.auction_service import AuctionService
from model_realm.services.realm_service import RealmService
from utils.utils import Utils


class Calculation:

    def __init__(self, _auctions):
        self.auctions = _auctions
        self.time = datetime.datetime.now()

    def calcAvgPrice(self, _set):
        if len(_set) > 0:
            return round(sum(_set)/len(_set), 4)
        return 0

    def calcStandardDeviation(self, _set):
        avg = self.calcAvgPrice(_set)
        sub_avg_pow_set = []
        for item in _set:
            sub_avg_pow_set.append(round(pow((item-avg),2),4))
        return round(math.sqrt(self.calcAvgPrice(sub_avg_pow_set)), 4)

    def calcMarketPrice(self, _set, _minPrice, _maxPrice):
        market_price_set = []
        for price in _set:
            if price >= _minPrice and price <= _maxPrice:
                market_price_set.append(price)
        #print(_set)
        return self.calcAvgPrice(market_price_set)

    #TODO: Tutaj będa zmiany odnośnie parametrów _itemId, _item_sell_price, _connected_realm_id
    def calc(self, _itemId, _item_sell_price, _connected_realm_id):
        #realm_service = RealmService()
        #auction_service = AuctionService()

        #realms = realm_service.getRealmNamesByConnectedRealmId(_connected_realm_id)
        item_pricelist = []
        for auction in self.auctions:
            # item_pricelist += auction_service.getRealmPriceList(_itemId, realm)
            if auction.item == _itemId:
                quantity = auction.quantity
                price = Utils.unifyPrice(auction.buyout)/quantity
                if price > 0:
                    while quantity > 0:
                        item_pricelist.append(price)
                        quantity -= 1
        if len(item_pricelist) > 0:
            item_pricelist = sorted(item_pricelist)
            standard_deviation = self.calcStandardDeviation(item_pricelist)
            # Get vendor sell price continue if is not None (item exist statement)
            max_set_len = int(len(item_pricelist)*0.3)
            need_set = []
            counter = 0
            prev_price = 0
            # For each price in item_pricelist
            for price in item_pricelist:
                # Up to max_set_len (30% of item_pircelist)
                if counter <= max_set_len:
                    # Proceed only for price higher than vendor item sell price
                    if price > _item_sell_price:
                        # For first valid price set prev_price equal price
                        if counter == 0:
                            prev_price = price
                        # Grab all prices below or equal first half of max_set_len
                        if counter <= int(max_set_len/2):
                            # First half of set (15%)
                            need_set.append(price)
                            prev_price = price
                            counter += 1
                        else:
                            # Second half of set (max 30%)
                            if prev_price + 0.2 * price <= price:
                                # If price is higher than 20% of prev price break
                                break
                            need_set.append(price)
                            prev_price = price
                            counter += 1
                else:
                    break

            min_itemprice = item_pricelist[0]
            max_itemprice = item_pricelist[len(item_pricelist)-1]
            avg = self.calcAvgPrice(need_set)
            mp_standard_deviation = self.calcStandardDeviation(need_set)
            max_price = round(avg+mp_standard_deviation, 4)
            min_price = round(avg-mp_standard_deviation, 4)
            market_price = self.calcMarketPrice(need_set, min_price, max_price)
            if avg > 0 and market_price == 0:
                market_price = avg
            calculations = {
                "market_price": market_price,
                "standard_deviation": standard_deviation,
                "quantity": len(item_pricelist),
                "min_price": min_itemprice,
                "max_price": max_itemprice,
                "avg_price": self.calcAvgPrice(item_pricelist),
                "datetime": self.time
            }
        else:
            calculations = {
                "market_price": 0,
                "standard_deviation": 0,
                "quantity": 0,
                "min_price": 0,
                "max_price": 0,
                "avg_price": 0,
                "datetime": self.time
            }
        return calculations