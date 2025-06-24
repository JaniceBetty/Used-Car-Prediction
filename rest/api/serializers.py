from rest_framework import serializers

# Define enums as constants
SELLER_TYPE_CHOICES = ["individual", "dealer", "trusted"]
FUEL_TYPE_CHOICES = ["petrol", "diesel", "electric", "lpg", "cng"]
TRANSMISSION_TYPE_CHOICES = ["automatic", "manual"]

class CarPricePredictionRequestSerializer(serializers.Serializer):
    vehicle_age = serializers.IntegerField()
    km_driven = serializers.IntegerField()
    mileage = serializers.FloatField()
    engine = serializers.IntegerField()
    max_power = serializers.FloatField()
    seats = serializers.IntegerField()
    seller_type = serializers.ChoiceField(choices=SELLER_TYPE_CHOICES)
    fuel_type = serializers.ChoiceField(choices=FUEL_TYPE_CHOICES)
    transmission_type = serializers.ChoiceField(choices=TRANSMISSION_TYPE_CHOICES)

class CarPricePredictionResponseSerializer(serializers.Serializer):
    min_price = serializers.IntegerField()
    max_price = serializers.IntegerField()
    optimal_price = serializers.IntegerField()
