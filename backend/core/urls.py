# core/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, AssetView, YahooFinance, AlphaVantage,
    ClientView, FundView, PortfolioView, OrderView,
    TradeRatingView, AIForecastView, SupportRequestView, YahooNewsView,
    CreateCheckoutSessionView, SubscriptionStatusView)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('yahoo-finance/', YahooFinance.as_view(), name='yahoo_finance'),
    path('alpha-vantage/', AlphaVantage.as_view(), name='alpha_vantage'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # CRUD endpoints for Firebase models
    path('assets/', AssetView.as_view(), name='asset-list-create'),
    path('assets/<str:asset_id>/', AssetView.as_view(), name='asset-detail'),
    path('clients/', ClientView.as_view(), name='client-list-create'),
    path('clients/<str:client_id>/', ClientView.as_view(), name='client-detail'),
    path('funds/', FundView.as_view(), name='fund-list-create'),
    path('funds/<str:fund_id>/', FundView.as_view(), name='fund-detail'),
    path('portfolios/', PortfolioView.as_view(), name='portfolio-list-create'),
    path('portfolios/<str:portfolio_id>/', PortfolioView.as_view(), name='portfolio-detail'),
    path('orders/', OrderView.as_view(), name='order-list-create'),
    path('orders/<str:order_id>/', OrderView.as_view(), name='order-detail'),
    path('trade-ratings/', TradeRatingView.as_view(), name='trade-rating-list-create'),
    path('trade-ratings/<str:trade_rating_id>/', TradeRatingView.as_view(), name='trade-rating-detail'),
    path('ai-forecasts/', AIForecastView.as_view(), name='ai-forecast-list-create'),
    path('ai-forecasts/<str:forecast_id>/', AIForecastView.as_view(), name='ai-forecast-detail'),
    path('support-requests/', SupportRequestView.as_view(), name='support-request-list-create'),
    path('support-requests/<str:support_request_id>/', SupportRequestView.as_view(), name='support-request-detail'),
    path('yahoo-news/', YahooNewsView.as_view(), name='yahoo-news'),

    # AI routes
    path('act-ai/', include('act_ai.urls')),

    # Stripe routes
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('subscription-status/', SubscriptionStatusView.as_view(), name='subscription-status'),
]
