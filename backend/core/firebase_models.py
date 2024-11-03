# core/firebase_models.py
from firebase_admin import firestore
from django.conf import settings
import firebase_admin
from datetime import datetime

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


class Client:
    def __init__(self, name, fund_manager_id):
        self.name = name
        self.fund_manager_id = fund_manager_id

    def save(self):
        client_ref = db.collection('clients').document()
        client_ref.set({
            'name': self.name,
            'fund_manager_id': self.fund_manager_id
        })
        return client_ref.id

    @staticmethod
    def get(client_id):
        client_ref = db.collection('clients').document(client_id)
        return client_ref.get().to_dict()

    def update(self, client_id):
        client_ref = db.collection('clients').document(client_id)
        client_ref.update({
            'name': self.name,
            'fund_manager_id': self.fund_manager_id
        })

    @staticmethod
    def delete(client_id):
        db.collection('clients').document(client_id).delete()

    @staticmethod
    def get_all():
        clients = db.collection('clients').stream()
        return [client.to_dict() for client in clients]


class Fund:
    def __init__(self, name, user_id=None, client_id=None):
        self.name = name
        self.user_id = user_id
        self.client_id = client_id

    def save(self):
        fund_ref = db.collection('funds').document()
        fund_ref.set({
            'name': self.name,
            'user_id': self.user_id,
            'client_id': self.client_id
        })
        return fund_ref.id

    @staticmethod
    def get(fund_id):
        fund_ref = db.collection('funds').document(fund_id)
        return fund_ref.get().to_dict()

    def update(self, fund_id):
        fund_ref = db.collection('funds').document(fund_id)
        fund_ref.update({
            'name': self.name,
            'user_id': self.user_id,
            'client_id': self.client_id
        })

    @staticmethod
    def delete(fund_id):
        db.collection('funds').document(fund_id).delete()

    @staticmethod
    def get_all():
        funds = db.collection('funds').stream()
        return [fund.to_dict() for fund in funds]


class Portfolio:
    def __init__(self, name, fund_id):
        self.name = name
        self.fund_id = fund_id

    def save(self):
        portfolio_ref = db.collection('portfolios').document()
        portfolio_ref.set({
            'name': self.name,
            'fund_id': self.fund_id
        })
        return portfolio_ref.id

    @staticmethod
    def get(portfolio_id):
        portfolio_ref = db.collection('portfolios').document(portfolio_id)
        return portfolio_ref.get().to_dict()

    def update(self, portfolio_id):
        portfolio_ref = db.collection('portfolios').document(portfolio_id)
        portfolio_ref.update({
            'name': self.name,
            'fund_id': self.fund_id
        })

    @staticmethod
    def delete(portfolio_id):
        db.collection('portfolios').document(portfolio_id).delete()

    @staticmethod
    def get_all():
        portfolios = db.collection('portfolios').stream()
        return [portfolio.to_dict() for portfolio in portfolios]


class Asset:
    def __init__(self, symbol, price, volume, amount, last_updated, portfolio_id):
        self.symbol = symbol
        self.price = price
        self.volume = volume
        self.amount = amount
        self.last_updated = last_updated or datetime.utcnow().isoformat()
        self.portfolio_id = portfolio_id

    def save(self):
        asset_ref = db.collection('assets').document()
        asset_ref.set({
            'symbol': self.symbol,
            'price': self.price,
            'volume': self.volume,
            'amount': self.amount,
            'last_updated': self.last_updated,
            'portfolio_id': self.portfolio_id
        })
        return asset_ref.id

    @staticmethod
    def get(asset_id):
        asset_ref = db.collection('assets').document(asset_id)
        return asset_ref.get().to_dict()

    def update(self, asset_id):
        asset_ref = db.collection('assets').document(asset_id)
        asset_ref.update({
            'symbol': self.symbol,
            'price': self.price,
            'volume': self.volume,
            'amount': self.amount,
            'last_updated': datetime.utcnow().isoformat(),
            'portfolio_id': self.portfolio_id
        })

    @staticmethod
    def delete(asset_id):
        db.collection('assets').document(asset_id).delete()

    @staticmethod
    def get_all():
        assets = db.collection('assets').stream()
        return [asset.to_dict() for asset in assets]


