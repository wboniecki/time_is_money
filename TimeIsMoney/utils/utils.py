class Utils:

    @staticmethod
    def unifyPrice(_price):
        # price is string we need convert into G,SSCC decimal float format
        hashlist = list(_price)
        if len(hashlist) >= 4:
            hashlist.insert(len(hashlist) - 4, '.')
        else:
            while len(hashlist) < 4:
                hashlist.insert(0, '0')
            hashlist.insert(len(hashlist) - 4, '.')
        return float(''.join(hashlist))

