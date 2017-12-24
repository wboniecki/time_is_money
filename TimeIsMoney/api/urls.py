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
    connected_realm_list
)

urlpatterns = [
    url(r'^realms', realm_list, name='model.realm-list'),
    url(r'^realm/(?P<realm_slug>[-\w]+)', realm_detail, name='realm-details'),
    url(r'^item/(?P<itemId>\d+)', item_detail, name='item-details'),
    url(r'^connected-realm/(?P<realm_slug>[-\w]+)', connected_realm_list, name='connected-realm-list'),
    url(r'(?P<realm_slug>[-\w]+)/last/(?P<itemId>\d+)', realm_item, name='tsd_last_realm_item'),
    url(r'(?P<realm_slug>[-\w]+)/hourly/(?P<itemId>\d+)', tsd_hourly_realm_item_chart, name='tsd_hourly_chart'),
    url(r'(?P<realm_slug>[-\w]+)/daily/(?P<itemId>\d+)', tsd_daily_realm_time_chart, name='tsd_daily_chart'),
    url(r'(?P<realm_slug>[-\w]+)/daily-details/(?P<itemId>\d+)', tsd_daily_details_realm_time_chart, name='tsd_daily_details_chart')
]

urlpatterns = format_suffix_patterns(urlpatterns)