# act_ai/urls.py
from django.urls import path
from .views import PredictView, HistoryView, TradeRatingView, FinnhubStockDataView, FinnhubNewsView, CoinDataView, TrendingCoinsView, GeminiChatView

urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('history/', HistoryView.as_view(), name='history'),
    path('trade-rating/', TradeRatingView.as_view(), name='trade_rating'),
    path('stock-data/', FinnhubStockDataView.as_view(), name='stock_data'),
    path('stock-news/', FinnhubNewsView.as_view(), name='stock_news'),
    path('coin-data/', CoinDataView.as_view(), name='coin_data'),
    path('trending-coins/', TrendingCoinsView.as_view(), name='trending_coins'),
    path('chat/', GeminiChatView.as_view(), name='gemini_chat'),
]

