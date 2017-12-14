import datetime
import numpy as np

from utils.utils import Utils

class TSDCalculation:

    def __init__(self, auctions):
        self.auctions = auctions
        self.time = datetime.datetime.now()

    def calc(self, itemId, item_sell_price):
        item_pricelist = []
        for auction in self.auctions:
            if auction.item == itemId:
                quantity = auction.quantity
                price = Utils.unifyPrice(auction.buyout)/quantity
                if price > 0:
                    while quantity > 0:
                        item_pricelist.append(price)
                        quantity -= 1
        if len(item_pricelist) > 0:
            item_pricearray = np.array(item_pricelist)
            item_pricearray = np.sort(item_pricearray)
            # Get vendor sell price continue if is not None (item exist statement)
            max_set_len = int(item_pricearray.size*0.3)
            if max_set_len > 1:
                maxneed_setarray = item_pricearray[:max_set_len]
                need_setarray = maxneed_setarray[:int(maxneed_setarray.size*0.5)]
                prev_price = np.amax(need_setarray)
                secondhalf_needlist = []
                for price in np.nditer(maxneed_setarray[int(maxneed_setarray.size*0.5):]):
                    if prev_price + 0.2 * price <= price:
                        # If price is higher than 20% of prev price break
                        break
                    secondhalf_needlist.append(price)
                    prev_price = price
                need_setarray = np.append(need_setarray, np.array(secondhalf_needlist))
            else:
                need_setarray = item_pricearray
            min_itemprice = np.amin(item_pricearray)
            max_itemprice = np.amax(item_pricearray)
            standard_deviation = np.around(np.std(item_pricearray), decimals=4)
            avg_price = np.around(np.average(item_pricearray), decimals=4)
            avg = np.around(np.average(need_setarray), decimals=4)
            mp_standard_deviation = np.around(np.std(need_setarray), decimals=4)
            max_price = np.around(avg+mp_standard_deviation, decimals=4)
            min_price = np.around(avg-mp_standard_deviation, decimals=4)
            market_pricearray = need_setarray[np.where(need_setarray >= min_price)]
            market_pricearray = market_pricearray[np.where(market_pricearray <= max_price)]
            if np.array_equal(market_pricearray, need_setarray):
                market_price = avg
            else:
                if avg > 0 and market_pricearray.size == 0:
                    market_price = avg
                elif avg == 0:
                    market_price = item_sell_price
                else:
                    market_price = np.around(np.average(market_pricearray), decimals=4)
            calculations = {
                "market_price": format(market_price, '.4f'),
                "standard_deviation": format(standard_deviation, '.4f'),
                "quantity": item_pricearray.size,
                "min_price": format(min_itemprice, '.4f'),
                "max_price": format(max_itemprice, '.4f'),
                "avg_price": format(avg_price, '.4f'),
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
