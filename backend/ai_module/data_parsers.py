# ai_module/data_parsers.py
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import json


"""
Refactored data parsing for API integration
"""

@dataclass
class MarketPrice:
    """Current market price data"""
    last_sale_price: float
    bid_price: float
    ask_price: float
    net_change: float
    percent_change: float
    timestamp: str


@dataclass
class TradingVolume:
    """Volume information"""
    current_volume: int
    bid_size: float
    ask_size: float


@dataclass
class PriceRange:
    """Price range information"""
    daily_low: float
    daily_high: float
    fifty_two_week_low: float
    fifty_two_week_high: float


@dataclass
class MarketStatus:
    """Market status information"""
    status: str
    stock_type: str
    exchange: str
    is_real_time: bool


@dataclass
class TechnicalData:
    """Combined technical analysis data"""
    price: MarketPrice
    volume: TradingVolume
    ranges: PriceRange
    status: MarketStatus


@dataclass
class ForecastData:
    """Forecast data structure"""
    technical_analysis: str
    ai_analysis: str
    timestamp: str
    symbol: str

@dataclass
class NewsData:
    """News data structure"""
    summary: str
    published_at: str
    source: str

class DataParser:
    """Base class for all data parsing operations"""

    @staticmethod
    def _safe_float(value: str) -> float:
        """Safely convert string to float"""
        try:
            return float(str(value).replace('$', '').replace(',', ''))
        except (ValueError, AttributeError):
            return 0.0

    @staticmethod
    def _safe_int(value: str) -> int:
        """Safely convert string to integer"""
        try:
            return int(str(value).replace(',', ''))
        except (ValueError, AttributeError):
            return 0


class MarketDataParser(DataParser):
    """Parser for market-related data"""

    @classmethod
    def parse_price(cls, price_str: str) -> float:
        """Parse price string to float"""
        return cls._safe_float(price_str)

    @classmethod
    def parse_volume(cls, volume_str: str) -> int:
        """Parse volume string to integer"""
        return cls._safe_int(volume_str)

    @classmethod
    def parse_percentage(cls, percentage_str: str) -> float:
        """Parse percentage string to float"""
        try:
            return cls._safe_float(percentage_str.replace('%', ''))
        except (ValueError, AttributeError):
            return 0.0

    @classmethod
    def parse_range(cls, range_str: str) -> Tuple[float, float]:
        """Parse range string to tuple of floats"""
        try:
            low, high = range_str.split(' - ')
            return cls._safe_float(low), cls._safe_float(high)
        except (ValueError, AttributeError):
            return 0.0, 0.0


    @classmethod
    def parse_yahoo_finance_data(cls, data: Dict) -> Optional[TechnicalData]:
        """Parse Yahoo Finance response into TechnicalData object"""
        try:
            body = data.get('body', {})
            primary = body.get('primaryData', {})
            key_stats = body.get('keyStats', {})

            # Parse ranges
            day_range = key_stats.get('dayrange', {}).get('value', '0-0')
            fifty_two_week = key_stats.get('fiftyTwoWeekHighLow', {}).get('value', '0-0')
            daily_low, daily_high = cls.parse_range(day_range)
            yearly_low, yearly_high = cls.parse_range(fifty_two_week)

            # Create data objects
            price = MarketPrice(
                last_sale_price=cls.parse_price(primary.get('lastSalePrice', '0')),
                bid_price=cls.parse_price(primary.get('bidPrice', '0')),
                ask_price=cls.parse_price(primary.get('askPrice', '0')),
                net_change=float(primary.get('netChange', 0)),
                percent_change=cls.parse_percentage(primary.get('percentageChange', '0%')),
                timestamp=primary.get('lastTradeTimestamp', '')
            )

            volume = TradingVolume(
                current_volume=cls.parse_volume(primary.get('volume', '0')),
                bid_size=float(primary.get('bidSize', 0)),
                ask_size=float(primary.get('askSize', 0))
            )

            ranges = PriceRange(
                daily_low=daily_low,
                daily_high=daily_high,
                fifty_two_week_low=yearly_low,
                fifty_two_week_high=yearly_high
            )

            status = MarketStatus(
                status=body.get('marketStatus', ''),
                stock_type=body.get('stockType', ''),
                exchange=body.get('exchange', ''),
                is_real_time=primary.get('isRealTime', False)
            )

            return TechnicalData(price, volume, ranges, status)

        except Exception as e:
            print(f"Error parsing Yahoo Finance data: {str(e)}")
            return None

    @classmethod
    def parse_alpha_vantage_data(cls, data: Dict) -> Optional[Dict]:
        """Parse Alpha Vantage response into structured format"""
        try:
            time_series = data.get('Time Series (Daily)', {})
            if not time_series:
                return None

            latest_date = next(iter(time_series))
            latest_data = time_series[latest_date]

            return {
                'date': latest_date,
                'open': cls._safe_float(latest_data.get('1. open', 0)),
                'high': cls._safe_float(latest_data.get('2. high', 0)),
                'low': cls._safe_float(latest_data.get('3. low', 0)),
                'close': cls._safe_float(latest_data.get('4. close', 0)),
                'volume': cls._safe_int(latest_data.get('5. volume', 0))
            }

        except Exception as e:
            print(f"Error parsing Alpha Vantage data: {str(e)}")
            return None


