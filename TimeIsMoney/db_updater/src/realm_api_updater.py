'''
wboniecki 2017-11-12
Realm API Updater class, contains methods for update realm and connected_realm tables in database.
Implements UpdaterInterface class.
'''
import logging, urllib.error
from labels import labels
from db_updater.src.updater_interface import UpdaterInterface
from model_realm.services import ConnectedRealmService, RealmService

# Init the logger instance
log = logging.getLogger('realm_update')
label = labels.DBU


class RealmAPIUpdater(UpdaterInterface):
    # Returns url string to parse JSON data.
    def generateApiLink(self):
        return 'https://'+self.region+'.api.battle.net/wow/realm/status?locale='+self.getLocale()+'&apikey='+self.getApiKey()

    # Main Realm API Updater method
    def main(self):
        # connected_realm counters -> cr_
        cr_total = 0
        cr_inserted = 0
        cr_deprecated = 0
        # realm counters -> r_
        r_total = 0
        r_inserted = 0
        r_updated = 0
        r_deprecated = 0

        # connected_realm hash table
        connected_realm_hash = []

        log.debug(label['@DBU1'])
        if self.isRegionValid():
            # Init services
            connected_realm_service = ConnectedRealmService()
            realm_service = RealmService()

            # Generate Realm API url
            url = self.generateApiLink()

            # Try to get data from api link
            data = None
            try:
                data = self.getApiLinkData(url)['realms']
            except urllib.error.URLError as e:
                log.error(label['@DBU7'] % url)
                log.error(e)

            # Go if data is not empty
            if data is not None:
                log.debug(label['@DBU3'])
                log.info(label['@DBU5'] % (self.region, 'ConnectedRealm'))
                log.info(label['@DBU5'] % (self.region, 'Realm'))
                # Loop through JSON -> each = 1 Realm
                for each in data:
                    r_total += 1
                    # Check connected_realm in hash table, connected_realm record must be UNIQUE
                    if each['connected_realms'] not in connected_realm_hash:
                        connected_realm_hash.append(each['connected_realms'])
                        cr_total += 1
                        # Check connected_realm exist if no, insert new and grab object
                        if not connected_realm_service.isConnectedRealmExist(each['connected_realms']):
                            if connected_realm_service.create(each['connected_realms']):
                                # Insert success
                                cr_inserted += 1
                                log.debug(label['@DBU29'] % ('ConnectedRealm', each['connected_realms']))
                            else:
                                # Insert fail
                                log.debug(each)
                                log.error(label['@DBU9'] % 'ConnectedRealm')

                    # Check realm exist, if no insert new else update
                    realm = realm_service.isRealmExist(each['name'])
                    connected_realm_id = connected_realm_service.getIdByRealms(each['connected_realms'])
                    if not realm:
                        if realm_service.create(each, connected_realm_id, self.region):
                            # Insert success
                            r_inserted += 1
                            log.debug(label['@DBU29'] % ('Realm', each['name']))
                        else:
                            # Insert fail
                            log.debug(each)
                            log.error(label['@DBU9'] % 'Realm')
                    else:
                        if realm_service.update(each):
                            # Update success
                            r_updated += 1
                            log.debug(label['@DBU30'] % ('Realm', each['name']))
                            # if false - update not needed
                # Check current db connected_realms
                connected_realms_active = connected_realm_service.getRealmsByStatus(status=True)
                for each in connected_realms_active:
                    if not each in connected_realm_hash:
                        # Change status of connected_realm to 0
                        if connected_realm_service.unactive(each):
                            cr_deprecated += 1
                            log.info(label['@DBU31'] % ('ConnectedRealm', each))
                        else:
                            # Error
                            log.debug(each)
                            log.error(label['@DBU32'] % 'ConnectedRealm')
                        # Change isActive of realm/s to 0
                        connected_realm_id = connected_realm_service.getIdByRealms(each)
                        realm_unactive = realm_service.unactive(connected_realm_id)
                        if realm_unactive > 0 or realm_service.countConnectedRealmById(connected_realm_id) > 0:
                            r_deprecated += realm_unactive
                            log.info(label['@DBU31']  % ('Realm/s', each))
                        else:
                            # Error
                            log.debug(each)
                            log.error(label['@DBU32'] % 'Realm')
        else:
            log.error(label['@DBU6']) # No valid region

        log.info(label['@DBU33'] % ('ConnectedRealm', str(cr_total), str(cr_inserted), str(cr_deprecated)))
        log.info(label['@DBU22'] % ('Realm', str(r_total), str(r_updated), str(r_inserted), str(r_deprecated)))
        log.debug(label['@DBU2'])