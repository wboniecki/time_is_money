from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    home_page,
    item_details_view)

urlpatterns = [
    url(r'^$', home_page, name='home_page'),
    url(r'^(?P<realm_slug>[-\w]+)/item/(?P<item_id>\d+)', item_details_view, name='item_details')
    #url(r'^realms', realm_list, name='model.realm-list'),
    #url(r'^model.realm/(?P<pk>\d+)', realm_detail, name='model.realm-details')
]

urlpatterns = format_suffix_patterns(urlpatterns)