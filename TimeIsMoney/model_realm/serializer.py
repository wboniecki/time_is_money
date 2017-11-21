from rest_framework.serializers import ModelSerializer
from .models import Realm, ConnectedRealm

class RealmSerializer(ModelSerializer):
    class Meta:
        model = Realm
        fields = '__all__'

class ConnectedRealmSerializer(ModelSerializer):
    class Meta:
        model = ConnectedRealm
        fields = '__all__'