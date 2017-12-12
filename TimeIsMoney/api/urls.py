from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    realm_list,
    realm_detail,
    tsd_hourly_realm_item_chart
)

urlpatterns = [
    url(r'^realms', realm_list, name='model.realm-list'),
    url(r'^model.realm/(?P<pk>\d+)', realm_detail, name='model.realm-details'),
    url(r'(?P<realm_slug>[-\w]+)/hourly/(?P<itemId>\d+)', tsd_hourly_realm_item_chart, name='tsd_hourly_chart')
]

urlpatterns = format_suffix_patterns(urlpatterns)