class NewsParser(DataParser):
    """Parser for news-related data"""

    @classmethod
    def parse_yahoo_news(cls, news_data: Dict, max_summaries: int = 5) -> List[NewsData]:
        """
        Parse Yahoo Finance news response into list of NewsData objects

        Args:
            news_data: Raw news data from Yahoo Finance API
            max_summaries: Maximum number of recent summaries to return (default: 5)

        Returns:
            List[NewsData]: List of parsed news data objects
        """
        try:
            parsed_news = []

            if not news_data or 'body' not in news_data:
                return []

            articles = news_data.get('body', [])

            for article in articles[:max_summaries]:
                if article.get('text'):  # Using 'text' field instead of 'summary'
                    news_item = NewsData(
                        summary=article.get('text', '').strip(),
                        published_at=article.get('time', ''),
                        source=article.get('source', '')
                    )
                    parsed_news.append(news_item)

            return parsed_news

        except Exception as e:
            print(f"Error parsing Yahoo news data: {str(e)}")
            return []

    @staticmethod
    def format_news_for_analysis(news_items: List[NewsData]) -> str:
        """
        Format parsed news items into a string for analysis

        Args:
            news_items: List of NewsData objects

        Returns:
            str: Formatted news summary string
        """
        if not news_items:
            return "No recent news available."

        formatted_news = []
        for item in news_items:
            formatted_news.append(f"""
Source: {item.source}
Published: {item.published_at}
Summary: {item.summary}
---""")

        return "\n".join(formatted_news)
class ForecastParser(DataParser):
    """Parser for forecast-related data"""

    @classmethod
    def format_forecast(cls, technical_data: Dict, analysis_text: str, symbol: str) -> ForecastData:
        """Format technical data and analysis into a forecast structure"""
        try:
            timestamp = datetime.now().isoformat()

            # Use existing MarketDataParser for technical analysis formatting
            market_parser = MarketDataParser()
            tech_analysis = market_parser.parse_yahoo_finance_data(technical_data) if technical_data else None
            formatted_tech = cls.format_technical_analysis(
                tech_analysis) if tech_analysis else "Technical data unavailable"

            return ForecastData(
                technical_analysis=formatted_tech,
                ai_analysis=analysis_text,
                timestamp=timestamp,
                symbol=symbol
            )

        except Exception as e:
            print(f"Error formatting forecast: {str(e)}")
            return None

    @staticmethod
    def format_technical_analysis(technical_data: TechnicalData) -> str:
        """Format TechnicalData into readable string"""
        if not technical_data:
            return "Technical data unavailable"

        return f"""
    REAL-TIME MARKET DATA:
    Price Action:
    - Current Price: ${technical_data.price.last_sale_price}
    - Net Change: {technical_data.price.net_change} ({technical_data.price.percent_change}%)
    - Bid/Ask Spread: ${technical_data.price.bid_price} / ${technical_data.price.ask_price}

    Volume Analysis:
    - Current Volume: {technical_data.volume.current_volume:,}
    - Bid Size: {technical_data.volume.bid_size:,}
    - Ask Size: {technical_data.volume.ask_size:,}

    Trading Ranges:
    - Today's Range: ${technical_data.ranges.daily_low} - ${technical_data.ranges.daily_high}
    - 52-Week Range: ${technical_data.ranges.fifty_two_week_low} - ${technical_data.ranges.fifty_two_week_high}

    Market Context:
    - Exchange: {technical_data.status.exchange}
    - Market Status: {technical_data.status.status}
    - Data Type: {'Real-time' if technical_data.status.is_real_time else 'Delayed'}
    """

    @staticmethod
    def to_api_format(forecast: ForecastData) -> str:
        """Convert ForecastData to API-compatible string format"""
        return f"""
STOCK ANALYSIS FOR: {forecast.symbol}
GENERATED: {forecast.timestamp}

{forecast.technical_analysis}

AI ANALYSIS AND RECOMMENDATIONS:
{forecast.ai_analysis}
"""


