from rest_framework.serializers import ModelSerializer
from .models import Realm, ConnectedRealm

class RealmSerializer(ModelSerializer):
    class Meta:
        model = Realm
        fields = '__all__'

class RealmDetailSerializer(ModelSerializer):
    class Meta:
        model = Realm
        fields = ('name', 'slug', 'isActive', 'population', 'dateModified')

class RealmsInConnectedRealmSerializer(ModelSerializer):
    class Meta:
        model = Realm
        fields = ('name', 'slug')

class ConnectedRealmSerializer(ModelSerializer):
    class Meta:
        model = ConnectedRealm
        fields = '__all__'