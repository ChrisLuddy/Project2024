# core/urls.py
from django.urls import path
from .views import AssetList, YahooFinance, AlphaVantage, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('assets/', AssetList.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('yahoo-finance/', YahooFinance.as_view(), name='yahoo_finance'),
    path('alpha-vantage/', AlphaVantage.as_view(), name='alpha_vantage'),
    path('register/', RegisterView.as_view(), name='register'),
]