class Order:
    def __init__(self, amount, order_type, portfolio_id):
        self.amount = amount
        self.order_type = order_type
        self.portfolio_id = portfolio_id

    def save(self):
        order_ref = db.collection('orders').document()
        order_ref.set({
            'amount': self.amount,
            'order_type': self.order_type,
            'portfolio_id': self.portfolio_id
        })
        return order_ref.id

    @staticmethod
    def get(order_id):
        order_ref = db.collection('orders').document(order_id)
        return order_ref.get().to_dict()

    def update(self, order_id):
        order_ref = db.collection('orders').document(order_id)
        order_ref.update({
            'amount': self.amount,
            'order_type': self.order_type,
            'portfolio_id': self.portfolio_id
        })

    @staticmethod
    def delete(order_id):
        db.collection('orders').document(order_id).delete()

    @staticmethod
    def get_all():
        orders = db.collection('orders').stream()
        return [order.to_dict() for order in orders]


class TradeRating:
    def __init__(self, rating, order_id):
        self.rating = rating
        self.order_id = order_id

    def save(self):
        rating_ref = db.collection('trade_ratings').document()
        rating_ref.set({
            'rating': self.rating,
            'order_id': self.order_id
        })
        return rating_ref.id

    @staticmethod
    def get(rating_id):
        rating_ref = db.collection('trade_ratings').document(rating_id)
        return rating_ref.get().to_dict()

    def update(self, rating_id):
        rating_ref = db.collection('trade_ratings').document(rating_id)
        rating_ref.update({
            'rating': self.rating,
            'order_id': self.order_id
        })

    @staticmethod
    def delete(rating_id):
        db.collection('trade_ratings').document(rating_id).delete()

    @staticmethod
    def get_all():
        ratings = db.collection('trade_ratings').stream()
        return [rating.to_dict() for rating in ratings]


class AIForecast:
    def __init__(self, forecast, user_id):
        self.forecast = forecast
        self.user_id = user_id

    def save(self):
        forecast_ref = db.collection('ai_forecasts').document()
        forecast_ref.set({
            'forecast': self.forecast,
            'user_id': self.user_id
        })
        return forecast_ref.id

    @staticmethod
    def get(forecast_id):
        forecast_ref = db.collection('ai_forecasts').document(forecast_id)
        return forecast_ref.get().to_dict()

    def update(self, forecast_id):
        forecast_ref = db.collection('ai_forecasts').document(forecast_id)
        forecast_ref.update({
            'forecast': self.forecast,
            'user_id': self.user_id
        })

    @staticmethod
    def delete(forecast_id):
        db.collection('ai_forecasts').document(forecast_id).delete()

    @staticmethod
    def get_all():
        forecasts = db.collection('ai_forecasts').stream()
        return [forecast.to_dict() for forecast in forecasts]


class SupportRequest:
    def __init__(self, request, user_id):
        self.request = request
        self.user_id = user_id

    def save(self):
        request_ref = db.collection('support_requests').document()
        request_ref.set({
            'request': self.request,
            'user_id': self.user_id
        })
        return request_ref.id

    @staticmethod
    def get(request_id):
        request_ref = db.collection('support_requests').document(request_id)
        return request_ref.get().to_dict()

    def update(self, request_id):
        request_ref = db.collection('support_requests').document(request_id)
        request_ref.update({
            'request': self.request,
            'user_id': self.user_id
        })

    @staticmethod
    def delete(request_id):
        db.collection('support_requests').document(request_id).delete()

    @staticmethod
    def get_all():
        requests = db.collection('support_requests').stream()
        return [request.to_dict() for request in requests]
