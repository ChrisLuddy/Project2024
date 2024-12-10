# act_ai/urls.py
from django.urls import path
from .views import PredictView, HistoryView, TradeRatingView

urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('history/', HistoryView.as_view(), name='history'),
    path('trade-rating/', TradeRatingView.as_view(), name='trade_rating'),
]

