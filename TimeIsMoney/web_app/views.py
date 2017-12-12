from django.shortcuts import render, Http404, render_to_response
from model_realm.services.realm_service import RealmService
from model_item.item_service import ItemService
from model_tsd.services.tsd_hourly_service import TSDHourlyService

from django.conf import settings

# Create your views here.
def home_page(request):
    return render(request, 'web_app/index.html', {})

def item_details_view(request, realm_slug, item_id):
    realm_service = RealmService()
    item_service = ItemService()
    tsd_service = TSDHourlyService()
    realm = realm_service.getRealmBySlug(realm_slug)
    item = item_service.getItemByItemId(item_id)
    tsd = tsd_service.getRealmItemLastData(item.id, realm.connected_realm)
    print(settings.STATIC_URL)
    print(tsd.market_price)
    print(realm.connected_realm.id)
    print(item.id)
    # TODO: dodaj walidacje na istnienie TSD (najlepiej juz w templatce)
    if realm and realm.isActive and item:
        connected_realms = realm_service.getRealmNamesAndSlugsByConnectedRealmId(realm.connected_realm)
        return render(request, 'web_app/item_details.html',
                      {
                          'realm': realm,
                          'item': item,
                          'tsd': tsd,
                          'connected_realms': connected_realms
                      })
    else:
        raise Http404("No valid realm or item.")