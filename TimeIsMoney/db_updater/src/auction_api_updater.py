import logging, urllib.error, datetime
from labels import labels
from db_updater.src.updater_interface import UpdaterInterface

from model_realm.services.realm_service import RealmService
from model_auction.auction_service import AuctionService
from model_auction.auc_daily_stat_service import AuctionDailyStatsService
from model_auction.auc_time_stat_builder import AuctionUpdateTimeStatBuilder

# Init the logger instance
log = logging.getLogger('auction_update')
label = labels.DBU

class AuctionAPIUpdater(UpdaterInterface):

    def _generateRealmAuctionsApiLink(self, realm_slug):
        return 'https://'+self.region+'.api.battle.net/wow/auction/data/'+realm_slug+'?locale='+self.getLocale()+'&apikey='+self.getApiKey()

    def _getRealmAuctionsApiLinkData(self, url):
        data = None
        try:
            data = self.getApiLinkData(url)
            return data['files'][0]
        except urllib.error.URLError as e:
            log.error(label['@DBU7'] % url)
            log.error(e)
        return data

    def main(self):
        log.debug(label['@DBU1'])  # Begin
        if self.isRegionValid():
            # Init services
            realm_service = RealmService()
            auction_service = AuctionService()
            auctions_stats = AuctionDailyStatsService()

            realms_done = []  # Contains all done realms
            # Retrieve all active realms in defined region
            realms = realm_service.getRealmByIsActive(True)
            if not realms:
                # Error when no realms in database
                log.error(label['@DBU15'] % self.region)
            else:
                # For each realm in list proceed to create or update auctions
                for realm_name in realms:
                    if realm_name in realms_done:
                        # Realm already done
                        log.info(label['@DBU16'] % realm_name)
                    else:
                        realm_slug = realms[realm_name]
                        # Realm is not in the done list
                        log.debug(label['@DBU17'] % realm_name)
                        created = 0
                        deprecated = 0
                        updated = 0
                        total = 0
                        # Retrieve url auction api
                        url = self._generateRealmAuctionsApiLink(realm_slug)
                        api_data = self._getRealmAuctionsApiLinkData(url)
                        if api_data != None:
                            # Create new auc_time_stat_object
                            time_start = datetime.datetime.now().time()
                            # Data in api exist continue
                            last_modified = api_data['lastModified']  # Save last modified
                            auction_url = api_data['url']  # Save auctions url
                            # UPDATE
                            # Mandatory to check if Realm is up to date
                            if realm_service.isRealmNotUpdate(realm_name, last_modified):
                                # Realm is not up to date, continue - updating
                                # Continue update with auction json
                                auction_json = self._parseAuctionJson(auction_url)
                                if auction_json is not None:
                                    # Continue create with auction json
                                    connected_realms = auction_json['realms']
                                    auctions = auction_json['auctions']  # Save all auctions
                                    # Get current, active auction objects in database
                                    # Need to store auction num to check if exist in JSON
                                    current_auctions_auc = auction_service.getActiveAuctions(connected_realms)
                                    # current_auctions_auc = auction_service.getCurrentAuctions(connected_realms)
                                    log.debug('Active auctions: %s' % str(len(current_auctions_auc)))
                                    log.debug(label['@DBU24'] % realm_name)
                                    for auction in auctions:
                                        total += 1
                                        if auction['auc'] in current_auctions_auc:
                                            auc = current_auctions_auc[auction['auc']]
                                            if str(auc.bid) != str(auction['bid']) or str(auc.buyout) != str(
                                                    auction['buyout']) or str(auc.quantity) != str(
                                                auction['quantity']) or str(auc.timeLeft) != str(
                                                auction['timeLeft']):

                                                auc.bid = auction['bid']
                                                auc.buyout = auction['buyout']
                                                auc.quantity = auction['quantity']
                                                auc.timeLeft = auction['timeLeft']
                                                auc.save()
                                                updated += 1
                                            del current_auctions_auc[auction['auc']]
                                            # Api BUG with owner or ownerRealm ???
                                            # TODO: w zwiazku z wystapieniem bugu ??? w owner i ownerRealm, zalozyc FK dla ownerRealm w auction model i preSave
                                            # Update existing
                                            # if auction_service.updateAuction(auction):
                                            #     updated += 1
                                        else:
                                            # Insert new one
                                            if auction_service.crate(auction):
                                                created += 1
                                            else:
                                                # Error when inserting new auction - not valid
                                                log.error(label['@DBU19'] % realm_name)
                                                log.debug(label['@DBU14'] % auction)
                                    # All left in currnetAuctionsAuc number is deprecated - not existing in JSON
                                    # Database must be updated to set isActive in this auctions to 0
                                    for current_auction in current_auctions_auc:
                                        if auction_service.unactive(connected_realms, current_auction):
                                            deprecated += 1
                                        else:
                                            # Error
                                            log.error(label['@DBU31'] % (str(current_auction), realm_name))
                                    for each in connected_realms:
                                        # After inserting, update a connected realms
                                        if realm_service.updateLastModified(each, last_modified):
                                            realms_done.append(each['name'])
                                        else:
                                            # Error when updating a relms
                                            log.error(label['@DBU20'] % each['name'])
                                            # Summary info
                                    log.debug(label['@DBU21'] % realm_name)
                                    log.info(label['@DBU22'] % (
                                        realm_name, str(total), str(updated), str(created),
                                     str(deprecated)))
                                    # Save update time stats
                                    AuctionUpdateTimeStatBuilder(time_start, created+updated+deprecated, realm_name).save()
                                    # Update daily crud operations on realm
                                    auctions_stats.update(created, updated, deprecated, realm_name)
                                    #self.updateDailyStat(created, updated, deprecated, total)
                                else:
                                    # Auction JSON is None
                                    log.error(label['@DBU23'] % realm_name)
                            else:
                                # Realm is up to date
                                log.debug(label['@DBU26'] % realm_name)
                            # # CREATE
                            # # No necessary to check is realm up to date, table is truncated
                            #
                            #     log.debug(label['@DBU18'] % realm_name)
                            #     for auction in auctions:
                            #         total += 1
                            #         if auction_service.crate(auction):
                            #             created += 1
                            #         else:
                            #             # Error when inserting new auction - not valid
                            #             log.error(label['@DBU19'] % realm_name)
                            #             log.debug(label['@DBU14'] % auction)
                            #     for each in connected_realms:
                            #         # After inserting, update a connected realms
                            #         if realm_service.updateLastModified(each, last_modified):
                            #             realms_done.append(each['name'])
                            #         else:
                            #             # Error when updating a relms
                            #             log.error(label['@DBU20'] % each['name'])
                            #         # Summary info
                            #     log.debug(label['@DBU21'] % realm_name)
                            #     log.info(label['@DBU22'] % (
                            #         realm_name, str(total), str(updated), str(created),
                            #         str(deprecated)))
                        else:
                            # None of realm api link data
                            log.error(label['@DBU28'] % (realm_name, url))
        else:
            log.error(label['@DBU6']) #Region is not valid
        log.debug(label['@DBU2'])  # End

    def _parseAuctionJson(self, url):
        data = None
        try:
            data = self.getApiLinkData(url)
        except urllib.error.URLError as e:
            log.error(label['@DBU7'] % url)
            log.error(e)
        return data