# core/urls.py
from django.urls import path
from .views import AssetList

urlpatterns = [
    path('assets/', AssetList.as_view()),
]