class GeneralDataParser(DataParser):
    """Parser for general data formats"""

    @classmethod
    def string_to_list(cls, input_str: str) -> list:
        """Convert a string formatted as a list into a Python list."""
        try:
            cleaned = input_str.strip('[]').strip()
            if not cleaned:
                return []

            items = [item.strip().strip("'\"") for item in cleaned.split(',')]
            return [cls._convert_numeric(item) for item in items]

        except Exception as e:
            print(f"Error converting string to list: {str(e)}")
            return []

    @classmethod
    def json_to_dict(cls, json_data: Union[str, bytes]) -> Dict:
        """Convert JSON data to Python dictionary."""
        try:
            if isinstance(json_data, (str, bytes)):
                try:
                    return json.loads(json_data)
                except json.JSONDecodeError:
                    with open(json_data, 'r') as file:
                        return json.load(file)
            raise ValueError("Input must be JSON string or file path")
        except Exception as e:
            raise Exception(f"Error parsing JSON data: {str(e)}")

    @classmethod
    def dict_to_json(cls, python_dict: Dict, file_path: Optional[str] = None, pretty: bool = True) -> str:
        """Convert Python dictionary to JSON string."""
        if not isinstance(python_dict, dict):
            raise TypeError("Input must be a dictionary")

        try:
            json_string = json.dumps(python_dict, indent=4 if pretty else None, sort_keys=True)
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(json_string)
            return json_string
        except Exception as e:
            raise Exception(f"Error converting dictionary to JSON: {str(e)}")

    @staticmethod
    def _convert_numeric(value: str) -> Union[int, float, str]:
        """Convert string to appropriate numeric type if possible."""
        try:
            if '.' not in value:
                return int(value)
            return float(value)
        except ValueError:
            return value

    class NewsParser(DataParser):
        """Parser for news-related data"""

        @classmethod
        def parse_yahoo_news(cls, news_data: Dict, max_summaries: int = 5) -> List[NewsData]:
            """
            Parse Yahoo Finance news response into list of NewsData objects

            Args:
                news_data: Raw news data from Yahoo Finance API
                max_summaries: Maximum number of summaries to return (default: 5)

            Returns:
                List[NewsData]: List of parsed news data objects
            """
            try:
                parsed_news = []

                if not news_data or 'articles' not in news_data:
                    return []

                articles = news_data.get('articles', [])

                for article in articles[:max_summaries]:
                    if article.get('summary'):
                        news_item = NewsData(
                            summary=article.get('summary', '').strip(),
                            published_at=article.get('published_at', ''),
                            source=article.get('source', '')
                        )
                        parsed_news.append(news_item)

                return parsed_news

            except Exception as e:
                print(f"Error parsing Yahoo news data: {str(e)}")
                return []

        @staticmethod
        def format_news_for_analysis(news_items: List[NewsData]) -> str:
            """
            Format parsed news items into a string for analysis

            Args:
                news_items: List of NewsData objects

            Returns:
                str: Formatted news summary string
            """
            if not news_items:
                return "No recent news available."

            formatted_news = []
            for item in news_items:
                formatted_news.append(f"""
    Source: {item.source}
    Published: {item.published_at}
    Summary: {item.summary}
    ---""")

            return "\n".join(formatted_news)

