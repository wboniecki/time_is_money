from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from .views import (
    realm_list,
    realm_detail,
    updater,
    RealmDetailAPIView
)

# from .views import (
#     RealmListAPIView
# )

urlpatterns = [
    url(r'^realms', realm_list, name='model.realm-list'),
    url(r'^updater/(?P<region>[\w-]+)', updater, name='updater'),
    url(r'^model.realm/(?P<pk>\d+)', realm_detail, name='model.realm-details')
]

urlpatterns = format_suffix_patterns(urlpatterns)