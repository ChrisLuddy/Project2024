from AI_Crew import AI_Crew
from market_data import MarketData
from data_parsers import ForecastParser, NewsParser
import logging
from datetime import datetime
from chatbot_tools import StockDataTool

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self, api_key=None, models_config=None):
        self.models_config = models_config
        self.api_key = api_key
        self.ai_crew = AI_Crew()
        self.results = {}
        self.calculation_result = None
        self.research_result = None
        self.market_data = MarketData()
        self.conversation_history = []
        self.stock_data_tool = StockDataTool(self.market_data)

    def _create_chat_task(self, user_message, context_data=None):
        """
        Create a chat interaction task that maintains context and provides informed responses.

        Args:
            user_message (str): The user's input message
            context_data (str, optional): Any relevant market data or analysis context
        """
        # Build context from conversation history and any available market data
        context = "\n".join(self.conversation_history[-5:])  # Last 5 messages for context
        if context_data:
            context += f"\n\nRelevant Market Data:\n{context_data}"

        return [self.ai_crew.create_task(
            agent=self.ai_crew.agents[4],
            description=f"""Respond to the following user message about the stock market.
                        You have access to a tool that can:
                        - Fetch real-time market data for stocks and cryptocurrencies
                        - Show trending cryptocurrencies and their performance
                        - Get detailed crypto market insights and metrics
                        - Provide latest news for both stocks and crypto
                        

               User Message: {user_message}

               Previous Conversation Context:
               {context}

               Guidelines:
               - Provide natural, conversational responses
               - Reference relevant market data when asked and available
               - Maintain conversation context
               - Explain complex concepts simply
               - Ask clarifying questions if needed
               - Stay focused on financial/market topics
                    Use your market data tool when:
                - Users ask about specific stocks or cryptocurrencies
                - Someone wants to know what's trending in crypto
                - Questions about market performance or news arise
                - Comparing different assets or markets"""
                ,
            expected_output="""A natural, informed response that:
               - Directly addresses the user's question/comment
               - Includes relevant market data when available
               - Maintains a conversational tone
               - Provides clear explanations
               - Asks follow-up questions if needed"""
        )]

    def process_chat_message(self, user_message):
        """
        Process a chat message and return a response.

        Args:
            user_message (str): The user's input message


        Returns:
            str: The chatbot's response
        """
        try:

            context_data = None

            # Create and execute chat task
            chat_task = self._create_chat_task(user_message, context_data)
            response = self.ai_crew.kickoff(chat_task)

            # Update conversation history
            self.conversation_history.append(f"User: {user_message}")
            self.conversation_history.append(f"Assistant: {response}")

            return response

        except Exception as e:
            print(f"Error in process_chat_message: {str(e)}")
            return "I apologize, but I encountered an error processing your message. Could you please try rephrasing or ask another question?"

    def _create_summarize_data_task(self, data):
        """Create a data summarization task"""
        return [self.ai_crew.create_task(
            agent=self.ai_crew.agents[3],
            description=f"Take the following data points related to  and summarize the data. The input may include information such as stock data, financials, and other relevant metrics. Your summary should include a clear and concise explanation of the company's recent performance, including stock price, changes, market details, and any financial highlights. Additionally, summarize any available news or recent events related to the company in natural language. \n {data}",
            expected_output=""" 
            Provide a concise and clear summary of the data. do NOT explain the data, just give bullet point facts.
             Do not add any additional financial information or give any notes, just forward the data in an extremely concise manner. Example:
            If the data is structued like : "symbol": "AAPL",
            "companyName": "Apple Inc. Common Stock",
            "stockType": "Common Stock",
            "exchange": "NASDAQ-GS",
            "primaryData": {
              "lastSalePrice": "$254.49",
              "netChange": "+4.70",
              "percentageChange": "+1.88%",
              "deltaIndicator": "up",
              "lastTradeTimestamp": "Dec 22, 2024",
              "isRealTime": false,
              "bidPrice": "N/A",
              "askPri..."
              Output :
            1. The company name is Apple Inc.
            2. The stock type is Common Stock.
            3. The exchange is NASDAQ-GS.
            4. The last sale price was $254.49.
            5. The stock price increased by $4.70, or 1.88%.
            6. The last trade occurred on December 22, 2024.
            7. The real-time data is unavailable.
            8. The bid price and ask price are not available.
        
            If the data includes news or financials, the summary should include:
            - Any relevant financial metrics or reports (e.g., net income, earnings).
            - A summary of recent news articles or significant events related to the company.
    """
        )]

    def _create_news_blog_task(self, news):
        """Create a news blogging task"""

        return [self.ai_crew.create_task(
            agent=self.ai_crew.agents[3],
            description=f"Take the following news articles related to the company's stock and create a short blog post. The blog should summarize the key points of the news in a concise and engaging manner, and provide a brief analysis of what this could mean for the company's future prospects, performance, or strategy. \n {news}",
            expected_output=""" 
            Provide a short blog post summarizing the news. Example:

            "Recent News: Apple Inc. has announced a major investment in renewable energy, partnering with several firms to create a new solar-powered manufacturing facility. This move aligns with their long-term sustainability goals and reinforces their commitment to reducing carbon emissions. Analysts believe this strategy could strengthen Apple's brand reputation and potentially attract more environmentally conscious consumers."

            Key requirements:
            - Summarize the main points of the news in an engaging manner.
            - Provide a brief analysis or opinion on how this news might impact the company (e.g., financial outlook, public perception, strategic goals).
            - Keep the tone professional yet accessible, suitable for a blog audience.
            """
        )]

    def _create_unique_research_task(self,data):
        """Create initial research tasks"""

        return  [self.ai_crew.create_task(
                agent=self.ai_crew.agents[0],
                description=f"Research the stock performance and recent news of the stock.Analyze the provided information for  ESPECIALLY for unique insights and relationships the data implies. the data to be analyzed is : {data}",
            expected_output=   """
                                Technical Analysis:
                                - Price Trends: Analyze recent price movements and significant patterns
                                - Volume Analysis: Examine trading volume trends and their implications
                                - Moving Averages: Key MA levels, crossovers, and support/resistance
                                - Momentum Indicators: RSI, MACD, and other relevant momentum signals
                                
                                Fundamental Analysis:
                                - Financial Metrics: Key ratios and their current implications
                                - Earnings Overview: Recent performance and future projections
                                - Market Position: Competitive standing and market share analysis
                                - Industry Context: Sector trends and company's relative position
                                
                                News Analysis:
                                - Recent Developments: Major news events and their impact
                                - Market Sentiment: Overall market perception and sentiment shifts
                                - Future Catalysts: Upcoming events that could affect the stock
                                
                                Unique Insights:
                                - Hidden Patterns: Non-obvious relationships in the data
                                - Risk Assessment: Underappreciated risk factors
                                - Opportunities: Unique potential based on data analysis
                                - Correlations: Notable relationships between different metrics
                                
                                Conclusion:
                                - Key Findings: Summary of most important discoveries
                                - Forward Outlook: Short and long-term projections
                                - Confidence Level: (1-10) with brief explanation
                               
                                
                                """
            )]



    def _create_trading_opportunity_research(self,data):


        return[ self.ai_crew.create_task (
            agent=self.ai_crew.agents[0],
            description=f"""Analyze short-term and long term trading opportunities for based on technical analysis. If it is wise to hold, buy or sell make a point of it. 

    
        
            Provide a detailed short-term trading analysis where you always explain your thought process WHY, covering:
        
            1. Price Action Analysis:
               - Current trend direction and strength
               - Price momentum indicators
               - Support/resistance levels from current price action
               - Significance of the current bid/ask spread
        
            2. Volume Analysis:
               - Volume trend analysis
               - Buying/selling pressure analysis
               - Volume-price relationship
               - Unusual volume activity assessment
        
            3. Trading Range Analysis:
               - Key levels within today's range
               - Position relative to 52-week range
               - Breakout/breakdown potential
               - Price volatility assessment
        
            4. Market Context:
               - Current market phase
               - Trading session analysis
               - Exchange-specific considerations
               - Real-time vs delayed data implications
        
            5. Short-term AND Longer term Opportunities:
               - Identified trading setups
               - Risk/reward scenarios
               - Entry/exit points
               - Stop-loss levels
               
               The data to be analyzed is: {data}
        
            Format each section clearly and provide specific price levels where applicable.""",
            expected_output=f""" T Provide a comprehensive short-term trading analysis with:
            1. Clear trend identification and direction
            2. Specific support and resistance levels
            3. Volume-based insights
            4. Concrete trading opportunities
            5. Risk management levels (entry, exit, stop-loss)
            6. Short-term price targets
            7. Confidence level in the analysis"""
                )]

    def _create_calculation_task(self):
        """Create calculation tasks with proper calculator format"""
        if not self.research_result:
            raise ValueError("Research result not available")

        current_time = datetime.now().strftime("%B %d, %Y, %I:%M %p GMT")

        return [
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[1],
                description="""Calculate key financial ratios using exact format:
                'Formula: [ratio_name] | Calculate: [numbers]'

                Required calculations:
                1. P/E Ratio: 'Formula: Price to Earnings | Calculate: [price] / [earnings]'
                2. Debt-to-Equity: 'Formula: Debt to Equity | Calculate: [total_debt] / [total_equity]'
                3. ROE: 'Formula: Return on Equity | Calculate: [net_income] / [equity]'

                If any data is unavailable, use:
                'Formula: [ratio_name] | Calculate: None'""",
                expected_output=f"""The time of analysis is : {current_time}. Provide each calculation result in sequence, one per line.
                Example:
                Result for Price to Earnings: 15.5
                Result for Debt to Equity: 0.8
                No data available for Return on Equity"""
            )
        ]

    def agent_data_cleaning(self, symbol: str):
        """
        Gathers all market data and cleans each piece individually before combining.
        """
        try:
            cleaned_data = ""
            news_data = ""

            # Ensure result is string
            def process_kickoff_result(result):
                return str(result)


            # Yahoo Finance Data
            yahoo_quote = self.market_data.get_yahoo_finance_quote(symbol)
            task = self._create_summarize_data_task(yahoo_quote)
            if task:  # Verify task was created successfully
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += process_kickoff_result(result)

            yahoo_analyst = self.market_data.get_yahoo_analyst_recommendations(symbol)
            task = self._create_summarize_data_task(yahoo_analyst)
            if task:
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += process_kickoff_result(result)

            yahoo_insider = self.market_data.get_yahoo_insider_trading(symbol)
            task = self._create_summarize_data_task(yahoo_insider)
            if task:
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += process_kickoff_result(result)

            # Finnhub Data
            finnhub_quote = self.market_data.get_finnhub_quote(symbol)
            task = self._create_summarize_data_task(finnhub_quote)
            if task:
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += process_kickoff_result(result)

            finnhub_metrics = self.market_data.get_finnhub_metrics_formatted(symbol)
            task = self._create_summarize_data_task(finnhub_metrics)
            if task:
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += process_kickoff_result(result)

            # Alpha Vantage Data
            alpha_income = self.market_data.get_alpha_vantage_income_formatted(symbol)
            task = self._create_summarize_data_task(alpha_income)
            if task:
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += process_kickoff_result(result)

            alpha_price = self.market_data.get_alpha_vantage_price(symbol)
            task = self._create_summarize_data_task(alpha_price)
            if task:
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += str(process_kickoff_result(result))
            print(cleaned_data)
            alpha_daily = self.market_data.get_alpha_vantage_daily(symbol)
            task = self._create_summarize_data_task(alpha_daily)
            if task:
                result = str(self.ai_crew.kickoff(task))
                cleaned_data += process_kickoff_result(result)

            # News data
            finnhub_news = self.market_data.get_finnhub_news_formatted(symbol)
            news_task = self._create_news_blog_task(finnhub_news)
            if news_task:
                news_result = str(self.ai_crew.kickoff(news_task))
                news_data = process_kickoff_result(news_result)

            # Combine all data
            combined_data = cleaned_data + news_data

            combined_data = combined_data
            print(combined_data)
            # Perform unique research
            research_task = self._create_unique_research_task(combined_data)
            research_result = str(self.ai_crew.kickoff(research_task))



            # Trading opportunity analysis
            trading_task = self._create_trading_opportunity_research(research_result)
            trading_result = str(self.ai_crew.kickoff(trading_task))




            return research_result,trading_result


        except Exception as e:
            print(f"Error in agent_data_cleaning: {str(e)}")
            import traceback
            traceback.print_exc()
            return "", "", ""




    def _create_trade_rating_task(self,data):
        """Create risk assessment tasks using all available data"""

        return  self.ai_crew.create_task(
                agent=self.ai_crew.agents[2],
                description=f"""Analyze risk factors and provide a binary risk assessment (POSITIVE/NEGATIVE) based on:

    1. Recent News Analysis:
    2. Research Analysis:
    3. Financial Calculations:
   

    Focus on the news summaries for sentiment analysis while considering quantitative data from research and calculations. the data to analyze is: {data}
                """,
                expected_output="POSITIVE or NEGATIVE as a single word response, indicating the overall risk assessment"
            )

    def _create_prediction_task(self, data):
        """Create prediction tasks using all available data"""

        return self.ai_crew.create_task(
            agent=self.ai_crew.agents[2],
            description=f"""Analyze all available data and generate a comprehensive price prediction. Use the following data for analysis:

    {data}

    Consider and analyze:
    1. Technical Indicators:
       - Current price trends and momentum
       - Support and resistance levels
       - Volume patterns and anomalies
       - Moving averages and key technical levels

    2. Fundamental Factors:
       - Recent financial metrics and ratios
       - Company performance indicators
       - Market position and competitive analysis
       - Industry trends and sector performance

    3. Market Sentiment:
       - News sentiment analysis
       - Trading patterns
       - Insider activity
       - Market psychology indicators

    4. Risk Factors:
       - Volatility measurements
       - Market conditions
       - Company-specific risks
       - External factors and potential catalysts

    Provide specific predictions for:
    - Short-term (1-5 days)
    - Medium-term (1-3 weeks)
    - Long-term (1-3 months)

    Include price targets, support/resistance levels, and confidence levels for each timeframe.""",

            expected_output="""
    Price Prediction Analysis:

    1. Short-term Outlook (1-5 days):
       - Price Target Range: [specific range]
       - Key Support Levels: [levels]
       - Key Resistance Levels: [levels]
       - Expected Volatility: [High/Medium/Low]
       - Confidence Level: [1-10]
       - Primary Drivers: [key factors]

    2. Medium-term Outlook (1-3 weeks):
       - Price Target Range: [specific range]
       - Key Support Levels: [levels]
       - Key Resistance Levels: [levels]
       - Expected Volatility: [High/Medium/Low]
       - Confidence Level: [1-10]
       - Primary Drivers: [key factors]

    3. Long-term Outlook (1-3 months):
       - Price Target Range: [specific range]
       - Key Support Levels: [levels]
       - Key Resistance Levels: [levels]
       - Expected Volatility: [High/Medium/Low]
       - Confidence Level: [1-10]
       - Primary Drivers: [key factors]

    4. Critical Levels:
       - Stop Loss Level: [price]
       - Take Profit Level: [price]
       - Key Breakout Level: [price]
       - Key Breakdown Level: [price]

    5. Prediction Confidence Matrix:
       Technical Analysis Confidence: [1-10]
       Fundamental Analysis Confidence: [1-10]
       Market Sentiment Confidence: [1-10]
       Overall Prediction Confidence: [1-10]

    6. Key Risk Factors:
       [List specific risks that could invalidate the prediction]

    7. Primary Catalysts:
       [List potential events/factors that could accelerate the predicted movement]

    Final Verdict:
    [Clear, concise statement of the overall prediction with primary reasoning]"""
        )

    def _is_crypto(self, symbol: str) -> bool:
        """
        Determine if the symbol is a cryptocurrency.
        """

        crypto_symbols = {'BTC', 'ETH', 'USDT', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL'}
        return symbol.upper() in crypto_symbols

    def get_crypto_market_data(self, symbol: str) -> str:
        """
        Gather all relevant crypto market data using market_data.py functions.
        Returns formatted string of combined data.
        """
        try:
            # Convert common symbols to CoinGecko format
            symbol_mapping = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'SOL': 'solana',
                'ADA': 'cardano',
                'XRP': 'ripple',
                'DOGE': 'dogecoin',
                'BNB': 'binancecoin',
                'USDT': 'tether'
            }

            coingecko_id = symbol_mapping.get(symbol.upper(), symbol.lower())

            # Get current price and market data
            price_data = self.market_data.get_coingecko_price(coingecko_id)

            # Get historical market chart data (30 days)
            market_chart = self.market_data.get_coingecko_market_chart(coingecko_id, 30)

            # Get trending coins data for market context
            trending_data = self.market_data.get_coingecko_trending_coins()

            # Combine all data into a formatted string
            combined_data = f"""
            Current Market Data for {symbol.upper()}:
            Price and Market Data: {price_data}

            Historical Chart Data (30 Days):
            {market_chart}

            Market Context and Trends:
            {trending_data}
            """

            return combined_data
        except Exception as e:
            print(f"Error gathering crypto market data: {str(e)}")
            return ""

    def _create_crypto_research_task(self, data):
        """Create research tasks specifically for cryptocurrencies"""
        return [self.ai_crew.create_task(
            agent=self.ai_crew.agents[0],
            description=f"""Research the cryptocurrency performance and market dynamics.
               Focus on crypto-specific metrics and indicators:

               1. Market Analysis:
               - Price action and volume patterns
               - Market dominance and relative strength
               - Network activity and on-chain metrics
               - Exchange inflows/outflows

               2. Technical Indicators:
               - Moving averages and trend analysis
               - RSI, MACD for crypto markets
               - Volume-weighted metrics
               - Network health indicators

               3. Market Sentiment:
               - Social media sentiment
               - Developer activity
               - Institutional interest
               - Regulatory developments

               4. Network Fundamentals:
               - Transaction volume and fees
               - Active addresses
               - Mining/staking statistics
               - Protocol updates and governance

               The data to analyze is: {data}""",
            expected_output="""
               Cryptocurrency Analysis Report:

               1. Market Performance:
               - Price trends and key levels
               - Volume analysis and liquidity depth
               - Market cap and dominance metrics
               - Exchange activity patterns

               2. Technical Overview:
               - Current trend direction and strength
               - Key support/resistance levels
               - Momentum indicators analysis
               - Volume profile assessment

               3. Market Sentiment Analysis:
               - Social sentiment metrics
               - Institutional flows
               - Development activity
               - Community growth/engagement

               4. Network Health:
               - Transaction metrics
               - Network security assessment
               - Protocol development status
               - Ecosystem growth indicators

               5. Risk Analysis:
               - Volatility assessment
               - Liquidity analysis
               - Regulatory considerations
               - Technical vulnerabilities

               6. Unique Insights:
               - Hidden patterns in data
               - Cross-market correlations
               - Anomaly detection
               - Forward-looking indicators
               """
        )]

    def _create_crypto_trading_task(self, data):
        """Create trading analysis task specifically for cryptocurrencies"""
        return [self.ai_crew.create_task(
            agent=self.ai_crew.agents[0],
            description=f"""Analyze trading opportunities in the cryptocurrency market:

               1. Market Structure Analysis:
               - Key price levels and market phases
               - Volume profile and liquidity zones
               - Exchange order book depth
               - Cross-exchange arbitrage opportunities

               2. Technical Trading Setups:
               - Entry and exit points
               - Risk management levels
               - Position sizing considerations
               - Multiple timeframe analysis

               3. Market Microstructure:
               - Exchange-specific dynamics
               - Spread analysis
               - Market making patterns
               - Institutional flow indicators

               4. Risk Assessment:
               - Volatility analysis
               - Liquidity risk
               - Counter-party risk
               - Regulatory risk

               The data to analyze is: {data}""",
            expected_output="""
               Cryptocurrency Trading Analysis:

               1. Market Position:
               - Current trend status
               - Key price levels
               - Volume analysis
               - Market dominance

               2. Trading Opportunities:
               - Entry points
               - Exit targets
               - Stop-loss levels
               - Position sizing recommendations

               3. Risk Management:
               - Volatility assessment
               - Liquidity analysis
               - Exchange considerations
               - Security factors

               4. Technical Levels:
               - Support zones
               - Resistance zones
               - Pivot points
               - Moving averages

               5. Market Context:
               - Correlation analysis
               - Market sentiment
               - On-chain metrics
               - Exchange flows
               """
        )]

    def process_prediction(self, symbol):
        """Process prediction for both crypto and stocks"""
        try:
            if self._is_crypto(symbol):
                # Get crypto market data
                market_data = self.get_crypto_market_data(symbol)

                # Create and execute crypto research task
                research_task = self._create_crypto_research_task(market_data)
                research_result = str(self.ai_crew.kickoff(research_task))

                # Create and execute prediction task using research results
                prediction_task = self._create_prediction_task(research_result)
                prediction_result = str(self.ai_crew.kickoff([prediction_task]))
            else:
                # Use stock prediction logic
                research_data, trading_data = self.agent_data_cleaning(symbol)
                prediction_task = self._create_prediction_task(research_data)
                prediction_result = str(self.ai_crew.kickoff([prediction_task]))

            return prediction_result

        except Exception as e:
            print(f"Error in process_prediction: {str(e)}")
            return ""

    def process_trade_rating(self, symbol):
        """Process trade rating for both crypto and stocks"""
        try:
            if self._is_crypto(symbol):
                # Get crypto market data
                market_data = self.get_crypto_market_data(symbol)

                # Create and execute crypto trading task
                trading_task = self._create_crypto_trading_task(market_data)
                trading_result = str(self.ai_crew.kickoff(trading_task))

                # Create and execute rating task using trading analysis
                rating_task = self._create_trade_rating_task(trading_result)
                rating_result = self.ai_crew.kickoff([rating_task])
            else:
                # Use stock rating logic
                research_data, trading_data = self.agent_data_cleaning(symbol)
                rating_task = self._create_trade_rating_task(trading_data)
                rating_result = self.ai_crew.kickoff([rating_task])

            return rating_result

        except Exception as e:
            print(f"Error in process_trade_rating: {str(e)}")
            return ""
