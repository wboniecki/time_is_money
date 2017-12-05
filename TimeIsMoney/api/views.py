from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from model_realm.models import Realm
from .serializers import RealmSerializer

from db_updater.src.service_manager import createOrUpdateRealms
from db_updater.src.service_manager import updateAllAuctions, deleteOldAuctions
from db_updater.src.service_manager import createOrUpdateItems
from model_tsd.calculation import Calculation
import logging


class RealmListAPIView(ListAPIView):
    queryset = Realm.objects.all()
    serializer_class = RealmSerializer

class RealmDetailAPIView(RetrieveAPIView):
    queryset = Realm.objects.all()
    serializer_class = RealmSerializer
    print(serializer_class.data)


@api_view(['GET'])
def realm_list(request, format=None):
    if request.method == 'GET':
        realms = Realm.objects.all()
        serializer = RealmSerializer(realms, many=True)
        # TEST PURPOSES ONLY
        #print(utils.unifyPrice("0"))
        calc = Calculation()
        #calc.calc(114821, "Doomhammer")
        deleteOldAuctions('eu')
        #createOrUpdateItems('eu')
        #updateAllAuctions('eu')
        #createAllAuctions('eu')
        #updateConnectedRealm('eu')
        #createOrUpdateRealms('eu')
        #updateAuctions('fy4phjcqqt2qqphjhqumtvra8vws2w4y', 'eu')
        #migrateAllAuctions('fy4phjcqqt2qqphjhqumtvra8vws2w4y', 'eu')
        #updateAllAuctions('fy4phjcqqt2qqphjhqumtvra8vws2w4y', 'eu')
        return Response(serializer.data)

@api_view(['GET'])
def realm_detail(request, pk):
    try:
        realm = Realm.objects.get(pk=pk)
    except Realm.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RealmSerializer(realm)
        print(serializer.data)
        json = JSONRenderer().render(serializer.data)
        print(json)
        return Response(serializer.data)

def getRealms():
    realms = Realm.objects.all()
    serializer = RealmSerializer(realms, many=True)
    return serializer.data

@api_view(['GET'])
def updater(request, region):
    #TODO: wstępnie ogarnięte serializacje (save oraz update), uporządkowałbym to do klasy i zaczął kodzić pobieranie json z blizzapi
    if request.method == 'GET':
        realms = getRealms()
        for realm in realms:
            if realm['region'] == region:
                print('ok')

            if realm['region'] == 'us':
                print('update')
                urealm = Realm.objects.get(name=realm['name'], region=realm['region'])
                realm['region'] = 'eu'
                serializer = RealmSerializer(urealm, data=realm)
                if serializer.is_valid():
                    serializer.update(urealm, serializer.validated_data)
                    print(serializer.validated_data)
        return Response(getRealms())

class Updater(UpdateAPIView):
    queryset = Realm.objects.all()
    serializer_class = RealmSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.region = request.data.get('region')
        instance.save()

        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)