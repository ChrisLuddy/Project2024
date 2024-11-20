from AI_Crew import AI_Crew
from backend_client import BackendClient
from data_parsers import ForecastParser
import logging

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self, api_key=None, models_config=None):
        self.models_config = models_config
        self.api_key = api_key
        self.ai_crew = None
        self.results = {}
        self.company = None
        self.calculation_result = None
        self.research_result = None
        self.backend_client = None

    def initialize_ai_crew(self, api_key=None, models_config=None):
        """Initialize or update AI Crew configuration"""
        if api_key:
            self.api_key = api_key
        if models_config:
            self.models_config = models_config

        if self.api_key and self.models_config:
            self.ai_crew = AI_Crew(self.api_key, self.models_config)
            self.backend_client = BackendClient()
            return True
        return False

    def authenticate_backend(self, username: str, password: str) -> bool:
        """Authenticate with the backend"""
        if self.backend_client:
            return self.backend_client.authenticate(username, password)
        return False

    def set_company(self, company_name):
        """Set company name for analysis"""
        self.company = company_name

    def get_required_variables(self, initial_check=True):
        """Return list of required variables for task execution
        initial_check: if True, only check company and ai_crew initialization"""
        if initial_check:
            return {
                'company': self.company,
                'ai_crew_initialized': bool(self.ai_crew)
            }
        else:
            return {
                'company': self.company,
                'research_result': self.research_result,
                'calculation_result': self.calculation_result,
                'ai_crew_initialized': bool(self.ai_crew)
            }

    def _create_research_task(self):
        """Create initial research tasks"""
        if not self.company:
            raise ValueError("Company name not set")

        # Get technical analysis data
        analysis_data = self.backend_client.get_technical_analysis_data(self.company)
        market_context = self.backend_client.format_technical_analysis(analysis_data)

        return [
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[0],
                description=f"Research the stock performance and recent news of {self.company}.",
                expected_output="Provide a summary of stock's recent performance, financials, and news articles."
            ),
            # Needs additional API endpoints for accurate data
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[0],
                description="""Find the following specific financial numbers from the investigated stock:
                1. Current stock price
                2. Earnings Per Share (EPS)
                3. Total Liabilities/Debt
                4. Total Shareholder Equity
                5. Net Income
                6. Previous year's Shareholder Equity (for average calculation)

                Add any other relevant statistics previously discovered.

                Format the numbers clearly and explain the time period each number represents (e.g. quarterly, annual, TTM).""",
                expected_output="A clear list of these financial numbers with their time periods and sources."
            ),
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[0],
                description=f"""Analyze short-term trading opportunities for {self.company} based on technical analysis.

        {market_context}

        Provide a detailed short-term trading analysis covering:

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

        5. Short-term Opportunities:
           - Identified trading setups
           - Risk/reward scenarios
           - Entry/exit points
           - Stop-loss levels

        Format each section clearly and provide specific price levels where applicable.""",
                expected_output="""Provide a comprehensive short-term trading analysis with:
        1. Clear trend identification and direction
        2. Specific support and resistance levels
        3. Volume-based insights
        4. Concrete trading opportunities
        5. Risk management levels (entry, exit, stop-loss)
        6. Short-term price targets
        7. Confidence level in the analysis"""
            )
        ]



    def _create_calculation_task(self):
        """Create calculation tasks"""
        if not self.research_result:
            raise ValueError("Research result not available")

        return [
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[1],
                description=f"Calculate key accounting ratios for {self.company} with the data {self.research_result} (e.g., P/E ratio, Debt-to-Equity, and Return on Equity). Include Previously researched financial data in structured output",
                expected_output="""Provide calculations and interpretations for P/E, Debt-to-Equity, and ROE ratios in the format : "Formula: net_income / number_of_shares | Calculate: 1000000 / 500000" """
            ),
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[1],
                description="Structure the financial data into JSON as output. Only the names and values. Do not include interpretations",
                expected_output="""{"stock_data": {"Company Name": "Tesla", "P_E_Ratio": {"Value": 924.78},"Debt_to_Equity_Ratio": {"Value": 0.44}}}"""
            )
        ]

    def _create_risk_assessment_task(self):
        """Create risk assessment tasks"""
        if not self.research_result:
            raise ValueError("Research result not available")

        return [
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[2],
                description=f"Provide a comprehensive risk assessment for various investment choices for {self.company} "
                            f"related specifically to: {self.research_result} \n {self.calculation_result}",
                expected_output="A scale of the risk involved in decisions to buy, hold scaled to mild, moderate or severe risk."
            )
        ]

    def _create_blog_tasks(self):
        """Create blog tasks"""
        if not self.calculation_result:
            raise ValueError("Calculation result not available")

        return [
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[2],
                description=f"Based on previous analysis: {self.calculation_result} Make recommendation make a buy, sell, or hold recommendation.",
                expected_output="Provide a recommendation with supporting reasons: buy, sell, or hold."
            ),
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[3],
                description="Format the research, accounting data, and recommendation into a blog post.",
                expected_output="A well-formatted blog post combining research, financial ratios, and a final recommendation."
            )
        ]

    def _create_profit_loss_calculator_tasks(self):
        """Create profit/loss calculator tasks"""
        return [
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[1],
                description="""Calculate Profit/Loss analysis for the portfolio:
                1. Individual Trade P/L
                   - Entry price and exit price
                   - Position size
                   - Holding period
                   - Transaction costs

                2. Portfolio Level Analysis
                   - Total P/L
                   - Percentage returns
                   - Realized vs Unrealized gains
                   - Position weightings

                3. Performance Metrics
                   - ROI per trade
                   - Win/Loss ratio
                   - Average profit per trade
                   - Maximum drawdown

                Show all calculations using the Calculator tool with proper formula labeling.""",
                expected_output="""Provide analysis in format:
                {
                    "trade_analysis": {
                        "individual_trades": [
                            {
                                "trade_id": "id",
                                "entry": {"price": number, "date": "date"},
                                "exit": {"price": number, "date": "date"},
                                "position_size": number,
                                "costs": number,
                                "p_l": number,
                                "roi": number
                            }
                        ],
                        "summary": {
                            "total_trades": number,
                            "winning_trades": number,
                            "losing_trades": number,
                            "win_ratio": number
                        }
                    },
                    "portfolio_analysis": {
                        "total_pl": number,
                        "percentage_return": number,
                        "realized_gains": number,
                        "unrealized_gains": number,
                        "current_positions": [
                            {
                                "symbol": "ticker",
                                "weight": number,
                                "unrealized_pl": number
                            }
                        ]
                    },
                    "performance_metrics": {
                        "roi": number,
                        "average_profit": number,
                        "max_drawdown": number,
                        "sharpe_ratio": number
                    }
                }"""
            )
        ]

    def _create_tax_fee_calculator_tasks(self):
        """Create tax/fee calculator tasks"""
        return [
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[1],
                description="""Calculate tax and fee estimates for trades:
                1. Transaction Fees
                   - Broker commissions
                   - Exchange fees
                   - Spread costs
                   - Currency conversion fees (if applicable)

                2. Tax Calculations
                   - Short-term capital gains
                   - Long-term capital gains
                   - Wash sale adjustments
                   - Tax loss harvesting opportunities

                3. Cost Basis Tracking
                   - FIFO/LIFO calculations
                   - Adjusted cost basis
                   - Holding period tracking

                Use Calculator tool for all calculations and show your work.""",
                expected_output="""Provide analysis in format:
                {
                    "transaction_fees": {
                        "per_trade": [
                            {
                                "trade_id": "id",
                                "commission": number,
                                "exchange_fee": number,
                                "spread_cost": number,
                                "total_fees": number
                            }
                        ],
                        "total_fees": number
                    },
                    "tax_estimates": {
                        "short_term_gains": {
                            "total": number,
                            "tax_rate": number,
                            "estimated_tax": number
                        },
                        "long_term_gains": {
                            "total": number,
                            "tax_rate": number,
                            "estimated_tax": number
                        },
                        "wash_sales": [
                            {
                                "trade_id": "id",
                                "disallowed_loss": number,
                                "adjusted_basis": number
                            }
                        ],
                        "tax_loss_harvest": {
                            "opportunities": [
                                {
                                    "symbol": "ticker",
                                    "potential_harvest": number,
                                    "hold_until": "date"
                                }
                            ]
                        }
                    },
                    "cost_basis": {
                        "method": "FIFO/LIFO",
                        "positions": [
                            {
                                "symbol": "ticker",
                                "lots": [
                                    {
                                        "purchase_date": "date",
                                        "quantity": number,
                                        "original_basis": number,
                                        "adjusted_basis": number,
                                        "holding_period": "short/long"
                                    }
                                ]
                            }
                        ]
                    },
                    "summary": {
                        "total_fees_ytd": number,
                        "estimated_tax_liability": number,
                        "potential_tax_savings": number
                    }
                }"""
            ),
            self.ai_crew.create_task(
                agent=self.ai_crew.agents[1],
                description="""Review tax implications and optimize for:
                1. Tax Efficiency
                   - Identify tax-saving opportunities
                   - Suggest timing of trades
                   - Recommend tax-efficient strategies

                2. Fee Optimization
                   - Analyze fee impact on returns
                   - Suggest fee reduction strategies
                   - Compare broker/venue costs

                Provide actionable recommendations.""",
                expected_output="""Provide analysis in format:
                {
                    "tax_optimization": {
                        "immediate_actions": [
                            {
                                "action": "description",
                                "potential_saving": number,
                                "implementation": "steps"
                            }
                        ],
                        "long_term_strategy": [
                            {
                                "strategy": "description",
                                "expected_benefit": "description",
                                "timeline": "implementation_period"
                            }
                        ]
                    },
                    "fee_optimization": {
                        "recommendations": [
                            {
                                "area": "description",
                                "current_cost": number,
                                "potential_saving": number,
                                "action": "description"
                            }
                        ],
                        "broker_comparison": [
                            {
                                "broker": "name",
                                "fee_structure": "description",
                                "estimated_savings": number
                            }
                        ]
                    },
                    "priority_actions": [
                        {
                            "action": "description",
                            "impact": "high/medium/low",
                            "timeline": "immediate/short_term/long_term",
                            "estimated_benefit": number
                        }
                    ]
                }"""
            )
        ]

    def research_and_calculate(self, company_name=None):
        """Main method to run all analyses"""
        try:
            if not self.ai_crew:
                raise ValueError("AI Crew not initialized")

            if company_name:
                self.set_company(company_name)

            if not self.company:
                raise ValueError("Company name not set")

            # Initial company research
            research_tasks = self._create_research_task()
            self.research_result = str(self.ai_crew.kickoff(research_tasks))
            self.results['research'] = self.research_result

            # Calculate financial details
            calc_tasks = self._create_calculation_task()
            self.calculation_result = str(self.ai_crew.kickoff(calc_tasks))
            self.results['calculations'] = self.calculation_result

            # Risk assessment
            risk_tasks = self._create_risk_assessment_task()
            self.results['risk_assessment'] = str(self.ai_crew.kickoff(risk_tasks))

            # Blog creation
            blog_tasks = self._create_blog_tasks()
            self.results['blog'] = str(self.ai_crew.kickoff(blog_tasks))

            # Profit loss calculation
            profit_loss_tasks = self._create_profit_loss_calculator_tasks()
            self.results['profit_loss'] = str(self.ai_crew.kickoff(profit_loss_tasks))

            # Tax and fee calculation
            tax_fee_tasks = self._create_tax_fee_calculator_tasks()
            self.results['tax_fee'] = str(self.ai_crew.kickoff(tax_fee_tasks))

            self.print_results()
            return self.results

        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            return None

    def create_and_post_research_forecast(self, user_id: int) -> str:
        """
        Create and post a research-based forecast

        """
        try:
            if not self.company:
                raise ValueError("Company symbol not set")

            # Get technical data
            tech_data = self.backend_client.get_technical_analysis_data(self.company)
            if not tech_data:
                raise ValueError(f"Could not get technical data for {self.company}")

            # Execute research tasks
            research_tasks = self._create_research_task()
            analysis_result = self.ai_crew.kickoff(research_tasks)

            # Create forecast data
            forecast_data = ForecastParser.format_forecast(
                technical_data=tech_data,
                analysis_text=analysis_result,
                symbol=self.company
            )

            if forecast_data:
                # Post to backend
                result = self.backend_client.post_forecast(forecast_data, user_id)
                if result:
                    logger.info(f"Posted research forecast for {self.company} by user {user_id}")
                    return result.get('forecast_id')

            return None

        except Exception as e:
            logger.error(f"Error creating research forecast: {str(e)}")
            return None

    def print_results(self):
        """Print all results in formatted way"""
        try:
            for key, value in self.results.items():
                print("\n############")
                print(f"{key.replace('_', ' ').title()} results:")
                print(value)
        except Exception as e:
            print(f"Error printing results: {str(e)}")

    def get_result(self, result_type):
        """Get specific result by type"""
        return self.results.get(result_type)

    def get_all_results(self):
        """Get all results"""
        return self.results

    def clear_results(self):
        """Clear all stored results"""
        self.results = {}
        self.research_result = None
        self.calculation_result = None