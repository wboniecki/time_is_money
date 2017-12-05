import datetime
from ..models import Realm
from django.db.models import ObjectDoesNotExist
from ..serializer import RealmSerializer


class RealmService:

    def countConnectedRealmById(self, connected_realm_id):
        return len(Realm.objects.filter(connected_realm=connected_realm_id))

    # Method called every time when new record show. Inserts this record to database.
    def create(self, json_data, connected_realm_id, region):
        data = {
            'region': region,
            'name': json_data['name'],
            'slug': json_data['slug'],
            'status': json_data['status'],
            'population': json_data['population'],
            'connected_realm': connected_realm_id,
            'dateModified': datetime.datetime.now(),
            'dateChecked': datetime.date.today()
        }

        serializer = RealmSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return True

        return False

    def update(self, realm_data):
        realm = self.getRealmByName(realm_name=realm_data['name'])

        if (realm.population != realm_data['population'] or
                    realm.name != realm_data['name'] or
                    realm.slug != realm_data['slug'] or
                    realm.status != realm_data['status']):

            realm.population = realm_data['population']
            realm.name = realm_data['name']
            realm.slug = realm_data['slug']
            realm.status = realm_data['status']

            realm.save()
            return True

        return False

    def getRealmByIsActive(self, is_active):
        records = Realm.objects.filter(isActive=is_active)
        realm_table = {}

        if records:
            for record in records:
                realm_table[record.name] = record.slug

        return realm_table

    def getRealmByName(self, realm_name):
        return Realm.objects.filter(name=realm_name).first()

    def getRealmConnectedRealmId(self, realm_name):
        realm = Realm.objects.filter(name=realm_name).first()
        if realm:
            return realm.connected_realm
        return None

    def getRealmNamesByConnectedRealmId(self, _id):
        realm_names = []
        realms = Realm.objects.filter(connected_realm=_id)
        for realm in realms:
            realm_names.append(realm.name)
        return realm_names

    def isRealmExist(self, realm_name):
        return Realm.objects.filter(name=realm_name).first()

    def isRealmNotUpdate(self, realm_name, last_modified):
        realm = Realm.objects.filter(name=realm_name).first()

        if realm:
            if str(realm.lastModified) != str(last_modified):
                return True
        return False

    def unactive(self, connected_realm_id):
        realms = Realm.objects.filter(connected_realm=connected_realm_id)
        counter = 0

        if realms:
            for realm in realms:
                if realm.isActive == True or realm.status == True:
                    realm.isActive = False
                    realm.status = False
                    realm.save()
                    counter += 1

        return counter

    def updateLastModified(self, connected_realm, last_modified):
        realm = Realm.objects.filter(name=connected_realm['name'], slug=connected_realm['slug']).first()
        if realm:
            realm.lastModified = last_modified
            realm.dateModified = datetime.datetime.now()
            realm.save()
            return True
        return False