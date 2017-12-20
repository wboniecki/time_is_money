from rest_framework.serializers import ModelSerializer
from .models import Item

#TODO: Usun lub zmodyfikuj - nieuzywane
class ItemSerilizer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemDetailSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('itemId', 'name', 'sellPrice', 'icon')