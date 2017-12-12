from rest_framework.serializers import ModelSerializer
from .models import ItemRealmTimeSeriesDataHourly

class TSDHourlyChartSerializer(ModelSerializer):
    class Meta:
        model = ItemRealmTimeSeriesDataHourly
        fields = ('datetime', 'market_price', 'quantity')