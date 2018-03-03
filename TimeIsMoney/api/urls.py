from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    realm_list,
    realm_detail,
    tsd_hourly_realm_item_chart,
    tsd_daily_realm_time_chart,
    tsd_daily_details_realm_time_chart,
    realm_item,
    item_detail,
    item_list,
    connected_realm_list,
    active_realm_list,
    realm_active_auction_count
)

urlpatterns = [
    url(r'^realms-test', realm_list, name='model.realm-list'),
    url(r'^realms', active_realm_list, name='active-realm-list'),
    url(r'^realm/(?P<realm_slug>[-\w]+)', realm_detail, name='realm-details'),
    url(r'^item/(?P<itemId>\d+)', item_detail, name='item-details'),
    url(r'^item-list', item_list, name='item-list'),
    url(r'^connected-realm/(?P<realm_slug>[-\w]+)', connected_realm_list, name='connected-realm-list'),
    url(r'(?P<realm_slug>[-\w]+)/last/(?P<itemId>\d+)', realm_item, name='tsd_last_realm_item'),
    url(r'(?P<realm_slug>[-\w]+)/hourly/(?P<itemId>\d+)', tsd_hourly_realm_item_chart, name='tsd_hourly_chart'),
    url(r'(?P<realm_slug>[-\w]+)/daily/(?P<itemId>\d+)', tsd_daily_realm_time_chart, name='tsd_daily_chart'),
    url(r'(?P<realm_slug>[-\w]+)/daily-details/(?P<itemId>\d+)', tsd_daily_details_realm_time_chart, name='tsd_daily_details_chart'),
    url(r'(?P<realm_slug>[-\w]+)/auction-count',realm_active_auction_count, name='realm-active-auction-count')
]

urlpatterns = format_suffix_patterns(urlpatterns)