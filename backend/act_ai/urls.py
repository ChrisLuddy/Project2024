# act_ai/urls.py
from django.urls import path
from .views import PredictView, HistoryView

urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('history/', HistoryView.as_view(), name='history'),
]

