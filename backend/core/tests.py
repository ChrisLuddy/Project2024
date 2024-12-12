# core/tests.py
import os
import django
import pytest


# Specify the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'act_backend.settings')

# Initialize Django
django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .firebase_models import Asset, Client, Fund, Portfolio, Order, TradeRating, AIForecast

User = get_user_model()

class FirebaseModelsTests(APITestCase):
    def setUp(self):
        # Create groups if not exist
        Group.objects.get_or_create(name='FundAdmin')
        Group.objects.get_or_create(name='FundManager')

        # Delete existing users to avoid UNIQUE constraint errors
        User.objects.filter(username='fund_admin').delete()
        User.objects.filter(username='fund_manager').delete()

        # Create fund admin user
        self.fund_admin_user = User.objects.create_user(username='fund_admin_unique', password='password123', role='fund_admin', is_active=True)
        fund_admin_group = Group.objects.get(name='FundAdmin')
        self.fund_admin_user.groups.add(fund_admin_group)

        # Create fund manager user
        self.fund_manager_user = User.objects.create_user(username='fund_manager_unique', password='password123', role='fund_manager', is_active=True)
        fund_manager_group = Group.objects.get(name='FundManager')
        self.fund_manager_user.groups.add(fund_manager_group)

        # Authenticate with JWT token for fund manager
        refresh = RefreshToken.for_user(self.fund_manager_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_client_crud_operations(self):
        # Create a client
        create_url = reverse('client-list-create')
        data = {"name": "Test Client", "fund_manager_id": self.fund_manager_user.id}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client_id = response.data['client_id']

        # Retrieve the client
        retrieve_url = reverse('client-detail', args=[client_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Client")

        # Update the client
        update_data = {"name": "Updated Test Client", "fund_manager_id": self.fund_manager_user.id}
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Test Client")

        # Delete the client
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fund_crud_operations(self):
        # Create a fund
        create_url = reverse('fund-list-create')
        data = {"name": "Test Fund", "user_id": self.fund_manager_user.id}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        fund_id = response.data['fund_id']

        # Retrieve the fund
        retrieve_url = reverse('fund-detail', args=[fund_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Fund")

        # Update the fund
        update_data = {"name": "Updated Test Fund", "user_id": self.fund_manager_user.id}
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Test Fund")

        # Delete the fund
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_asset_crud_operations(self):
        # Create an asset
        create_url = reverse('asset-list-create')
        data = {
            'symbol': 'AAPL',
            'price': 150.0,
            'volume': 10,
            'amount': 1500.0,
            'last_updated': '2023-12-01T00:00:00Z',
            'portfolio_id': 'portfolio_123'
        }
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        asset_id = response.data['asset_id']

        # Retrieve the asset
        retrieve_url = reverse('asset-detail', args=[asset_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], "AAPL")

        # Update the asset
        update_data = {
            'symbol': 'GOOGL',
            'price': 2000.0,
            'volume': 5,
            'amount': 10000.0,
            'last_updated': '2023-12-01T00:00:00Z',
            'portfolio_id': 'portfolio_123'
        }
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], "GOOGL")

        # Delete the asset
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_portfolio_crud_operations(self):
        # Create a portfolio
        create_url = reverse('portfolio-list-create')
        data = {"name": "Test Portfolio", "fund_id": "fund_123"}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        portfolio_id = response.data['portfolio_id']

        # Retrieve the portfolio
        retrieve_url = reverse('portfolio-detail', args=[portfolio_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Portfolio")

        # Update the portfolio
        update_data = {"name": "Updated Test Portfolio", "fund_id": "fund_123"}
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Test Portfolio")

        # Delete the portfolio
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_order_crud_operations(self):
        # Create an order
        create_url = reverse('order-list-create')
        data = {"amount": 100, "order_type": "buy", "portfolio_id": "portfolio_123"}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['order_id']

        # Retrieve the order
        retrieve_url = reverse('order-detail', args=[order_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], 100)

        # Update the order
        update_data = {"amount": 150, "order_type": "buy", "portfolio_id": "portfolio_123"}
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], 150)

        # Delete the order
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_trade_rating_crud_operations(self):
        # Create a trade rating
        create_url = reverse('trade-rating-list-create')
        data = {"rating": 5, "order_id": "order_123"}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        trade_rating_id = response.data['trade_rating_id']

        # Retrieve the trade rating
        retrieve_url = reverse('trade-rating-detail', args=[trade_rating_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 5)

        # Update the trade rating
        update_data = {"rating": 4, "order_id": "order_123"}
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4)

        # Delete the trade rating
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ai_forecast_crud_operations(self):
        # Create an AI forecast
        create_url = reverse('ai-forecast-list-create')
        data = {"forecast": "Positive", "user_id": self.fund_admin_user.id}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        forecast_id = response.data['forecast_id']

        # Retrieve the AI forecast
        retrieve_url = reverse('ai-forecast-detail', args=[forecast_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['forecast'], "Positive")

        # Update the AI forecast
        update_data = {"forecast": "Negative", "user_id": self.fund_admin_user.id}
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['forecast'], "Negative")

        # Delete the AI forecast
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_support_request_crud_operations(self):
        # Create a support request
        create_url = reverse('support-request-list-create')
        data = {"request": "Need help", "user_id": self.fund_admin_user.id}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        support_request_id = response.data['support_request_id']

        # Retrieve the support request
        retrieve_url = reverse('support-request-detail', args=[support_request_id])
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['request'], "Need help")

        # Update the support request
        update_data = {"request": "Updated request for assistance", "user_id": self.fund_admin_user.id}
        response = self.client.put(retrieve_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['request'], "Updated request for assistance")

        # Delete the support request
        response = self.client.delete(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class AccessDeniedTests(APITestCase):
    def setUp(self):
        # Create groups if not exist
        Group.objects.get_or_create(name='FundAdmin')

        # Create fund admin user
        self.fund_admin_user = User.objects.create_user(username='fund_admin_denied', password='password123', role='fund_admin')
        fund_admin_group = Group.objects.get(name='FundAdmin')
        self.fund_admin_user.groups.add(fund_admin_group)

        # Authenticate with JWT token for fund admin
        refresh = RefreshToken.for_user(self.fund_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_asset_view_access_denied(self):
        create_url = reverse('asset-list-create')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_view_access_denied(self):
        create_url = reverse('client-list-create')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fund_view_access_denied(self):
        create_url = reverse('fund-list-create')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
