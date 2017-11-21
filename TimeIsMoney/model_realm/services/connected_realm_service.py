from ..models import ConnectedRealm
from django.db.models import ObjectDoesNotExist
from ..serializer import ConnectedRealmSerializer


class ConnectedRealmService:

    def create(self, realms):
        data = {
            'realms': realms
        }
        serializer = ConnectedRealmSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return True

        return False

    def getIdByRealms(self, realms):
        return ConnectedRealm.objects.filter(realms=realms).first().id


    def getRealmsByStatus(self, status):
        records = ConnectedRealm.objects.filter(status=status)
        realms_table = []

        if records:
            for record in records:
                realms_table.append(record.realms)

        return realms_table

    def isConnectedRealmExist(self, realms):
        return ConnectedRealm.objects.filter(realms=realms).first()

    def unactive(self, realms):
        connected_realm = ConnectedRealm.objects.filter(realms=realms).first()

        if connected_realm:
            connected_realm.status = 0
            connected_realm.save()
            return True

        return False