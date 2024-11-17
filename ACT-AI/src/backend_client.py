import requests
from datetime import datetime
import logging
from typing import Optional, Dict
from data_parsers import (
    MarketDataParser,
    TechnicalData,
    MarketPrice,
    TradingVolume,
    PriceRange,
    MarketStatus,
    ForecastData
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackendClient:
    def __init__(self, base_url: str = "http://161.35.38.50:8000"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.session = requests.Session()
        self.market_parser = MarketDataParser()

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with the backend"""
        try:
            response = requests.post(
                f"{self.base_url}/api/token/",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            tokens = response.json()
            self.token = tokens["access"]
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            logger.info("Successfully authenticated with backend")
            return True
        except requests.RequestException as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False

    def get_technical_analysis_data(self, symbol: str) -> Optional[Dict]:
        """
        Get combined technical analysis data including both real-time and historical
        Args:
            symbol: Stock symbol to analyze
        Returns:
            Optional[Dict]: Dictionary containing technical and historical data
        """
        try:
            # Get real-time market data
            yahoo_response = self.session.get(
                f"{self.base_url}/api/yahoo-finance/",
                params={"ticker": symbol}
            )
            yahoo_response.raise_for_status()
            yahoo_data = yahoo_response.json()
            technical_data = self.market_parser.parse_yahoo_finance_data(yahoo_data)

            # Get historical data
            alpha_response = self.session.get(
                f"{self.base_url}/api/alpha-vantage/",
                params={"symbol": symbol}
            )
            alpha_response.raise_for_status()
            historical_data = self.market_parser.parse_alpha_vantage_data(
                alpha_response.json()
            )

            if technical_data:
                return {
                    'technical': technical_data,
                    'historical': historical_data,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            return None

        except Exception as e:
            logger.error(f"Error fetching analysis data: {str(e)}")
            return None

    @staticmethod
    def format_technical_analysis(data: Dict) -> str:
        """
        Format technical analysis data into a readable string
        Args:
            data: Dictionary containing technical and historical data
        Returns:
            str: Formatted analysis string
        """
        if not data or 'technical' not in data:
            return "Technical analysis data unavailable"

        tech = data['technical']
        hist = data.get('historical', {})

        return f"""
REAL-TIME MARKET DATA:
Price Action:
- Current Price: ${tech.price.last_sale_price}
- Net Change: {tech.price.net_change} ({tech.price.percent_change}%)
- Bid/Ask Spread: ${tech.price.bid_price} / ${tech.price.ask_price}

Volume Analysis:
- Current Volume: {tech.volume.current_volume:,}
- Bid Size: {tech.volume.bid_size:,}
- Ask Size: {tech.volume.ask_size:,}

Trading Ranges:
- Today's Range: ${tech.ranges.daily_low} - ${tech.ranges.daily_high}
- 52-Week Range: ${tech.ranges.fifty_two_week_low} - ${tech.ranges.fifty_two_week_high}

Market Context:
- Exchange: {tech.status.exchange}
- Market Status: {tech.status.status}
- Data Type: {'Real-time' if tech.status.is_real_time else 'Delayed'}

RECENT HISTORICAL DATA:
{f'''- Date: {hist.get('date', 'N/A')}
- Open: ${hist.get('open', 'N/A')}
- High: ${hist.get('high', 'N/A')}
- Low: ${hist.get('low', 'N/A')}
- Close: ${hist.get('close', 'N/A')}
- Volume: {hist.get('volume', 'N/A'):,}''' if hist else 'Historical data unavailable'}
"""

    def get_market_data(self, symbol: str) -> Optional[TechnicalData]:
        """
        Get just the real-time market data
        Args:
            symbol: Stock symbol to analyze
        Returns:
            Optional[TechnicalData]: Parsed technical data
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/yahoo-finance/",
                params={"ticker": symbol}
            )
            response.raise_for_status()
            data = response.json()
            return self.market_parser.parse_yahoo_finance_data(data)
        except Exception as e:
            logger.error(f"Error fetching market data: {str(e)}")
            return None

    def get_historical_data(self, symbol: str) -> Optional[Dict]:
        """
        Get just the historical data
        Args:
            symbol: Stock symbol to analyze
        Returns:
            Optional[Dict]: Historical price data
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/alpha-vantage/",
                params={"symbol": symbol}
            )
            response.raise_for_status()
            data = response.json()
            return self.market_parser.parse_alpha_vantage_data(data)
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            return None

    def post_forecast(self, forecast_data: ForecastData, user_id: int) -> Optional[Dict]:
        """
        Send a formatted forecast to the backend

        Args:
            forecast_data: ForecastData object containing the analysis
            user_id: ID of the user generating the forecast

        Returns:
            Optional[Dict]: Response data containing forecast_id if successful
        """
        try:
            from data_parsers import ForecastParser
            forecast_text = ForecastParser.to_api_format(forecast_data)

            response = self.session.post(
                f"{self.base_url}/api/ai-forecasts/",
                json={
                    "forecast": forecast_text,
                    "user_id": user_id
                }
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Successfully posted forecast with ID: {result.get('forecast_id')}")
            return result

        except Exception as e:
            logger.error(f"Error posting forecast: {str(e)}")
            return None



def main():
    """
    Dummy test while External API data points are "N/A"
            """

    # Initialize the BackendClient
    client = BackendClient(base_url="http://161.35.38.50:8000")

    # Authenticate the user (replace with actual username and password)
    username = "SuperAdmin"
    password = "password_123"
    if not client.authenticate(username, password):
        logger.error("Authentication failed. Exiting.")
        return

    # Create dummy forecast data based on the provided structure
    forecast_data = ForecastData(
        technical_analysis="Based on the RSI and moving averages, the stock is in a bullish trend.",
        ai_analysis="The AI model predicts a 70% probability of the stock price increasing in the next week.",
        timestamp=datetime.now().isoformat(),
        symbol="AAPL"
    )

    # Post the forecast
    user_id = 123  # Replace with an actual user ID
    response = client.post_forecast(forecast_data, user_id)

    # Check the result
    if response:
        logger.info(f"Forecast posted successfully: {response}")
    else:
        logger.error("Failed to post the forecast.")

if __name__ == "__main__":
    main()