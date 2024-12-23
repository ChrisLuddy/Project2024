# tests/test_firebase_crud.py
import os
import django
from datetime import datetime
from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Specify the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'act_backend.settings')

# Initialize Django
django.setup()

from core.firebase_models import Client, Fund, Portfolio, Asset, Order, TradeRating, AIForecast, SupportRequest

User = get_user_model()


class FirebaseCRUDTests(APITestCase):
    """
    Unified tests for Firebase models using CRUD operations.
    """

    def test_model_crud(self):
        """Run CRUD operations for all Firebase models."""
        models_to_test = [
            {
                'model': Client,
                'create_data': {'name': 'Test Client', 'fund_manager_id': 1},
                'update_data': {'name': 'Updated Test Client'},
            },
            {
                'model': Fund,
                'create_data': {'name': 'Test Fund', 'user_id': 1},
                'update_data': {'name': 'Updated Test Fund'},
            },
            {
                'model': Portfolio,
                'create_data': {'name': 'Test Portfolio', 'fund_id': 'test_fund_id'},
                'update_data': {'name': 'Updated Test Portfolio'},
            },
            {
                'model': Asset,
                'create_data': {
                    'symbol': 'AAPL',
                    'price': 150.0,
                    'volume': 1000,
                    'amount': 10,
                    'last_updated': datetime.now().isoformat(),
                    'portfolio_id': 'test_portfolio_id',
                },
                'update_data': {'price': 155.0},
            },
            {
                'model': Order,
                'create_data': {'amount': 5, 'order_type': 'buy', 'portfolio_id': 'test_portfolio_id'},
                'update_data': {'amount': 10},
            },
            {
                'model': TradeRating,
                'create_data': {'rating': 4.5, 'order_id': 'test_order_id'},
                'update_data': {'rating': 5.0},
            },
            {
                'model': AIForecast,
                'create_data': {'forecast': 'Positive', 'user_id': 1},
                'update_data': {'forecast': 'Negative'},
            },
            {
                'model': SupportRequest,
                'create_data': {'request': 'Need help with portfolio', 'user_id': 1},
                'update_data': {'request': 'Updated request for assistance'},
            },
        ]

        for model_data in models_to_test:
            self._test_single_model(
                model_class=model_data['model'],
                create_data=model_data['create_data'],
                update_data=model_data['update_data'],
            )

    def _test_single_model(self, model_class, create_data, update_data):
        """Test CRUD operations for a single model."""
        instance = model_class(**create_data)
        instance_id = instance.save()
        self.assertIsNotNone(instance_id, f"{model_class.__name__} creation failed.")

        retrieved_instance = model_class.get(instance_id)
        self.assertIsNotNone(retrieved_instance, f"{model_class.__name__} retrieval failed.")
        for key, value in create_data.items():
            self.assertEqual(retrieved_instance.get(key), value, f"{model_class.__name__} retrieval mismatch.")

        for key, value in update_data.items():
            setattr(instance, key, value)
        instance.update(instance_id)
        updated_instance = model_class.get(instance_id)
        for key, value in update_data.items():
            self.assertEqual(updated_instance.get(key), value, f"{model_class.__name__} update mismatch.")

        model_class.delete(instance_id)
        deleted_instance = model_class.get(instance_id)
        self.assertIsNone(deleted_instance, f"{model_class.__name__} deletion failed.")


class PermissionTests(APITestCase):
    """Tests for CRUD permissions based on user roles."""

    def setUp(self):
        self.fund_admin_user = User.objects.create_user(
            username='fund_admin',
            email='fund_admin@example.com',
            password='password123',
            role='fund_admin',
            is_active=True
        )
        self.fund_manager_user = User.objects.create_user(
            username='fund_manager',
            email='fund_manager@example.com',
            password='password123',
            role='fund_manager',
            is_active=True
        )

    def authenticate(self, user):
        """Authenticate user with JWT token."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_fund_manager_permissions(self):
        """Test FundManager access to fund-related endpoints."""
        self.authenticate(self.fund_manager_user)
        url = '/api/funds/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fund_admin_permissions(self):
        """Test FundAdmin denied access to fund-related endpoints."""
        self.authenticate(self.fund_admin_user)
        url = '/api/funds/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_permissions(self):
        """Test anonymous user access denial."""
        url = '/api/funds/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ExternalAPITests(APITestCase):
    """
    Tests for external API integrations (Stripe, Yahoo Finance).
    """

    def authenticate(self, user):
        """Authenticate user with JWT token."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    @patch('requests.get')
    def test_yahoo_finance_api(self, mock_get):
        """Test Yahoo Finance API integration."""
        mock_response = {
            "ticker": "AAPL",
            "price": 150.0,
            "change": -0.5,
            "currency": "USD"
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Authenticate user
        user = User.objects.create_user(
            username='fund_manager',
            email='fund_manager@example.com',
            password='password123',
            role='fund_manager',
            is_active=True
        )
        self.authenticate(user)

        url = '/api/yahoo-finance/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), mock_response)

    @patch('requests.get')
    def test_alpha_vantage_api(self, mock_get):
        """Test Alpha Vantage API integration."""
        mock_response = {
            "Meta Data": {"Symbol": "IBM"},
            "Time Series (Daily)": {
                "2024-12-22": {"1. open": "120.0", "2. high": "125.0", "3. low": "118.0", "4. close": "123.0"}
            }
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Authenticate user
        user = User.objects.create_user(
            username='fund_manager',
            email='fund_manager@example.com',
            password='password123',
            role='fund_manager',
            is_active=True
        )
        self.authenticate(user)

        url = '/api/alpha-vantage/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), mock_response)
