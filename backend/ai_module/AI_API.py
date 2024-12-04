# ai_module/AI_API.py
from ai_module.task_manager import TaskManager
import logging
from typing import Optional, Dict, ClassVar
from datetime import datetime
from ai_module.data_parsers import NewsParser

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
                    "Blogger": {"model": "gemini/gemini-1.5-flash", "base_url": " "}
                }
            )

            if success and self._task_manager.authenticate_backend("SuperAdmin", "password_123"):
                logger.info("TaskManager initialized and authenticated successfully")
                return True

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

            self.task_manager.set_company(symbol)
            research_tasks = self.task_manager._create_research_task()
            forecast = str(self.task_manager.ai_crew.kickoff(research_tasks))

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

            self.task_manager.set_company(symbol)
            self.task_manager.research_result = str(
                self.task_manager.ai_crew.kickoff(self.task_manager._create_research_task())
            )

            self.task_manager.calculation_result = str(
                self.task_manager.ai_crew.kickoff(self.task_manager._create_calculation_task())
            )

            risk_tasks = self.task_manager._create_risk_assessment_task()
            rating = str(self.task_manager.ai_crew.kickoff(risk_tasks)).strip()

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

    def check_health(self) -> Dict:
        """Check health status of the AI module"""
        try:
            has_task_manager = self._task_manager is not None
            return {
                "status": "healthy" if has_task_manager else "uninitialized",
                "task_manager_initialized": bool(has_task_manager and self._task_manager.ai_crew),
                "backend_authenticated": bool(
                    has_task_manager and
                    self._task_manager.backend_client and
                    self._task_manager.backend_client.token
                )
            }
        except Exception as e:
            logger.error(f"Error checking health: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    def test_forecast(self):
        """Test forecast generation for symbols"""
        print("\n=== Starting Forecast Test ===")

        test_symbols = ["AAPL"]

        for symbol in test_symbols:
            try:
                print(f"\nGenerating Forecast for {symbol}:")
                print("-" * 30)
                forecast = self.get_forecast("123", symbol, user_id=1)
                print("Forecast ID:", forecast['id'])
                print("User ID:", forecast['user_id'])
                print("\nForecast Preview:")
                print(forecast['forecast'][:500] + "..." if len(forecast['forecast']) > 500 else forecast['forecast'])

            except Exception as e:
                print(f"Error generating forecast for {symbol}: {e}")
                continue

        print("\n=== Forecast Test Complete ===")

    def test_trade_ratings(self):
        """Test trade ratings for multiple symbols"""
        print("\n=== Starting Trade Rating Test ===")

        test_symbols = ["AAPL"]

        for symbol in test_symbols:
            try:
                print(f"\nProcessing trade rating for {symbol}...")

                # Get and parse news data
                print(f"\nParsed News Data for {symbol}:")
                print("-" * 30)
                news_data = self.task_manager.backend_client.get_yahoo_news(symbol)
                news_parser = NewsParser()
                parsed_news = news_parser.parse_yahoo_news(news_data)
                news_context = news_parser.format_news_for_analysis(parsed_news)
                print(news_context)

                # Get the trade rating
                rating = self.get_trade_rating(symbol)

                print(f"""
    Rating Results:
    ------------------------
    Symbol: {rating['symbol']}
    Rating: {rating['rating']}
    Timestamp: {rating['timestamp']}
    User ID: {rating['user_id']}
    ------------------------""")

            except Exception as e:
                print(f"Error getting trade rating for {symbol}: {e}")
                continue

        print("\n=== Trade Rating Test Complete ===")

# Test functionality
if __name__ == "__main__":
    # Use singleton instance
    ai = AiAPI()

    # Initial health check
    health = ai.check_health()
    print("\nInitial Health Status:", health)

    try:
        # Run forecast test first
        ai.test_forecast()

        # Then run trade rating test
        ai.test_trade_ratings()

    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Final health check
        final_health = ai.check_health()
        print("\nFinal Health Status:", final_health)