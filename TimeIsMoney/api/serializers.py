from rest_framework.serializers import ModelSerializer
from model_realm.models import Realm


class RealmSerializer(ModelSerializer):
    class Meta:
        model = Realm
        fields = '__all__'