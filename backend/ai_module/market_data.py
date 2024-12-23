import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Dict
from .data_parsers import (
    MarketDataParser,
    FinancialMetricsParser,
    TechnicalData,
    MarketPrice,
    TradingVolume,
    PriceRange,
    MarketStatus
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)


class MarketData:
    def __init__(self):
        self.market_parser = MarketDataParser()
        self.financial_parser = FinancialMetricsParser()
        self.RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
        self.RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')
        self.ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
        if not all([self.RAPIDAPI_KEY, self.RAPIDAPI_HOST, self.ALPHA_VANTAGE_API_KEY]):
            raise ValueError("Missing required API keys in environment variables")


    def get_finnhub_news_formatted(self, symbol: str, num_items: int = 4) -> str:
        """Get formatted news data from Finnhub"""
        try:

            today = datetime.now()

            from_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            to_date = today.strftime("%Y-%m-%d")

            news_data = self.get_finnhub_news(symbol, from_date, to_date)

            return self.financial_parser.parse_news_items(news_data, num_items)
        except Exception as e:
            logger.error(f"Error formatting Finnhub news: {str(e)}")
            return f"Error formatting Finnhub news: {str(e)}"

    def get_alpha_vantage_income_formatted(self, symbol: str) -> str:
        """Get formatted income statement data from Alpha Vantage"""
        try:
            income_data = self.get_alpha_vantage_income(symbol)
            return self.financial_parser.parse_alpha_vantage_income(income_data)
        except Exception as e:
            logger.error(f"Error formatting Alpha Vantage income statement: {str(e)}")
            return "Unable to retrieve income statement data"

    def get_finnhub_metrics_formatted(self, symbol: str) -> str:
        """Get formatted financial metrics from Finnhub"""
        try:
            metrics_data = self.get_finnhub_metrics(symbol)
            return self.financial_parser.parse_finnhub_metrics(metrics_data)
        except Exception as e:
            logger.error(f"Error formatting Finnhub metrics: {str(e)}")
            return "Unable to retrieve financial metrics"


    def get_coingecko_market_chart(self, coin_id, days):
        """
        Get cryptocurrency market chart data from CoinGecko API.

        Output Variables:
        - prices: Array of [timestamp, price]
        - market_caps: Array of [timestamp, market_cap]
        - total_volumes: Array of [timestamp, volume]

        Args:
            coin_id (str): CoinGecko coin ID (e.g., 'bitcoin')
            days (int): Number of days of data

        Returns:
            dict: Market chart data for specified cryptocurrency
        """
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "daily"
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to CoinGecko API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching market chart data: {e}")

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

    def get_coingecko_price(self, coin_id):
        """
        Get cryptocurrency price data from CoinGecko API.

        Output Variables:
        - crypto_price: Current price in USD
        - market_cap: Market capitalization
        - volume_24h: 24-hour trading volume
        - price_change_24h: 24-hour price change percentage

        Args:
            coin_id (str): CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')

        Returns:
            dict: Current price data for the specified cryptocurrency
        """
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true"
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to CoinGecko API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching crypto data: {e}")

    def get_yahoo_analyst_recommendations(self, symbol):
        """
        Get analyst recommendations from Yahoo Finance API.

        Output Variables:
        - analyst_target_price: Price target
        - buy_recommendations: Number of buy ratings
        - sell_recommendations: Number of sell ratings
        - hold_recommendations: Number of hold ratings
        - consensus_rating: Overall analyst consensus

        Args:
            symbol (str): Stock symbol

        Returns:
            dict: Analyst recommendation data
        """
        try:
            url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/modules"
            headers = {
                'X-RapidAPI-Key': self.RAPIDAPI_KEY,
                'X-RapidAPI-Host': self.RAPIDAPI_HOST
            }
            params = {
                "symbol": symbol,
                "type": "stock",
                "module": "recommendation-trend"
            }
            response = requests.get(url, headers=headers, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Yahoo Finance API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching analyst data: {e}")



    def get_yahoo_finance_quote(self, symbol):
        """
        Get quote data from Yahoo Finance API.

        Output Variables:
        - last_sale_price: Latest trading price
        - net_change: Price change
        - percentage_change: Percentage price change
        - volume: Trading volume
        - company_name: Full company name
        - exchange: Trading exchange

        Args:
            symbol (str): Stock symbol (e.g., 'IBM', 'MSFT')

        Returns:
            dict: Quote data for the specified symbol
        """
        try:
            url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/quote"
            headers = {
                'X-RapidAPI-Key': self.RAPIDAPI_KEY,
                'X-RapidAPI-Host': self.RAPIDAPI_HOST
            }

            params = {"ticker": symbol, "type": "STOCKS"}

            response = requests.get(url, headers=headers, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Yahoo Finance API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching Yahoo Finance data: {e}")


    def get_yahoo_insider_trading(self, symbol):
        """
        Get insider trading data from Yahoo Finance API.

        Output Variables:
        - insider_purchases: Recent insider buy transactions
        - insider_sales: Recent insider sell transactions
        - transaction_amounts: Transaction values

        Args:
            symbol (str): Stock symbol

        Returns:
            dict: Insider trading data
        """
        try:
            url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/insider-trades"
            headers = {
                'X-RapidAPI-Key': self.RAPIDAPI_KEY,
                'X-RapidAPI-Host': self.RAPIDAPI_HOST
            }
            params = {"symbol": symbol}
            response = requests.get(url, headers=headers, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Yahoo Finance API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching insider trading data: {e}")



    def get_finnhub_quote(self, symbol: str) -> Dict:
        """
        Get real-time quote data from Finnhub.

        Output Variables:
        - current_price (c): Current price
        - price_change (d): Price change
        - percent_change (dp): Percent change
        - high_price (h): High price of the day
        - low_price (l): Low price of the day
        - volume (v): Trading volume

        Args:
            symbol (str): Stock symbol

        Returns:
            dict: Quote data
        """
        try:
            api_key = os.getenv("FINNHUB_API_KEY")
            if not api_key:
                raise ValueError("FINNHUB_API_KEY not set in environment variables")

            base_url = "https://finnhub.io/api/v1/quote"
            url = f"{base_url}?symbol={symbol}&token={api_key}"

            logger.info(f"Fetching quote data for symbol: {symbol}")
            response = requests.get(url)
            response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching quote data for {symbol}: {e}", exc_info=True)
            return {"error": str(e)}


    def get_alpha_vantage_price(self, symbol):
        """
        Get current price data from Alpha Vantage API.

        Output Variables:
        - current_price: Current stock price
        - volume: Trading volume
        - price_change: Price change
        - price_change_percent: Percentage price change

        Args:
            symbol (str): Stock symbol (e.g., 'IBM', 'MSFT')

        Returns:
            dict: Current price data for the specified symbol
        """
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching price data: {e}")





    def get_alpha_vantage_daily(self, symbol, output_size="compact"):
        """
        Get daily time series data from Alpha Vantage API.

        Args:
            symbol (str): Stock symbol (e.g., 'IBM', 'MSFT')
            output_size (str): Data size - 'compact' or 'full'

        Returns:
            dict: Daily time series data for the specified symbol
        """
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.ALPHA_VANTAGE_API_KEY,
                "outputsize": output_size,
                "datatype": "json"
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching Alpha Vantage data: {e}")

        try:
            # Retrieve API key from environment variables
            api_key = os.getenv("FINNHUB_API_KEY")
            if not api_key:
                raise ValueError("FINNHUB_API_KEY is not set in the environment variables")

            # Construct the URL for the request
            base_url = "https://finnhub.io/api/v1/quote"
            url = f"{base_url}?symbol={symbol}&token={api_key}"

            logger.info(f"Fetching stock data for symbol: {symbol}")


            response = requests.get(url)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:

            logger.error(f"Error fetching stock data for symbol {symbol}: {e}", exc_info=True)
            return {"error": str(e)}

        except Exception as e:

            logger.error(f"Unexpected error in get_finnhub_stock_data: {e}", exc_info=True)
            return {"error": str(e)}



    def get_alpha_vantage_income(self, symbol):
        """
        Get income statement data from Alpha Vantage API.

        Output Variables:
        - net_income: Annual net income
        - previous_net_income: Previous year's net income
        - operating_income: Operating income
        - gross_profit: Gross profit

        Args:
            symbol (str): Stock symbol (e.g., 'IBM', 'MSFT')

        Returns:
            dict: Income statement data for the specified symbol
        """
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "INCOME_STATEMENT",
                "symbol": symbol,
                "apikey": self.ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching income data: {e}")




    def get_alpha_vantage_balance(self, symbol):
        """
        Get balance sheet data from Alpha Vantage API.

        Output Variables:
        - total_liabilities: Total company liabilities
        - total_shareholder_equity: Current shareholder equity
        - previous_shareholder_equity: Previous year's equity
        - total_assets: Total company assets

        Args:
            symbol (str): Stock symbol (e.g., 'IBM', 'MSFT')

        Returns:
            dict: Balance sheet data for the specified symbol
        """
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "BALANCE_SHEET",
                "symbol": symbol,
                "apikey": self.ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching balance sheet data: {e}")


    def get_alpha_vantage_earnings(self, symbol):
        """
        Get earnings data from Alpha Vantage API.

        Output Variables:
        - annual_eps: Current annual earnings per share
        - previous_eps: Previous year's EPS

        Args:
            symbol (str): Stock symbol (e.g., 'IBM', 'MSFT')

        Returns:
            dict: Earnings data for the specified symbol
        """
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "EARNINGS",
                "symbol": symbol,
                "apikey": self.ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Alpha Vantage API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching earnings data: {e}")


    def get_finnhub_news(self, symbol, from_date, to_date):
        """
        Get company news from Finnhub API.

        Output Variables:
        - headline: News headline
        - summary: News summary
        - url: News article URL
        - datetime: Publication datetime
        - source: News source

        Args:
            symbol (str): Stock symbol
            from_date (str): Start date (YYYY-MM-DD)
            to_date (str): End date (YYYY-MM-DD)

        Returns:
            dict: News data for the specified symbol and date range
        """
        try:
            url = "https://finnhub.io/api/v1/company-news"
            params = {
                "symbol": symbol,
                "from": from_date,
                "to": to_date,
                "token": self.FINNHUB_API_KEY
            }
            response = requests.get(url, params=params)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Finnhub API: {e}")
        except Exception as e:
            raise Exception(f"Error fetching news data: {e}")




    def get_finnhub_metrics(self, symbol: str) -> Dict:
        """
        Get financial metrics from Finnhub.

        Output Variables:
        - eps: Earnings per share
        - pe_ratio: Price to earnings ratio
        - roe: Return on equity
        - total_debt: Total debt
        - total_equity: Total shareholder equity

        Args:
            symbol (str): Stock symbol

        Returns:
            dict: Financial metrics
        """
        try:
            api_key = os.getenv("FINNHUB_API_KEY")
            if not api_key:
                raise ValueError("FINNHUB_API_KEY not set in environment variables")

            base_url = "https://finnhub.io/api/v1/stock/metric"
            url = f"{base_url}?symbol={symbol}&metric=all&token={api_key}"

            logger.info(f"Fetching financial metrics for symbol: {symbol}")
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching metrics for {symbol}: {e}", exc_info=True)
            return {"error": str(e)}


    def run_test_api(self):
        """
        Test function to verify API endpoints and data formatting.
        Tests both raw API responses and formatted parser outputs.
        """
        import logging


        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        def print_test_result(test_name: str, success: bool, data: dict = None, error: str = None):
            """Helper function to print test results in a consistent format"""
            print("\n" + "=" * 80)
            print(f"Test: {test_name}")
            print(f"Status: {'✓ SUCCESS' if success else '✗ FAILED'}")
            if error:
                print(f"Error: {error}")
            if data:
                print("Sample Data:")
                print(json.dumps(data, indent=2)[:500] + "..." if len(str(data)) > 500 else json.dumps(data, indent=2))
            print("=" * 80)

        # Initialize test parameters
        test_symbol = "AAPL"  # Using Apple as test stock
        test_coin = "bitcoin"
        today = datetime.now()
        week_ago = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        today_str = today.strftime('%Y-%m-%d')

        try:
            # 1. Test Alpha Vantage endpoints
            print("\nTesting Alpha Vantage APIs...")
            """
            try:
                # Test income statement with formatting
                income_data = self.get_alpha_vantage_income(test_symbol)
                formatted_income = self.get_alpha_vantage_income_formatted(test_symbol)
                print_test_result(
                    "Alpha Vantage Income Statement (Formatted)",
                    True,
                    {"raw": income_data, "formatted": formatted_income}
                )
            except Exception as e:
                print_test_result("Alpha Vantage Income Statement", False, error=str(e))

            try:
                # Test price data
                price_data = self.get_alpha_vantage_price(test_symbol)
                print_test_result("Alpha Vantage Price", True, price_data)
            except Exception as e:
                print_test_result("Alpha Vantage Price", False, error=str(e))
            """
            # 2. Test Yahoo Finance endpoints
            print("\nTesting Yahoo Finance APIs...")

            try:
                quote_data = self.get_yahoo_finance_quote(test_symbol)
                print_test_result("Yahoo Finance Quote", True, quote_data)
            except Exception as e:
                print_test_result("Yahoo Finance Quote", False, error=str(e))

            try:
                analyst_data = self.get_yahoo_analyst_recommendations(test_symbol)
                print_test_result("Yahoo Analyst Recommendations", True, analyst_data)
            except Exception as e:
                print_test_result("Yahoo Analyst Recommendations", False, error=str(e))

            try:
                insider_data = self.get_yahoo_insider_trading(test_symbol)
                print_test_result("Yahoo Insider Trading", True, insider_data)
            except Exception as e:
                print_test_result("Yahoo Insider Trading", False, error=str(e))

            # 3. Test Finnhub endpoints
            print("\nTesting Finnhub APIs...")

            try:
                # Test metrics with formatting
                metrics_data = self.get_finnhub_metrics(test_symbol)
                formatted_metrics = self.get_finnhub_metrics_formatted(test_symbol)
                print_test_result(
                    "Finnhub Metrics (Formatted)",
                    True,
                    {"raw": metrics_data, "formatted": formatted_metrics}
                )
            except Exception as e:
                print_test_result("Finnhub Metrics", False, error=str(e))

            try:
                quote_data = self.get_finnhub_quote(test_symbol)
                print_test_result("Finnhub Quote", True, quote_data)
            except Exception as e:
                print_test_result("Finnhub Quote", False, error=str(e))

            try:
                formatted_news = self.get_finnhub_news_formatted(test_symbol)
                print_test_result(
                    "Finnhub News",
                    True,
                    formatted_news
                )
            except Exception as e:
                print_test_result("Finnhub News", False, error=str(e))

            try:
                # Test metrics with formatting
                metrics_data = self.get_finnhub_metrics(test_symbol)
                formatted_metrics = self.get_finnhub_metrics_formatted(test_symbol)
                print_test_result(
                    "Finnhub Metrics (Formatted)",
                    True,
                    {"raw": metrics_data, "formatted": formatted_metrics}
                )
            except Exception as e:
                print_test_result("Finnhub Metrics", False, error=str(e))

            try:
                quote_data = self.get_finnhub_quote(test_symbol)
                print_test_result("Finnhub Quote", True, quote_data)
            except Exception as e:
                print_test_result("Finnhub Quote", False, error=str(e))

            # 4. Test CoinGecko endpoints
            print("\nTesting CoinGecko APIs...")

            try:
                price_data = self.get_coingecko_price(test_coin)
                print_test_result("CoinGecko Price", True, price_data)
            except Exception as e:
                print_test_result("CoinGecko Price", False, error=str(e))

            try:
                market_chart = self.get_coingecko_market_chart(test_coin, 7)
                print_test_result("CoinGecko Market Chart", True, market_chart)
            except Exception as e:
                print_test_result("CoinGecko Market Chart", False, error=str(e))

            try:
                trending_coins = self.get_coingecko_trending_coins()
                print_test_result("CoinGecko Trending Coins", True, trending_coins)
            except Exception as e:
                print_test_result("CoinGecko Trending Coins", False, error=str(e))

            # Print summary
            print("\nTest Suite Summary")
            print(datetime.now().strftime("Completed at: %Y-%m-%d %H:%M:%S"))
            print("Note: Some API calls may fail due to rate limiting - retry after a few minutes")

        except Exception as e:
            logger.error(f"Fatal error in test suite: {str(e)}", exc_info=True)
            print("\nTest suite failed to complete due to fatal error")
            print(f"Error: {str(e)}")



