
from rest_framework.serializers import ModelSerializer

# from model_auction.models import AuctionEu
# from model_auction.models import AuctionUs
from model_realm.models import Realm

#
# class AuctionEuSerializer(ModelSerializer):
#     class Meta:
#         model = AuctionEu
#         fields = '__all__'
#
#     # TODO: w ModelSerializer ta metoda domyslnie istnieje, w tym przypadku nadpisywanie jej nie jest potrzebne
#     def create(self, validated_data):
#         auction = AuctionEu()
#         auction.auc = validated_data['auc']
#         auction.item = validated_data['item']
#         auction.owner = validated_data['owner']
#         auction.ownerRealm = validated_data['ownerRealm']
#         auction.bid = validated_data['bid']
#         auction.buyout = validated_data['buyout']
#         auction.quantity = validated_data['quantity']
#         auction.timeLeft = validated_data['timeLeft']
#         auction.rand = validated_data['rand']
#         auction.seed = validated_data['seed']
#         auction.context = validated_data['context']
#
#         # Additional data if exists
#         if 'bonusLists' in validated_data:
#             auction.bonusLists = validated_data['bonusLists']
#         if 'modifiers' in validated_data:
#             auction.modifiers = validated_data['modifiers']
#         if 'petSpeciesId' in validated_data:
#             auction.petSpeciesId = validated_data['petSpeciesId']
#         if 'petBreadId' in validated_data:
#             auction.petBreadId = validated_data['petBreadId']
#         if 'petSpeciesId' in validated_data:
#             auction.petSpeciesId = validated_data['petSpeciesId']
#         if 'petQualityId' in validated_data:
#             auction.petQualityId = validated_data['petQualityId']
#
#         auction.save()
#         return auction
#
#

class RealmSerializer(ModelSerializer):
    class Meta:
        model = Realm
        fields = '__all__'