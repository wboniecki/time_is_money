from .models import Auction
from .serializer import AuctionSerializer

class AuctionService:

    def crate(self, auction):
        serializer = AuctionSerializer(data=auction)

        if serializer.is_valid():
            serializer.save()
            return True

        return False

    def isNotEmpty(self):
        return Auction.objects.all().first()

    def getActiveAuctions(self, connected_realms):
        current_auctions = []
        current_auctions_auc = {}

        for connected_realm in connected_realms:
            current_auctions += Auction.objects.filter(ownerRealm=connected_realm['name'], isActive=1)
        counter = 0
        for current_auction in current_auctions:
            counter += 1
            current_auctions_auc[current_auction.auc] = current_auction
        return current_auctions_auc

    def getCurrentAuctions(self, connected_realms):
        current_auctions = []
        current_auctions_auc = []

        for connected_realm in connected_realms:
            current_auctions += Auction.objects.filter(ownerRealm=connected_realm['name'], isActive=1)
        counter = 0
        for current_auction in current_auctions:
            counter += 1
            current_auctions_auc.append(current_auction.auc)
        return current_auctions_auc

    def unactive(self, _connected_realms, _auc):
        for connected_realm in _connected_realms:
            auction = Auction.objects.filter(ownerRealm=connected_realm['name'], auc=_auc).first()

            if auction:
                auction.isActive = False
                auction.save()
                return True

        return False

    def updateAuction(self, _auc):
        auction = Auction.objects.filter(ownerRealm=_auc['ownerRealm'],
                                         auc=_auc['auc']).first()
        if auction:
            if str(auction.bid) != str(_auc['bid']) or str(auction.buyout) != str(_auc['buyout']) or str(auction.quantity) != str(_auc['quantity']) or str(auction.timeLeft) != str(_auc['timeLeft']):
                # print('bid: '+ str(auction.bid)+' '+str(_auc['bid']))
                # print('bid: ' + str(auction.buyout) + ' ' + str(_auc['buyout']))
                # print('bid: ' + str(auction.quantity) + ' ' + str(_auc['quantity']))
                # print('bid: ' + str(auction.timeLeft) + ' ' + _auc['timeLeft'])
                auction.bid = _auc['bid']
                auction.buyout = _auc['buyout']
                auction.quantity = _auc['quantity']
                auction.timeLeft = _auc['timeLeft']
                auction.save()
                return True

        return False
