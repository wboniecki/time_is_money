from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from model_tsd.services.tsd_hourly_service import TSDHourlyService
from model_tsd.serializer import (
    TSDHourlyChartSerializer,
    SingleTSDHourlySerializer,
    TSDDailyChartSerializer,
    TSDDailyDetailsChartSerializer)
from model_item.item_service import ItemService
from model_item.serializer import ItemDetailSerializer
from model_realm.services.realm_service import RealmService

from model_realm.models import Realm
from .serializers import RealmSerializer
from model_realm.serializer import RealmDetailSerializer, RealmsInConnectedRealmSerializer

from db_updater.src.service_manager import createOrUpdateRealms
from db_updater.src.service_manager import updateAllAuctions, deleteOldAuctions, tsdUpdater, tsdDeleteOld
from db_updater.src.service_manager import createOrUpdateItems
from model_tsd.calculation import Calculation
from model_tsd.services.tsd_hourly_service import TSDHourlyService
from model_tsd.services.tsd_daily_service import TSDDailyService
from model_tsd.test_calculation import calc_test
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
def tsd_hourly_realm_item_chart(request, itemId, realm_slug):
    item_service = ItemService()
    realm_service = RealmService()
    tsd_service = TSDHourlyService()
    realm = realm_service.getRealmBySlug(realm_slug)
    item = item_service.getItemByItemId(itemId)
    if realm and item:
        tsd_list = tsd_service.getRealmItemChartData(item, realm.connected_realm)
        serializer = TSDHourlyChartSerializer(tsd_list, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def tsd_daily_realm_time_chart(request, itemId, realm_slug):
    item_service = ItemService()
    realm_service = RealmService()
    tsd_service = TSDDailyService()
    realm = realm_service.getRealmBySlug(realm_slug)
    item = item_service.getItemByItemId(itemId)
    if realm and item:
        tsd_list = tsd_service.getRealmItemChartData(item, realm.connected_realm)
        serializer = TSDDailyChartSerializer(tsd_list, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def tsd_daily_details_realm_time_chart(request, itemId, realm_slug):
    item_service = ItemService()
    realm_service = RealmService()
    tsd_service = TSDDailyService()
    realm = realm_service.getRealmBySlug(realm_slug)
    item = item_service.getItemByItemId(itemId)
    if realm and item:
        tsd_list = tsd_service.getRealmItemChartData(item, realm.connected_realm)
        serializer = TSDDailyDetailsChartSerializer(tsd_list, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def realm_item(request, itemId, realm_slug):
    item_service = ItemService()
    realm_service = RealmService()
    tsd_service = TSDHourlyService()
    realm = realm_service.getRealmBySlug(realm_slug)
    item = item_service.getItemByItemId(itemId)
    if realm and item:
        tsd = tsd_service.getRealmItemLastData(item, realm.connected_realm)
        serializer = SingleTSDHourlySerializer(tsd)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def realm_list(request, format=None):
    if request.method == 'GET':
        realms = Realm.objects.all()
        serializer = RealmSerializer(realms, many=True)
        # TEST PURPOSES ONLY
        #deleteOldAuctions('eu')
        #tsdUpdater()
        #tsdDeleteOld()
        #createOrUpdateItems('eu')
        #updateAllAuctions('eu')
        #updateConnectedRealm('eu')
        #createOrUpdateRealms('eu')
        #calc_test()
        return Response(serializer.data)

@api_view(['GET'])
def item_detail(request, itemId):
    item_service = ItemService()
    item = item_service.getItemByItemId(itemId)
    if item:
        serializer = ItemDetailSerializer(item)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def connected_realm_list(request, realm_slug):
    realm_service = RealmService()
    realm = realm_service.getRealmBySlug(realm_slug)
    connected_realms = realm_service.getRealmNamesAndSlugsByConnectedRealmId(realm.connected_realm)
    if connected_realms:
        serializer = RealmsInConnectedRealmSerializer(connected_realms, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def realm_detail(request, realm_slug):
    realm_service = RealmService()
    realm = realm_service.getRealmBySlug(realm_slug)
    if realm:
        serializer = RealmDetailSerializer(realm)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def getRealms():
    realms = Realm.objects.all()
    serializer = RealmSerializer(realms, many=True)
    return serializer.data