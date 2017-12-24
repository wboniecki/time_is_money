from rest_framework.serializers import ModelSerializer
from .models import ItemRealmTimeSeriesDataHourly, ItemRealmTimeSeriesDataDaily

class TSDHourlyChartSerializer(ModelSerializer):
    class Meta:
        model = ItemRealmTimeSeriesDataHourly
        fields = ('datetime', 'market_price', 'quantity')

class SingleTSDHourlySerializer(ModelSerializer):
    class Meta:
        model = ItemRealmTimeSeriesDataHourly
        fields = ('quantity',
                  'market_price',
                  'avg_price',
                  'standard_deviation',
                  'datetime')

class TSDDailyChartSerializer(ModelSerializer):
    class Meta:
        model = ItemRealmTimeSeriesDataDaily
        fields = ('date', 'max_quantity', 'avg_market_price')

class TSDDailyDetailsChartSerializer(ModelSerializer):
    class Meta:
        model = ItemRealmTimeSeriesDataDaily
        fields = (
            'date',
            'max_quantity',
            'avg_quantity',
            'min_quantity',
            'open_market_price',
            'end_market_price',
            'min_market_price',
            'avg_market_price',
            'max_market_price')