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


            day_range = key_stats.get('dayrange', {}).get('value', '0-0')
            fifty_two_week = key_stats.get('fiftyTwoWeekHighLow', {}).get('value', '0-0')
            daily_low, daily_high = cls.parse_range(day_range)
            yearly_low, yearly_high = cls.parse_range(fifty_two_week)


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
                if article.get('text'):
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


class FinancialMetricsParser(DataParser):
    """Parser for financial metrics and ratios"""

    @staticmethod
    def parse_news_items(news_data: List[Dict], num_items: int = 4) -> str:
        """Parse news items into a formatted string with headlines and summaries"""
        try:
            news_list = list(news_data)
            items_to_process = news_list[:num_items]

            output = ""
            for i, item in enumerate(items_to_process):
                if i > 0:
                    output += "\n\n"

                # Safely get headline and summary with defaults
                headline = item.get('headline', 'No headline available')
                summary = item.get('summary', 'No summary available')

                # Add formatted content
                output += f"HEADLINE: {headline}\n"
                output += f"SUMMARY: {summary}"
            print(output)
            return output if output else "No news items available"

        except (TypeError, AttributeError) as e:
            return "Invalid news data format"
        except Exception as e:
            return f"Error processing news data: {str(e)}"

    @classmethod
    def parse_alpha_vantage_income(cls, data: Dict) -> str:
        """Parse Alpha Vantage income statement data"""
        try:
            metrics = {
                'Total Revenue': cls._get_alpha_vantage_metric(data, 'totalRevenue'),
                'Gross Profit': cls._get_alpha_vantage_metric(data, 'grossProfit'),
                'Operating Income': cls._get_alpha_vantage_metric(data, 'operatingIncome'),
                'EBITDA': cls._get_alpha_vantage_metric(data, 'ebitda'),
                'Net Income': cls._get_alpha_vantage_metric(data, 'netIncome'),
                'Research and Development': cls._get_alpha_vantage_metric(data, 'researchAndDevelopment'),
                'Interest Expense': cls._get_alpha_vantage_metric(data, 'interestExpense'),
                'Cost of Revenue': cls._get_alpha_vantage_metric(data, 'costOfRevenue'),
                'Income Tax Expense': cls._get_alpha_vantage_metric(data, 'incomeTaxExpense')
            }

            return '\n'.join(f"{key}: {value}" for key, value in metrics.items() if value is not None)
        except Exception as e:
            logger.error(f"Error parsing Alpha Vantage income data: {str(e)}")
            return "Unable to parse income statement data"

    @classmethod
    def parse_finnhub_metrics(cls, data: Dict) -> str:
        """Parse Finnhub financial metrics data"""
        try:
            metrics = {
                '52 Week High/Low': cls._get_52_week_range(data),
                'Price Relative to S&P500': cls._get_price_relative_sp500(data),
                'Revenue Growth': cls._get_revenue_growth(data),
                'Earnings Growth': cls._get_earnings_growth(data),
                'PE Ratio': cls._get_pe_ratio(data),
                'PB Ratio': cls._get_pb_ratio(data),
                'PS Ratio': cls._get_ps_ratio(data),
                'Current/Quick Ratio': cls._get_current_quick_ratio(data),
                'Debt/Equity': cls._get_debt_equity_ratio(data),
                'Cash Flow per Share': cls._get_cash_flow_per_share(data),
                'Operating Margin': cls._get_operating_margin(data),
                'Net Profit Margin': cls._get_net_profit_margin(data),
                'Return on Equity': cls._get_return_on_equity(data),
                'Beta': cls._get_beta(data),
                'Net Interest Coverage': cls._get_net_interest_coverage(data),
                'Asset Turnover': cls._get_asset_turnover(data),
                'Inventory Turnover': cls._get_inventory_turnover(data),
                'Receivables Turnover': cls._get_receivables_turnover(data)
            }

            return '\n'.join(f"{key}: {value}" for key, value in metrics.items() if value is not None)
        except Exception as e:
            logger.error(f"Error parsing Finnhub metrics data: {str(e)}")
            return "Unable to parse financial metrics data"

    @staticmethod
    def _get_alpha_vantage_metric(data: Dict, metric_name: str) -> Optional[str]:

        try:
            value = data['annualReports'][0].get(metric_name)
            return str(value) if value is not None else None
        except (KeyError, IndexError):
            return None


    @staticmethod
    def _get_annual_metric(data: Dict, metric_name: str) -> Optional[str]:
        try:
            value = data['annualReports'][0].get(metric_name)
            return str(value) if value is not None else None
        except (KeyError, IndexError):
            return None

    @staticmethod
    def _get_metric_value(data: Dict, metric_name: str) -> Optional[float]:
        return data.get('metric', {}).get(metric_name)

    @classmethod
    def _get_52_week_range(cls, data: Dict) -> Optional[str]:
        high = cls._get_metric_value(data, '52WeekHigh')
        low = cls._get_metric_value(data, '52WeekLow')
        if high is not None and low is not None:
            return f"High: {high}, Low: {low}"
        return None

    @classmethod
    def _get_price_relative_sp500(cls, data: Dict) -> Optional[str]:
        timeframes = ['4Week', '13Week', '26Week', '52Week', 'Ytd']
        values = []
        for timeframe in timeframes:
            value = cls._get_metric_value(data, f'priceRelativeToS&P500{timeframe}')
            if value is not None:
                values.append(f"{timeframe}: {value}%")
        return ', '.join(values) if values else None

    @classmethod
    def _get_revenue_growth(cls, data: Dict) -> Optional[str]:
        metrics = {
            '3Y': cls._get_metric_value(data, 'revenueGrowth3Y'),
            '5Y': cls._get_metric_value(data, 'revenueGrowth5Y'),
            'Quarterly': cls._get_metric_value(data, 'revenueGrowthQuarterlyYoy'),
            'TTM': cls._get_metric_value(data, 'revenueGrowthTTMYoy')
        }
        values = [f"{k}: {v}%" for k, v in metrics.items() if v is not None]
        return ', '.join(values) if values else None

    @classmethod
    def _get_earnings_growth(cls, data: Dict) -> Optional[str]:
        metrics = {
            '3Y': cls._get_metric_value(data, 'epsGrowth3Y'),
            'Quarterly': cls._get_metric_value(data, 'epsGrowthQuarterlyYoy'),
            'TTM': cls._get_metric_value(data, 'epsGrowthTTMYoy')
        }
        values = [f"{k}: {v}%" for k, v in metrics.items() if v is not None]
        return ', '.join(values) if values else None

    @classmethod
    def _get_pe_ratio(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'peAnnual')
        ttm = cls._get_metric_value(data, 'peTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_pb_ratio(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'pbAnnual')
        quarterly = cls._get_metric_value(data, 'pbQuarterly')
        if annual is not None or quarterly is not None:
            return f"Annual: {annual}, Quarterly: {quarterly}"
        return None

    @classmethod
    def _get_ps_ratio(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'psAnnual')
        ttm = cls._get_metric_value(data, 'psTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_current_quick_ratio(cls, data: Dict) -> Optional[str]:
        current_annual = cls._get_metric_value(data, 'currentRatioAnnual')
        current_quarterly = cls._get_metric_value(data, 'currentRatioQuarterly')
        quick_annual = cls._get_metric_value(data, 'quickRatioAnnual')
        quick_quarterly = cls._get_metric_value(data, 'quickRatioQuarterly')

        parts = []
        if current_annual is not None or current_quarterly is not None:
            parts.append(f"Current Ratio - Annual: {current_annual}, Quarterly: {current_quarterly}")
        if quick_annual is not None or quick_quarterly is not None:
            parts.append(f"Quick Ratio - Annual: {quick_annual}, Quarterly: {quick_quarterly}")
        return '; '.join(parts) if parts else None

    @classmethod
    def _get_debt_equity_ratio(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'longTermDebt/equityAnnual')
        quarterly = cls._get_metric_value(data, 'longTermDebt/equityQuarterly')
        if annual is not None or quarterly is not None:
            return f"Annual: {annual}, Quarterly: {quarterly}"
        return None

    @classmethod
    def _get_cash_flow_per_share(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'cashFlowPerShareAnnual')
        quarterly = cls._get_metric_value(data, 'cashFlowPerShareQuarterly')
        ttm = cls._get_metric_value(data, 'cashFlowPerShareTTM')

        parts = []
        if any(v is not None for v in [annual, quarterly, ttm]):
            return f"Annual: {annual}, Quarterly: {quarterly}, TTM: {ttm}"
        return None

    @classmethod
    def _get_operating_margin(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'operatingMarginAnnual')
        ttm = cls._get_metric_value(data, 'operatingMarginTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_net_profit_margin(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'netProfitMarginAnnual')
        ttm = cls._get_metric_value(data, 'netProfitMarginTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_return_on_equity(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'roeAnnual')
        ttm = cls._get_metric_value(data, 'roeTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_beta(cls, data: Dict) -> Optional[str]:
        beta = cls._get_metric_value(data, 'beta')
        return str(beta) if beta is not None else None

    @classmethod
    def _get_net_interest_coverage(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'netInterestCoverageAnnual')
        ttm = cls._get_metric_value(data, 'netInterestCoverageTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_asset_turnover(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'assetTurnoverAnnual')
        ttm = cls._get_metric_value(data, 'assetTurnoverTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_inventory_turnover(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'inventoryTurnoverAnnual')
        ttm = cls._get_metric_value(data, 'inventoryTurnoverTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None

    @classmethod
    def _get_receivables_turnover(cls, data: Dict) -> Optional[str]:
        annual = cls._get_metric_value(data, 'receivablesTurnoverAnnual')
        ttm = cls._get_metric_value(data, 'receivablesTurnoverTTM')
        if annual is not None or ttm is not None:
            return f"Annual: {annual}, TTM: {ttm}"
        return None
