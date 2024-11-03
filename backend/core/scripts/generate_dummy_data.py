# core/scripts/generate_dummy_data.py
import django
import sys
import os

# Add the project root directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Set up Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'act_backend.settings')
django.setup()

# Import models from firebase_models
from core.firebase_models import Client, Fund, Portfolio, Asset, Order, TradeRating, AIForecast, SupportRequest

def generate_dummy_data():
    # Generate clients
    client1 = Client(name="Client Alpha", fund_manager_id=2)
    client1_id = client1.save()

    client2 = Client(name="Client Beta", fund_manager_id=4)
    client2_id = client2.save()

    client3 = Client(name="Client Gamma", fund_manager_id=2)
    client3_id = client3.save()

    # Generate funds
    fund1 = Fund(name="Tech Growth Fund", user_id=1, client_id=client1_id)
    fund1.save()

    fund2 = Fund(name="Healthcare Fund", user_id=3, client_id=client2_id)
    fund2.save()

    fund3 = Fund(name="Real Estate Fund", user_id=5, client_id=client3_id)
    fund3.save()

    # Generate portfolios
    portfolio1 = Portfolio(name="Alpha Portfolio", fund_id=fund1.save())
    portfolio1.save()

    portfolio2 = Portfolio(name="Beta Portfolio", fund_id=fund2.save())
    portfolio2.save()

    portfolio3 = Portfolio(name="Gamma Portfolio", fund_id=fund3.save())
    portfolio3.save()

    # Generate assets
    asset1 = Asset(symbol="AAPL", price=150.5, volume=2000, amount=100, last_updated=None, portfolio_id=portfolio1.save())
    asset1.save()

    asset2 = Asset(symbol="GOOGL", price=2800.5, volume=500, amount=20, last_updated=None, portfolio_id=portfolio2.save())
    asset2.save()

    asset3 = Asset(symbol="TSLA", price=750.5, volume=1200, amount=10, last_updated=None, portfolio_id=portfolio3.save())
    asset3.save()

    # Generate orders
    order1 = Order(order_type="buy", amount=50, portfolio_id=portfolio1.save())
    order1.save()

    order2 = Order(order_type="sell", amount=20, portfolio_id=portfolio2.save())
    order2.save()

    order3 = Order(order_type="buy", amount=10, portfolio_id=portfolio3.save())
    order3.save()

    # Generate trade ratings
    trade_rating1 = TradeRating(rating=4.5, order_id=order1.save())
    trade_rating1.save()

    trade_rating2 = TradeRating(rating=3.0, order_id=order2.save())
    trade_rating2.save()

    trade_rating3 = TradeRating(rating=5.0, order_id=order3.save())
    trade_rating3.save()

    # Generate AI forecasts
    ai_forecast1 = AIForecast(forecast="Positive", user_id=1)
    ai_forecast1.save()

    ai_forecast2 = AIForecast(forecast="Neutral", user_id=2)
    ai_forecast2.save()

    ai_forecast3 = AIForecast(forecast="Negative", user_id=3)
    ai_forecast3.save()

    # Generate support requests
    support_request1 = SupportRequest(request="Need assistance with portfolio setup", user_id=2)
    support_request1.save()

    support_request2 = SupportRequest(request="Issue with account login", user_id=3)
    support_request2.save()

    support_request3 = SupportRequest(request="Question about asset management", user_id=4)
    support_request3.save()

    print("Dummy data for Firebase generated successfully.")

if __name__ == "__main__":
    generate_dummy_data()
