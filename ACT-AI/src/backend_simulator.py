import requests
import time
import logging
from typing import Optional, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BackendSimulator:
    def __init__(self, ai_server_url: str = "http://localhost:5000"):
        self.ai_server_url = ai_server_url

    def check_ai_server_health(self) -> bool:
        """Check if AI server is running"""
        try:
            response = requests.get(f"{self.ai_server_url}/health")
            response.raise_for_status()
            logger.info("AI server is healthy!")
            return True
        except requests.RequestException as e:
            logger.error(f"AI server health check failed: {e}")
            return False

    def get_forecast(self, forecast_id: str, symbol: str = "AAPL") -> Optional[Dict]:
        """Get forecast from AI server"""
        try:
            logger.info(f"Requesting forecast {forecast_id} for symbol {symbol} from AI server...")
            response = requests.get(
                f"{self.ai_server_url}/ai/forecasts/{forecast_id}",
                params={"symbol": symbol}
            )

            if response.status_code != 200:
                logger.error(f"Server returned error {response.status_code}: {response.text}")
                return None

            data = response.json()

            logger.info(f"Received response for {symbol}")
            return data

        except requests.RequestException as e:
            logger.error(f"Error getting forecast: {e}")
            return None


def run_tests():
    """Run a series of test requests"""
    backend = BackendSimulator()

    # Test 1: Health Check
    print("\n=== Testing AI Server Health ===")
    if not backend.check_ai_server_health():
        print("AI server not responding. Make sure it's running!")
        return

    # Test 2: Get Various Forecasts
    print("\n=== Testing Forecast Requests ===")
    test_cases = [
        {"id": "123", "symbol": "AAPL"},
        {"id": "456", "symbol": "MSFT"},
    ]

    for case in test_cases:
        print(f"\nTesting forecast ID: {case['id']} for {case['symbol']}")
        result = backend.get_forecast(case['id'], case['symbol'])
        if result:
            print("\nSuccess! Received forecast:")
            print("=" * 50)
            print(f"Forecast ID: {result.get('id')}")
            print(f"User ID: {result.get('user_id')}")
            print("\nForecast Text Preview:")
            print("-" * 30)
            forecast_text = result.get('forecast', '')
            print(forecast_text[:500] + "..." if len(forecast_text) > 500 else forecast_text)
            print("=" * 50)
            print()
        else:
            print("Failed to get forecast")

        time.sleep(1)


if __name__ == "__main__":
    print("Starting backend simulator...")
    print("Make sure the AI server is running on http://localhost:5000")
    print("Press Ctrl+C to stop")

    try:
        run_tests()
    except KeyboardInterrupt:
        print("\nStopping backend simulator...")
    except Exception as e:
        print(f"\nError during simulation: {e}")