# core/management/commands/test_firebase_models.py
from django.core.management.base import BaseCommand
from core.firebase_models import Client, Fund, Portfolio, Asset, Order, TradeRating, AIForecast, SupportRequest
from datetime import datetime


class Command(BaseCommand):
    help = 'Test CRUD operations for Firebase models'

    def handle(self, *args, **kwargs):
        try:
            # Test Client
            client_data = {'name': 'Test Client', 'fund_manager_id': 1}
            client = Client(**client_data)
            client_id = client.save()
            self.stdout.write(self.style.SUCCESS(f'Client created with ID: {client_id}'))

            retrieved_client = Client.get(client_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved Client: {retrieved_client}'))

            client.name = 'Updated Test Client'
            client.update(client_id)
            self.stdout.write(self.style.SUCCESS(f'Updated Client: {Client.get(client_id)}'))

            client.delete(client_id)
            self.stdout.write(self.style.SUCCESS('Deleted Client'))

            # Test Fund
            fund_data = {'name': 'Test Fund', 'user_id': 1}
            fund = Fund(**fund_data)
            fund_id = fund.save()
            self.stdout.write(self.style.SUCCESS(f'Fund created with ID: {fund_id}'))

            retrieved_fund = Fund.get(fund_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved Fund: {retrieved_fund}'))

            fund.name = 'Updated Test Fund'
            fund.update(fund_id)
            self.stdout.write(self.style.SUCCESS(f'Updated Fund: {Fund.get(fund_id)}'))

            fund.delete(fund_id)
            self.stdout.write(self.style.SUCCESS('Deleted Fund'))

            # Test Portfolio
            portfolio_data = {'name': 'Test Portfolio', 'fund_id': fund_id}
            portfolio = Portfolio(**portfolio_data)
            portfolio_id = portfolio.save()
            self.stdout.write(self.style.SUCCESS(f'Portfolio created with ID: {portfolio_id}'))

            retrieved_portfolio = Portfolio.get(portfolio_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved Portfolio: {retrieved_portfolio}'))

            portfolio.name = 'Updated Test Portfolio'
            portfolio.update(portfolio_id)
            self.stdout.write(self.style.SUCCESS(f'Updated Portfolio: {Portfolio.get(portfolio_id)}'))

            portfolio.delete(portfolio_id)
            self.stdout.write(self.style.SUCCESS('Deleted Portfolio'))

            # Test Asset
            asset_data = {'symbol': 'AAPL', 'price': 150.0, 'volume': 1000, 'amount': 10,  'last_updated': datetime.now().isoformat(), 'portfolio_id': portfolio_id}
            asset = Asset(**asset_data)
            asset_id = asset.save()
            self.stdout.write(self.style.SUCCESS(f'Asset created with ID: {asset_id}'))

            retrieved_asset = Asset.get(asset_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved Asset: {retrieved_asset}'))

            asset.price = 155.0
            asset.update(asset_id)
            self.stdout.write(self.style.SUCCESS(f'Updated Asset: {Asset.get(asset_id)}'))

            asset.delete(asset_id)
            self.stdout.write(self.style.SUCCESS('Deleted Asset'))

            # Test Order
            order_data = {'amount': 5, 'order_type': 'buy', 'portfolio_id': portfolio_id}
            order = Order(**order_data)
            order_id = order.save()
            self.stdout.write(self.style.SUCCESS(f'Order created with ID: {order_id}'))

            retrieved_order = Order.get(order_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved Order: {retrieved_order}'))

            order.amount = 10
            order.update(order_id)
            self.stdout.write(self.style.SUCCESS(f'Updated Order: {Order.get(order_id)}'))

            order.delete(order_id)
            self.stdout.write(self.style.SUCCESS('Deleted Order'))

            # Test TradeRating
            trade_rating_data = {'rating': 4.5, 'order_id': order_id}
            trade_rating = TradeRating(**trade_rating_data)
            trade_rating_id = trade_rating.save()
            self.stdout.write(self.style.SUCCESS(f'TradeRating created with ID: {trade_rating_id}'))

            retrieved_trade_rating = TradeRating.get(trade_rating_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved TradeRating: {retrieved_trade_rating}'))

            trade_rating.rating = 5.0
            trade_rating.update(trade_rating_id)
            self.stdout.write(self.style.SUCCESS(f'Updated TradeRating: {TradeRating.get(trade_rating_id)}'))

            trade_rating.delete(trade_rating_id)
            self.stdout.write(self.style.SUCCESS('Deleted TradeRating'))

            # Test AIForecast
            ai_forecast_data = {'forecast': 'Positive', 'user_id': 1}
            ai_forecast = AIForecast(**ai_forecast_data)
            ai_forecast_id = ai_forecast.save()
            self.stdout.write(self.style.SUCCESS(f'AIForecast created with ID: {ai_forecast_id}'))

            retrieved_ai_forecast = AIForecast.get(ai_forecast_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved AIForecast: {retrieved_ai_forecast}'))

            ai_forecast.forecast = 'Negative'
            ai_forecast.update(ai_forecast_id)
            self.stdout.write(self.style.SUCCESS(f'Updated AIForecast: {AIForecast.get(ai_forecast_id)}'))

            ai_forecast.delete(ai_forecast_id)
            self.stdout.write(self.style.SUCCESS('Deleted AIForecast'))

            # Test SupportRequest
            support_request_data = {'request': 'Need help with portfolio', 'user_id': 1}
            support_request = SupportRequest(**support_request_data)
            support_request_id = support_request.save()
            self.stdout.write(self.style.SUCCESS(f'SupportRequest created with ID: {support_request_id}'))

            retrieved_support_request = SupportRequest.get(support_request_id)
            self.stdout.write(self.style.SUCCESS(f'Retrieved SupportRequest: {retrieved_support_request}'))

            support_request.request = 'Updated request for assistance'
            support_request.update(support_request_id)
            self.stdout.write(self.style.SUCCESS(f'Updated SupportRequest: {SupportRequest.get(support_request_id)}'))

            support_request.delete(support_request_id)
            self.stdout.write(self.style.SUCCESS('Deleted SupportRequest'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during CRUD operations: {e}'))
