# core/views.py
import requests
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .firebase_models import Client, Fund, Portfolio, Asset, Order, TradeRating, AIForecast, SupportRequest
from django.conf import settings
from .serializers import RegisterSerializer
from .permissions import IsFundAdmin, IsFundManager, IsFundAdminOrFundManager

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionStatusView(APIView):
    permission_classes = [IsFundAdminOrFundManager]

    def get(self, request):
        try:
            customer_email = request.user.email
            customers = stripe.Customer.list(email=customer_email, limit=1)

            if not customers.data:
                return Response({"status": "No Stripe customer found"}, status=404)

            customer_id = customers.data[0].id

            subscriptions = stripe.Subscription.list(customer=customer_id, status="all", limit=1)

            if not subscriptions.data:
                return Response({"status": "No active subscription"}, status=200)

            subscription = subscriptions.data[0]

            plan = subscription['items']['data'][0]['plan']
            interval = plan['interval']
            nickname = plan['nickname']

            product_id = plan['product']
            product = stripe.Product.retrieve(product_id)
            plan_name = nickname if nickname else product['name']

            return Response({
                "status": subscription.status,
                "current_period_end": subscription.current_period_end,
                "plan_name": plan_name,
                "interval": interval
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsFundAdminOrFundManager]

    def post(self, request):
        try:
            price_id = request.data.get('price_id')  # monthly or yearly Price ID

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                # customer_email=request.user.email,
                customer_email=request.data.get('email'),
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url = 'http://127.0.0.1:5500/ACT-HTML-JavaScript/stripe-success.html?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = 'http://127.0.0.1:5500/ACT-HTML-JavaScript/stripe-cancel.html',

            )
            return Response({'sessionId': session.id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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


class AssetView(APIView):
    permission_classes = [IsFundManager]
    def get(self, request, asset_id=None):
        if asset_id:
            asset = Asset.get(asset_id)
            return Response(asset, status=status.HTTP_200_OK) if asset else Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)
        assets = Asset.get_all()
        return Response(assets, status=status.HTTP_200_OK)

    def post(self, request):
        asset = Asset(
            symbol=request.data.get('symbol'),
            price=request.data.get('price'),
            volume=request.data.get('volume'),
            amount=request.data.get('amount'),
            last_updated=request.data.get('last_updated'),
            portfolio_id=request.data.get('portfolio_id')
        )
        asset_id = asset.save()
        return Response({"asset_id": asset_id, "message": "Asset created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, asset_id):
        asset = Asset(
            symbol=request.data.get('symbol'),
            price=request.data.get('price'),
            volume=request.data.get('volume'),
            amount=request.data.get('amount'),
            last_updated=request.data.get('last_updated'),
            portfolio_id=request.data.get('portfolio_id')
        )
        asset.update(asset_id)
        updated_asset = Asset.get(asset_id)
        return Response(updated_asset, status=status.HTTP_200_OK)

    def delete(self, request, asset_id):
        Asset.delete(asset_id)
        return Response({"message": "Asset deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class ClientView(APIView):
    permission_classes = [IsFundManager]
    def get(self, request, client_id=None):
        if client_id:
            client = Client.get(client_id)
            return Response(client, status=status.HTTP_200_OK) if client else Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        clients = Client.get_all()
        return Response(clients, status=status.HTTP_200_OK)

    def post(self, request):
        client = Client(name=request.data.get('name'), fund_manager_id=request.data.get('fund_manager_id'))
        client_id = client.save()
        return Response({"client_id": client_id, "message": "Client created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, client_id):
        client = Client(name=request.data.get('name'), fund_manager_id=request.data.get('fund_manager_id'))
        client.update(client_id)
        updated_client = Client.get(client_id)
        return Response(updated_client, status=status.HTTP_200_OK)

    def delete(self, request, client_id):
        Client.delete(client_id)
        return Response({"message": "Client deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class FundView(APIView):
    permission_classes = [IsFundManager]
    def get(self, request, fund_id=None):
        if fund_id:
            fund = Fund.get(fund_id)
            return Response(fund, status=status.HTTP_200_OK) if fund else Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)
        funds = Fund.get_all()
        return Response(funds, status=status.HTTP_200_OK)

    def post(self, request):
        fund = Fund(name=request.data.get('name'), user_id=request.data.get('user_id'), client_id=request.data.get('client_id'))
        fund_id = fund.save()
        return Response({"fund_id": fund_id, "message": "Fund created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, fund_id):
        fund = Fund(name=request.data.get('name'), user_id=request.data.get('user_id'), client_id=request.data.get('client_id'))
        fund.update(fund_id)
        updated_fund = Fund.get(fund_id)
        return Response(updated_fund, status=status.HTTP_200_OK)

    def delete(self, request, fund_id):
        Fund.delete(fund_id)
        return Response({"message": "Fund deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class PortfolioView(APIView):
    permission_classes = [IsFundAdminOrFundManager]
    def get(self, request, portfolio_id=None):
        if portfolio_id:
            portfolio = Portfolio.get(portfolio_id)
            return Response(portfolio, status=status.HTTP_200_OK) if portfolio else Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)
        portfolios = Portfolio.get_all()
        return Response(portfolios, status=status.HTTP_200_OK)

    def post(self, request):
        portfolio = Portfolio(name=request.data.get('name'), fund_id=request.data.get('fund_id'))
        portfolio_id = portfolio.save()
        return Response({"portfolio_id": portfolio_id, "message": "Portfolio created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, portfolio_id):
        portfolio = Portfolio(name=request.data.get('name'), fund_id=request.data.get('fund_id'))
        portfolio.update(portfolio_id)
        updated_portfolio = Portfolio.get(portfolio_id)
        return Response(updated_portfolio, status=status.HTTP_200_OK)

    def delete(self, request, portfolio_id):
        Portfolio.delete(portfolio_id)
        return Response({"message": "Portfolio deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    permission_classes = [IsFundAdminOrFundManager]
    def get(self, request, order_id=None):
        if order_id:
            order = Order.get(order_id)
            return Response(order, status=status.HTTP_200_OK) if order else Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        orders = Order.get_all()
        return Response(orders, status=status.HTTP_200_OK)

    def post(self, request):
        order = Order(order_type=request.data.get('order_type'), amount=request.data.get('amount'), portfolio_id=request.data.get('portfolio_id'))
        order_id = order.save()
        return Response({"order_id": order_id, "message": "Order created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, order_id):
        order = Order(order_type=request.data.get('order_type'), amount=request.data.get('amount'), portfolio_id=request.data.get('portfolio_id'))
        order.update(order_id)
        updated_order = Order.get(order_id)
        return Response(updated_order, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        Order.delete(order_id)
        return Response({"message": "Order deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class TradeRatingView(APIView):
    permission_classes = [IsFundAdminOrFundManager]
    def get(self, request, trade_rating_id=None):
        if trade_rating_id:
            trade_rating = TradeRating.get(trade_rating_id)
            return Response(trade_rating, status=status.HTTP_200_OK) if trade_rating else Response({'error': 'Trade Rating not found'}, status=status.HTTP_404_NOT_FOUND)
        trade_ratings = TradeRating.get_all()
        return Response(trade_ratings, status=status.HTTP_200_OK)

    def post(self, request):
        trade_rating = TradeRating(rating=request.data.get('rating'), order_id=request.data.get('order_id'))
        trade_rating_id = trade_rating.save()
        return Response({"trade_rating_id": trade_rating_id, "message": "Trade Rating created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, trade_rating_id):
        trade_rating = TradeRating(rating=request.data.get('rating'), order_id=request.data.get('order_id'))
        trade_rating.update(trade_rating_id)
        updated_trade_rating = TradeRating.get(trade_rating_id)
        return Response(updated_trade_rating, status=status.HTTP_200_OK)

    def delete(self, request, trade_rating_id):
        TradeRating.delete(trade_rating_id)
        return Response({"message": "Trade Rating deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class AIForecastView(APIView):
    permission_classes = [IsFundAdminOrFundManager]

    def get(self, request, forecast_id=None):
        if forecast_id:
            forecast = AIForecast.get(forecast_id)
            return Response(forecast, status=status.HTTP_200_OK) if forecast else Response({'error': 'AI Forecast not found'}, status=status.HTTP_404_NOT_FOUND)
        forecasts = AIForecast.get_all()
        return Response(forecasts, status=status.HTTP_200_OK)

    def post(self, request):
        # Отладочное сообщение
        print(f"Request user: {request.user}, is_authenticated: {request.user.is_authenticated}, is_active: {request.user.is_active}, groups: {request.user.groups.all()}")

        forecast = AIForecast(forecast=request.data.get('forecast'), user_id=request.data.get('user_id'))
        forecast_id = forecast.save()
        return Response({"forecast_id": forecast_id, "message": "AI Forecast created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, forecast_id):
        forecast = AIForecast(forecast=request.data.get('forecast'), user_id=request.data.get('user_id'))
        forecast.update(forecast_id)
        updated_forecast = AIForecast.get(forecast_id)
        return Response(updated_forecast, status=status.HTTP_200_OK)

    def delete(self, request, forecast_id):
        AIForecast.delete(forecast_id)
        return Response({"message": "AI Forecast deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class SupportRequestView(APIView):
    permission_classes = [IsFundAdminOrFundManager]
    def get(self, request, support_request_id=None):
        if support_request_id:
            support_request = SupportRequest.get(support_request_id)
            return Response(support_request, status=status.HTTP_200_OK) if support_request else Response({'error': 'Support Request not found'}, status=status.HTTP_404_NOT_FOUND)
        support_requests = SupportRequest.get_all()
        return Response(support_requests, status=status.HTTP_200_OK)

    def post(self, request):
        support_request = SupportRequest(request=request.data.get('request'), user_id=request.data.get('user_id'))
        support_request_id = support_request.save()
        return Response({"support_request_id": support_request_id, "message": "Support Request created successfully!"}, status=status.HTTP_201_CREATED)

    def put(self, request, support_request_id):
        support_request = SupportRequest(request=request.data.get('request'), user_id=request.data.get('user_id'))
        support_request.update(support_request_id)
        updated_support_request = SupportRequest.get(support_request_id)
        return Response(updated_support_request, status=status.HTTP_200_OK)

    def delete(self, request, support_request_id):
        SupportRequest.delete(support_request_id)
        return Response({"message": "Support Request deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class YahooFinance(APIView):
    def get(self, request):
        try:
            url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/quote"
            headers = {
                'X-RapidAPI-Key': settings.YAHOO_FINANCE_API_KEY,
                'X-RapidAPI-Host': settings.YAHOO_FINANCE_API_HOST
            }
            params = {"ticker": "AAPL", "type": "STOCKS"}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": f"Failed to connect to Yahoo Finance API: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            return Response({"error": f"Failed to connect to Alpha Vantage API: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class YahooNewsView(APIView):
    """
    Fetches financial news from Yahoo Finance using RapidAPI and returns the response.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        # Extract query parameters
        tickers = request.GET.get('tickers', 'AAPL')  # Default to AAPL if no tickers are provided
        news_type = request.GET.get('type', 'ALL')    # Default to ALL if no type is provided

        try:
            # Define the Yahoo Finance API URL and headers
            url = "https://yahoo-finance15.p.rapidapi.com/api/v2/markets/news"
            headers = {
                'X-RapidAPI-Key': settings.YAHOO_FINANCE_API_KEY,
                'X-RapidAPI-Host': "yahoo-finance15.p.rapidapi.com"
            }
            params = {"tickers": tickers, "type": news_type}

            # Make the API request
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": f"Failed to fetch data from Yahoo Finance: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
