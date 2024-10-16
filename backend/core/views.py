# core/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from firebase_admin import firestore
from django.http import JsonResponse
from django.conf import settings

# Initializing the Firestore client
db = firestore.client()

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class AssetList(APIView):
    def get(self, request):
        try:
            # Getting all assets from Firestore
            assets_ref = db.collection('assets')
            assets = assets_ref.stream()

            asset_list = []
            for asset in assets:
                asset_list.append(asset.to_dict())

            return Response(asset_list, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Adding a new asset to Firestore
            asset_data = request.data
            db.collection('assets').add(asset_data)

            return Response({"message": "Asset added successfully!"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Yahoo Finance API view
class YahooFinance(APIView):
    def get(self, request):
        print(settings.YAHOO_FINANCE_API_KEY, settings.YAHOO_FINANCE_API_HOST)
        try:
            url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/quote"
            headers = {
                'X-RapidAPI-Key': settings.YAHOO_FINANCE_API_KEY,
                'X-RapidAPI-Host': settings.YAHOO_FINANCE_API_HOST
            }
            params = {
                "ticker": "AAPL",
                "type": "STOCKS"
            }
 
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            return Response(data, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": "Failed to connect to Yahoo Finance API. Details: " + str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Alpha Vantage API view
class AlphaVantage(APIView):
    def get(self, request):
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": "IBM",
                "apikey": settings.ALPHA_VANTAGE_API_KEY,
                "outputsize": "compact",
                "datatype": "json"
            }
            response = requests.get(url, params=params)
            data = response.json()

            return Response(data, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": "Failed to connect to Alpha Vantage API. Details: " + str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
