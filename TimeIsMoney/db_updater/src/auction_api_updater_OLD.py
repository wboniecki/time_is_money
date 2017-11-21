'''
wboniecki 2017-11-12
Auction service class for updater, contains methods for update Auction (Eu or Us) table in database.
Implements UpdaterInterface class.
'''
import logging, urllib.error, datetime
from labels import labels
from db_updater.src.updater_interface import UpdaterInterface
from model_auction.serializer import AuctionEuSerializer, AuctionUsSerializer
from model_auction.models import AuctionEu, AuctionUs
from model_realm.models import Realm

from django.db import connection

# Init the logger instance
log = logging.getLogger('auction_update')
label = labels.DBU

class AuctionService(UpdaterInterface):

    def create(self):
        if self.isRegionValid():
            # Make sure the db table is empty, make truncate
            auctions = self.getAllAuctions()
            if not auctions:
                self.main('create')
            else:
                # truncate table first
                log.warning(label['@DBU12'] % self.region)
                if self.truncateAllAunctions():
                    # Truncate complete call create method again
                    self.create()
                else:
                    # Errors
                    log.error(label['@DBU13'] % self.region)
        else:
            log.error(label['@DBU6'])

    def getRealmAuctionsApiLinkData(self, url):
        data = None
        try:
            data = self.getApiLinkData(url)
            return data['files'][0]
        except urllib.error.URLError as e:
            log.error(label['@DBU7'] % url)
            log.error(e)
        return data

    def generateRealmAuctionsApiLink(self, realm):
        return 'https://'+realm.region+'.api.battle.net/wow/auction/data/'+realm.slug+'?locale='+realm.locale+'&apikey='+self.getApiKey()

    def getAllAuctions(self):
        if self.region == 'eu':
            return AuctionEu.objects.all()
        if self.region == 'us':
            return AuctionUs.objects.all()

    def getCurrentAuctions(self, connectedRealms):
        currentAuctions = []
        for connectedRealm in connectedRealms:
            if self.region == 'eu':
                currentAuctions += AuctionEu.objects.filter(ownerRealm=connectedRealm['name'], isActive=1)
            if self.region == 'us':
                currentAuctions += AuctionUs.objects.filter(ownerRealm=connectedRealm['name'], isActive=1)

        return currentAuctions

    def insertNewAuction(self, auction):
        if self.region == 'eu':
            serializer = AuctionEuSerializer(data=auction)
        elif self.region == 'us':
            serializer = AuctionUsSerializer(data=auction)
        else:
            return False

        if serializer.is_valid():
            serializer.save()
            return True
        else:
            log.error(label['@DBU14'] % auction)
        return False

    def isRealmNotUpdate(self, realm, lastModified):
        return str(realm.lastModified) != str(lastModified)

    def main(self, action):
        log.debug(label['@DBU1']) #Begin
        realmsSlugDone = [] #Contains all done realms
        # Retrieve all active realms in defined region
        realms = Realm.objects.filter(isActive=1, region=self.region)
        if not realms:
            # Error when no realms in database
            log.error(label['@DBU15'] % self.region)
        else:
            # For each realm in list proceed to create or update auctions
            for realm in realms:
                if realm.slug in realmsSlugDone:
                    # Realm already done
                    log.debug(label['@DBU16'] % realm.name)
                else:
                    # Realm is not in the done list
                    log.debug(label['@DBU17'] % realm.name)
                    realmCreated = 0
                    realmDeprecated = 0
                    realmUpdated = 0
                    realmTotal = 0
                    # Retrieve url auction api
                    url = self.generateRealmAuctionsApiLink(realm)
                    apiData = self.getRealmAuctionsApiLinkData(url)
                    if apiData != None:
                        # Data in api exist continue
                        lastModified = apiData['lastModified'] #Save last modified
                        auctionUrl = apiData['url'] #Save auctions url
                        # TODO: TUTAJ
                        if action == 'create':
                            # CREATE
                            # No necessary to check is realm up to date, table is truncated
                            auctionJSON = self.parseAuctionJson(auctionUrl)
                            if auctionJSON != None:
                                # Continue create with auction json
                                connectedRealms = auctionJSON['realms']
                                auctions = auctionJSON['auctions'] #Save all auctions
                                log.debug(label['@DBU18'] % realm.name)
                                for auction in auctions:
                                    realmTotal += 1
                                    if self.insertNewAuction(auction):
                                        realmCreated += 1
                                    else:
                                        # Error when inserting new auction
                                        log.error(label['@DBU19'] % realm.name)
                                for connectedRealm in connectedRealms:
                                    # After inserting, update a connected realms
                                    if self.updateConnectedRealm(connectedRealm, lastModified):
                                        realmsSlugDone.append(connectedRealm['slug'])
                                    else:
                                        # Error when updating a relms
                                        log.error(
                                            label['@DBU20'] % connectedRealm[
                                                'name'])
                                # Summary info
                                log.debug(label['@DBU21'] % realm.name)
                                log.info(label['@DBU22'] % (realm.name, str(realmTotal), str(realmUpdated), str(realmCreated), str(realmDeprecated)))
                            else:
                                # Auction JSON is None
                                log.error(label['@DBU23'] % realm.name)
                        elif action == 'update':
                            # UPDATE
                            # Mandatory to check if Realm is up to date
                            if self.isRealmNotUpdate(realm, lastModified):
                                # Realm is not up to date, continue - updating
                                auctionJSON = self.parseAuctionJson(auctionUrl)
                                if auctionJSON != None:
                                    # Continue update with auction json
                                    connectedRealms = auctionJSON['realms']
                                    auctions = auctionJSON['auctions'] #Save all auctions
                                    currentAuctions = self.getCurrentAuctions(connectedRealms) # Get current, active auction objects in database
                                    currentAuctionsAuc = []
                                    # Need to store auction num to check if exist in JSON
                                    for currentAuction in currentAuctions:
                                        currentAuctionsAuc.append(currentAuction.auc)
                                    log.debug(label['@DBU24'] % realm.name)
                                    for auction in auctions:
                                        realmTotal += 1
                                        if auction['auc'] in currentAuctionsAuc:
                                            # Update existing
                                            if self.updateAuction(auction):
                                                realmUpdated += 1
                                                currentAuctionsAuc.remove(auction['auc'])
                                        else:
                                            # Insert new one
                                            if self.insertNewAuction(auction):
                                                realmCreated += 1
                                            else:
                                                log.error(label['@DBU19'] % realm.name)

                                    # All left in currnetAuctionsAuc number is deprecated - not existing in JSON
                                    # Database must be updated to set isActive in this auctions to 0
                                    for currentAuction in currentAuctions:
                                        if currentAuction.auc in currentAuctionsAuc:
                                            # Change isActive to 0
                                            currentAuction.isActive = 0
                                            currentAuction.save()
                                            realmDeprecated += 1

                                    # After updating, update a connected realms
                                    for connectedRealm in connectedRealms:
                                        if self.updateConnectedRealm(connectedRealm, lastModified):
                                            realmsSlugDone.append(connectedRealm['slug'])
                                        else:
                                            log.error(label['@DBU20'] % connectedRealm['name'])

                                    # Summary info
                                    log.debug(label['@DBU21'] % realm.name)
                                    log.info(label['@DBU22'] % (
                                    realm.name, str(realmTotal), str(realmUpdated), str(realmCreated),
                                    str(realmDeprecated)))
                                else:
                                    # Auction JSON is None
                                    log.error(label['@DBU25'] % realm.name)
                            else:
                                # Realm is up to date
                                log.debug(label['@DBU26'] % realm.name)
                        else:
                            # Specified action is not valid
                            log.critical(label['@DBU27'] % action)
                    else:
                        # None of realm api link data
                        log.error(label['@DBU28'] % (realm.name, url))

        log.debug(label['@DBU2']) #End

    def parseAuctionJson(self, url):
        data = None
        try:
            data = self.getApiLinkData(url)
        except urllib.error.URLError as e:
            log.error(label['@DBU7'] % url)
            log.error(e)
        return data

    def truncateAllAunctions(self):
        cursor = connection.cursor()
        if self.region == 'eu':
            log.debug(label['@DBU11'] % AuctionEu._meta.db_table)
            cursor.execute("TRUNCATE TABLE %s" % AuctionEu._meta.db_table)
            if cursor:
                return True
        if self.region == 'us':
            log.debug(label['@DBU11'] % AuctionUs._meta.db_table)
            cursor.execute("TRUNCATE TABLE %s" % AuctionUs._meta.db_table)
            return True

        return False

    def update(self):
        if self.isRegionValid():
            self.main('update')
        else:
            log.error(label['@DBU6'])

    def updateAuction(self, oldAuction):
        auction = AuctionEu.objects.get(ownerRealm=oldAuction['ownerRealm'],
                                              auc=oldAuction['auc'])
        if not auction:
            return False
        else:
            if auction.bid != oldAuction['bid']:
                auction.bid = oldAuction['bid']
            if auction.buyout != oldAuction['buyout']:
                auction.buyout = oldAuction['buyout']
            if auction.quantity != oldAuction['quantity']:
                auction.quantity = oldAuction['quantity']
            if auction.timeLeft != oldAuction['timeLeft']:
                auction.timeLeft = oldAuction['timeLeft']
            auction.save()
            return True

    def updateConnectedRealm(self, connectedRealm, lastModified):
        realm = Realm.objects.get(name=connectedRealm['name'], slug=connectedRealm['slug'],
                                       region=self.region)
        if not realm:
            return False
        else:
            realm.lastModified = lastModified
            realm.dateModified = datetime.datetime.now()
            realm.save()
            return True