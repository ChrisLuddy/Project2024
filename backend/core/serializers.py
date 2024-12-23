# core/serializers.py
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        """
        Create a new user with the specified role.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email = validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            is_active=True
        )        
        return user


# Fund Serializer
class FundSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    user_id = serializers.CharField(max_length=255, required=False)
    client_id = serializers.CharField(max_length=255, required=False)


# Portfolio Serializer
class PortfolioSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    fund_id = serializers.CharField(max_length=255)


# Asset Serializer
class AssetSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=50)
    price = serializers.FloatField()
    volume = serializers.IntegerField()
    amount = serializers.IntegerField()
    last_updated = serializers.DateTimeField(required=False)
    portfolio_id = serializers.CharField(max_length=255)


# Client Serializer
class ClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    fund_manager_id = serializers.IntegerField()


# Order Serializer
class OrderSerializer(serializers.Serializer):
    order_type = serializers.ChoiceField(choices=["buy", "sell"])
    amount = serializers.IntegerField()
    portfolio_id = serializers.CharField(max_length=255)


# Trade Rating Serializer
class TradeRatingSerializer(serializers.Serializer):
    rating = serializers.FloatField(min_value=0, max_value=5)
    order_id = serializers.CharField(max_length=255)


# AI Forecast Serializer
class AIForecastSerializer(serializers.Serializer):
    forecast = serializers.CharField(max_length=255)
    user_id = serializers.IntegerField()


# Support Request Serializer
class SupportRequestSerializer(serializers.Serializer):
    request = serializers.CharField(max_length=1000)
    user_id = serializers.CharField(max_length=255)
