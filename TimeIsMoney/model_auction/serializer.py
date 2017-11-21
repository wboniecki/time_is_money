from rest_framework.serializers import ModelSerializer
#from .models import AuctionEu, AuctionUs
from .models import Auction, AuctionDailyStats

class AuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'

class AuctionDailyStatsSerializer(ModelSerializer):
    class Meta:
        model = AuctionDailyStats
        fields = '__all__'

# class AuctionUsSerializer(ModelSerializer):
#     class Meta:
#         model = AuctionUs
#         fields = '__all__'

