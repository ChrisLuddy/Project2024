from src.ai_server import task_manager
from task_manager import TaskManager
import logging
from typing import Optional, Dict, ClassVar
from datetime import datetime
from data_parsers import NewsParser
from market_data import MarketData
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AiAPI:
    _instance: ClassVar[Optional['AiAPI']] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._task_manager = None
            self._initialized = True

    @property
    def task_manager(self) -> TaskManager:
        """Lazy initialization of TaskManager"""
        if self._task_manager is None:
            self._task_manager = TaskManager()
            self._initialize_task_manager()
        return self._task_manager

    def _initialize_task_manager(self) -> bool:
        """Initialize and authenticate TaskManager"""
        try:
            success = self._task_manager.initialize_ai_crew(
                api_key=" ",
                models_config={
                    "Researcher": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
                    "Accountant": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
                    "Recommender": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
                    "Blogger": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
                    "Chatbot": {"model": "gemini/gemini-1.5-flash", "base_url": " "}
                }
            )



            logger.error("Failed to initialize TaskManager")
            return False

        except Exception as e:
            logger.error(f"Error during TaskManager initialization: {str(e)}")
            return False

    def get_forecast(self, forecast_id: str, symbol: str, user_id: int = 1) -> Dict:
        """Get forecast by ID and symbol"""
        try:
            if not symbol:
                raise ValueError("Symbol parameter is required")

            logger.info(f"Processing forecast request - ID: {forecast_id}, Symbol: {symbol}")



            forecast = task_manager.process_prediction(symbol)

            return {
                "id": int(forecast_id) if forecast_id.isdigit() else 1,
                "forecast": forecast,
                "user_id": user_id
            }

        except Exception as e:
            logger.error(f"Error processing forecast request: {e}", exc_info=True)
            raise

    def get_trade_rating(self, symbol: str, user_id: int = 1) -> Dict:
        """Get trade rating based on news and technical analysis"""
        try:
            if not symbol:
                raise ValueError("Symbol parameter is required")

            logger.info(f"Processing trade rating request - Symbol: {symbol}")



            rating = task_manager.process_trade_rating(symbol)

            if rating not in ["POSITIVE", "NEGATIVE"]:
                logger.warning(f"Unexpected rating value: {rating}, defaulting to NEGATIVE")
                rating = "NEGATIVE"

            return {
                "symbol": symbol,
                "rating": rating,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id
            }

        except Exception as e:
            logger.error(f"Error processing trade rating request: {e}", exc_info=True)
            raise

    def get_chat(self, message: str, user_id: int = 1) -> Dict:
        """Process a chat message and return the response

        Args:
            message (str): The user's chat message
            user_id (int): User identifier, defaults to 1

        Returns:
            Dict: Contains response and metadata
        """
        try:
            if not message:
                raise ValueError("Message parameter is required")

            logger.info(f"Processing chat message - User ID: {user_id}")

            response = task_manager.process_chat_message(message)

            return {
                "message": message,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id
            }

        except Exception as e:
            logger.error(f"Error processing chat message: {e}", exc_info=True)
            raise

    def test_crypto_forecast(self):
        """Test forecast generation for cryptocurrencies"""
        print("\n=== Starting Crypto Forecast Test ===")

        test_symbols = ["BTC", "ETH", "SOL"]  # Test multiple crypto symbols

        for symbol in test_symbols:
            try:
                print(f"\nGenerating Forecast for {symbol}:")
                print("-" * 50)
                forecast = self.get_forecast("123", symbol, user_id=1)
                print(f"Symbol: {symbol}")
                print("Forecast ID:", forecast['id'])
                print("User ID:", forecast['user_id'])
                print("\nForecast Details:")
                print(forecast['forecast'])
                print("-" * 50)

            except Exception as e:
                print(f"Error generating forecast for {symbol}: {e}")
                continue

        print("\n=== Crypto Forecast Test Complete ===\n")

    def test_crypto_trade_rating(self):
        """Test trade rating generation for cryptocurrencies"""
        print("\n=== Starting Crypto Trade Rating Test ===")

        test_symbols = ["BTC", "ETH", "XRP"]  # Test the cryptos

        for symbol in test_symbols:
            try:
                print(f"\nGenerating Trade Rating for {symbol}:")
                print("-" * 50)
                rating = self.get_trade_rating(symbol, user_id=1)
                print(f"Symbol: {symbol}")
                print("Rating:", rating['rating'])
                print("Timestamp:", rating['timestamp'])
                print("User ID:", rating['user_id'])
                print("-" * 50)

            except Exception as e:
                print(f"Error generating trade rating for {symbol}: {e}")
                continue

        print("\n=== Crypto Trade Rating Test Complete ===\n")

    def test_stock_forecast(self):
        """Test forecast generation for stocks"""
        print("\n=== Starting Stock Forecast Test ===")

        test_symbols = ["AAPL", "TSLA", "MSFT"]  # Test multiple stock symbols

        for symbol in test_symbols:
            try:
                print(f"\nGenerating Forecast for {symbol}:")
                print("-" * 50)
                forecast = self.get_forecast("123", symbol, user_id=1)
                print(f"Symbol: {symbol}")
                print("Forecast ID:", forecast['id'])
                print("User ID:", forecast['user_id'])
                print("\nForecast Details:")
                print(forecast['forecast'])
                print("-" * 50)

            except Exception as e:
                print(f"Error generating forecast for {symbol}: {e}")
                continue

        print("\n=== Stock Forecast Test Complete ===\n")

    def test_stock_trade_rating(self):
        """Test trade rating generation for stocks"""
        print("\n=== Starting Stock Trade Rating Test ===")

        test_symbols = ["AAPL", "TSLA", "MSFT"]  # Test multiple stock symbols

        for symbol in test_symbols:
            try:
                print(f"\nGenerating Trade Rating for {symbol}:")
                print("-" * 50)
                rating = self.get_trade_rating(symbol, user_id=1)
                print(f"Symbol: {symbol}")
                print("Rating:", rating['rating'])
                print("Timestamp:", rating['timestamp'])
                print("User ID:", rating['user_id'])
                print("-" * 50)

            except Exception as e:
                print(f"Error generating trade rating for {symbol}: {e}")
                continue

        print("\n=== Stock Trade Rating Test Complete ===\n")

    def test_chat(self):
        """Test chat functionality with sample messages"""
        print("\n=== Starting Chat Test ===")

        test_messages = [
            "What's the current price of Bitcoin?",
            "How is Ethereum performing today?",
            "Tell me about Apple stock's latest performance",
            "What's the forecast for Tesla stock?",
            "Compare Bitcoin and Ethereum performance",
            "What are the trending cryptocurrencies right now?",
            "Give me a technical analysis of AAPL",
            "Should I invest in SOL?",
            "What's the market sentiment for MSFT?"
        ]

        for message in test_messages:
            try:
                print(f"\nProcessing message: '{message}'")
                print("-" * 50)
                chat_response = self.get_chat(message=message, user_id=1)

                print("\nResponse Details:")
                print(f"Timestamp: {chat_response['timestamp']}")
                print(f"User ID: {chat_response['user_id']}")
                print("\nBot Response:")
                print(chat_response['response'])
                print("-" * 50)

            except Exception as e:
                print(f"Error processing message '{message}': {e}")
                continue

        print("\n=== Chat Test Complete ===")

    def run_all_tests(self):
        """Run all tests in sequence"""
        try:
            print("\n========== Starting All Tests ==========")

            # Test crypto functionality
            self.test_crypto_forecast()
            self.test_crypto_trade_rating()

            # Test stock functionality
            self.test_stock_forecast()
            self.test_stock_trade_rating()

            # Test chat functionality
            self.test_chat()

            print("\n========== All Tests Complete ==========")

        except Exception as e:
            print(f"Error during testing: {e}")


    """OLD APIS --- SHOULD BE DELETED WHEN BACKEND MIGRATES """
    def get_finnhub_stock_data(self, symbol: str) -> Dict:
        """
        Fetch stock market data for a given symbol using Finnhub API.
        """

        try:
            # Retrieve API key from environment variables
            api_key = os.getenv("FINNHUB_API_KEY")
            if not api_key:
                raise ValueError("FINNHUB_API_KEY is not set in the environment variables")

            # Construct the URL for the request
            base_url = "https://finnhub.io/api/v1/quote"
            url = f"{base_url}?symbol={symbol}&token={api_key}"

            logger.info(f"Fetching stock data for symbol: {symbol}")

            # Execute the API request
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            return response.json()

        except requests.exceptions.RequestException as e:
            # Log any HTTP request errors
            logger.error(f"Error fetching stock data for symbol {symbol}: {e}", exc_info=True)
            return {"error": str(e)}

        except Exception as e:
            # Log any unexpected errors
            logger.error(f"Unexpected error in get_finnhub_stock_data: {e}", exc_info=True)
            return {"error": str(e)}

    def get_finnhub_news(self, category: str = "general") -> List[Dict]:
        """
        Fetch news from Finnhub API.
        """
        try:
            # Retrieve API key from environment variables
            api_key = os.getenv("FINNHUB_API_KEY")
            if not api_key:
                raise ValueError("FINNHUB_API_KEY is not set in the environment variables")

            # Construct the URL for the request
            base_url = "https://finnhub.io/api/v1/news"
            url = f"{base_url}?category={category}&token={api_key}"

            logger.info(f"Fetching Finnhub news for category: {category}")

            # Execute the API request
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            return response.json()

        except requests.exceptions.RequestException as e:
            # Log any HTTP request errors
            logger.error(f"Error fetching news for category {category}: {e}", exc_info=True)
            return {"error": str(e)}

        except Exception as e:
            # Log any unexpected errors
            logger.error(f"Unexpected error in get_finnhub_news: {e}", exc_info=True)
            return {"error": str(e)}

    def get_coingecko_coin_data(self, coin_id: str = "bitcoin") -> Dict:
        """
        Fetch cryptocurrency data for a given coin ID using CoinGecko API.
        """
        try:
            base_url = "https://api.coingecko.com/api/v3/coins"
            url = f"{base_url}/{coin_id}"

            logger.info(f"Fetching CoinGecko data for coin: {coin_id}")
            response = requests.get(url)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.error(f"Error fetching CoinGecko coin data: {e}", exc_info=True)
            raise

    def get_coingecko_trending_coins(self) -> Dict:
        """
        Fetch trending cryptocurrencies using CoinGecko API.
        """
        try:
            base_url = "https://api.coingecko.com/api/v3/search/trending"

            logger.info("Fetching trending cryptocurrencies from CoinGecko")
            response = requests.get(base_url)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.error(f"Error fetching CoinGecko trending coins: {e}", exc_info=True)
            raise



# Test functionality
if __name__ == "__main__":
    ai = AiAPI()
    ai.run_all_tests()
