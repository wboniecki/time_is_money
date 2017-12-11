from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from model_realm.models import Realm
from .serializers import RealmSerializer

from db_updater.src.service_manager import createOrUpdateRealms
from db_updater.src.service_manager import updateAllAuctions, deleteOldAuctions, tsdUpdater
from db_updater.src.service_manager import createOrUpdateItems
from model_tsd.calculation import Calculation
from model_tsd.services.tsd_hourly_service import TSDHourlyService
import logging
import datetime


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
        #deleteOldAuctions('eu')
        #tsdUpdater()
        #createOrUpdateItems('eu')
        #updateAllAuctions('eu')
        #updateConnectedRealm('eu')
        #createOrUpdateRealms('eu')
        return Response(serializer.data)

@api_view(['GET'])
def realm_detail(request, pk):
    try:
        realm = Realm.objects.get(pk=pk)
        serializer = RealmSerializer(realm)
        return Response(serializer.data)
    except Realm.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def getRealms():
    realms = Realm.objects.all()
    serializer = RealmSerializer(realms, many=True)
    return serializer.data