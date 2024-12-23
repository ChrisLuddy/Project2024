from crewai_tools import BaseTool
from typing import ClassVar, Dict, Optional
from pydantic import Field


class StockDataTool(BaseTool):
    name: str = "StockDataTool"
    description: str = "Fetches relevant market data for stocks and cryptocurrencies based on user queries"


    AVAILABLE_STOCKS: ClassVar[Dict[str, str]] = {
        'AAPL': 'Apple',
        'GOOG': 'Google',
        'MSFT': 'Microsoft',
        'AMZN': 'Amazon',
        'TSLA': 'Tesla',
        'META': 'Meta',
        'NVDA': 'NVIDIA',
        'AMD': 'AMD',
        'INTC': 'Intel',
        'NFLX': 'Netflix',
        'SPOT': 'Spotify',
        'ORCL': 'Oracle',
        'CSCO': 'Cisco',
        'BTC': 'Bitcoin',
        'ETH': 'Ethereum',
        'XRP': 'Ripple'
    }

    CRYPTOCURRENCIES: ClassVar[Dict[str, str]] = {
        'BTC': 'Bitcoin',
        'ETH': 'Ethereum',
        'XRP': 'Ripple',
        'USDT': 'Tether',
        'BNB': 'Binance Coin',
        'ADA': 'Cardano',
        'SOL': 'Solana',
        'DOT': 'Polkadot',
        'DOGE': 'Dogecoin',
        'AVAX': 'Avalanche'
    }


    market_data: Optional[object] = Field(default=None, description="Market data interface")

    def __init__(self, market_data):
        super().__init__()
        self.market_data = market_data

    def _run(self, query: str) -> str:
        """
        Process the query and determine whether to fetch stock or crypto data
        """
        query_lower = query.lower()

        # Check for trending crypto request
        if any(phrase in query_lower for phrase in
               ['trending crypto', 'trending cryptocurrencies', 'hot crypto', 'popular crypto']):
            return self.get_trending_crypto()

        # Check for crypto-specific request
        if any(word in query_lower for word in ['crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'coin']):
            return self.get_crypto_data(query)

        # Default to stock data
        return self.get_stock_data(query)

    async def _arun(self, query: str) -> str:
        """Async version of run"""
        return self._run(query)

    def get_crypto_data(self, query: str) -> str:
        """
        Fetch cryptocurrency data based on the query
        """
        try:
            mentioned_cryptos = []
            query_upper = query.upper()

            # Check for specific crypto mentions
            for symbol, name in self.CRYPTOCURRENCIES.items():
                if symbol in query_upper or name.upper() in query_upper:
                    mentioned_cryptos.append(symbol)

            if not mentioned_cryptos:
                return "I couldn't identify any specific cryptocurrencies in your query. Available cryptocurrencies are: " + \
                    ", ".join([f"{symbol} ({name})" for symbol, name in self.CRYPTOCURRENCIES.items()])

            response = ""
            for symbol in mentioned_cryptos:
                # Get crypto data from market_data
                crypto_quote = self.market_data.get_crypto_quote(symbol)
                crypto_metrics = self.market_data.get_crypto_metrics(symbol)
                crypto_news = self.market_data.get_crypto_news(symbol)

                response += f"\nData for {self.CRYPTOCURRENCIES[symbol]} ({symbol}):\n"
                response += f"Current Price Data: {crypto_quote}\n"
                response += f"Key Metrics: {crypto_metrics}\n"

                # Add news if relevant to query
                if any(word in query.lower() for word in ['news', 'happening', 'recent']):
                    response += f"Recent News: {crypto_news}\n"

            return response

        except Exception as e:
            return f"Error fetching cryptocurrency data: {str(e)}"

    def get_trending_crypto(self) -> str:
        """
        Fetch data about trending cryptocurrencies
        """
        try:
            trending_data = self.market_data.get_trending_crypto()

            response = "🔥 Trending Cryptocurrencies:\n"

            if isinstance(trending_data, dict) and 'trending' in trending_data:
                for crypto in trending_data['trending']:
                    symbol = crypto.get('symbol', 'N/A')
                    name = crypto.get('name', 'N/A')
                    price_change = crypto.get('price_change_24h', 'N/A')
                    volume = crypto.get('volume_24h', 'N/A')

                    response += f"\n{name} ({symbol}):\n"
                    response += f"24h Price Change: {price_change}%\n"
                    response += f"24h Volume: ${volume:,.2f}\n"
            else:
                response += "Unable to fetch trending data at the moment.\n"

            response += "\nNote: Cryptocurrency markets can be highly volatile. Always conduct thorough research before making investment decisions."

            return response

        except Exception as e:
            return f"Error fetching trending cryptocurrency data: {str(e)}"

    def get_stock_data(self, query: str) -> str:
        """
        Fetch relevant stock data based on the query.
        """
        try:
            # Extract mentioned stocks
            mentioned_stocks = []
            query_upper = query.upper()

            # Check for exact symbol matches
            for symbol, company in self.AVAILABLE_STOCKS.items():
                if symbol in query_upper or company.upper() in query_upper:
                    mentioned_stocks.append(symbol)

            if not mentioned_stocks:
                return "I couldn't identify any specific stocks in your query. Available stocks are: " + \
                    ", ".join([f"{symbol} ({name})" for symbol, name in self.AVAILABLE_STOCKS.items()])

            response = ""
            for symbol in mentioned_stocks:
                # Fetch basic quote data
                quote = self.market_data.get_yahoo_finance_quote(symbol)
                analyst = self.market_data.get_yahoo_analyst_recommendations(symbol)

                # Format the response
                response += f"\nData for {self.AVAILABLE_STOCKS[symbol]} ({symbol}):\n"
                response += f"Quote Data: {quote}\n"
                response += f"Analyst Recommendations: {analyst}\n"

                # Add more specific data based on query keywords
                if any(word in query.lower() for word in ['price', 'worth', 'cost', 'value']):
                    price_data = self.market_data.get_alpha_vantage_price(symbol)
                    response += f"Price Information: {price_data}\n"

                if any(word in query.lower() for word in ['news', 'happening', 'recent']):
                    news = self.market_data.get_finnhub_news_formatted(symbol)
                    response += f"Recent News: {news}\n"

                if any(word in query.lower() for word in ['metric', 'performance', 'stat']):
                    metrics = self.market_data.get_finnhub_metrics_formatted(symbol)
                    response += f"Key Metrics: {metrics}\n"

            return response

        except Exception as e:
            return f"Error fetching stock data: {str(e)}"