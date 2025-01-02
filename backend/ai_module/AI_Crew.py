import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from calculator_tool import CalculatorTool
from chatbot_tools import StockDataTool
from market_data import MarketData



class AI_Crew:



    def __init__(self):
        """
        Initialize the AI_Crew with an API key and a model configuration.
        models_config: A dictionary specifying which model each agent will use.
        Example: {
            "Researcher": {"model": "gpt-4", "base_url": "https://api.openai.com/v1"},
            "Accountant": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"},
            "Recommender": {"model": "gpt-3.5-turbo", "base_url": "https://api.openai.com/v1"},
            "Blogger": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11734"}
            "Chatbot": {"model": "gemini/gemini-1.5-flash", "base_url": " "}
        }
        """
        # Get the current file's directory
        current_dir = Path(__file__).resolve().parent
        # Get the parent directory
        parent_dir = current_dir.parent
        # Construct path to .env file
        env_path = parent_dir / '.env'

        # Load environment variables from .env file
        load_dotenv(dotenv_path=env_path)

        # Get API keys from environment variables
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")


        os.environ['GROQ_API_KEY'] = " "
        self.market_data = MarketData()
        self.models_config = {
            "Researcher": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
            "Accountant": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
            "Recommender": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
            "Blogger": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
            "Chatbot": {"model": "gemini/gemini-1.5-flash", "base_url": " "}
        }

        self.agents = self._create_agents()


    def _create_agents(self):
        """
        Create the 4 specific agents: Researcher, Accountant, Recommender, and Blogger.
        Each agent will use the model and base_url defined in the models_config dictionary.
        """
        # Initialize the agents with roles, goals, and backstories using their respective models.

        researcher = Agent(
            role="Researcher",
            goal="Research a particular stock and provide insightful information.",

            backstory="You are meticulous and dive deep into the stock market to gather detailed information.",
            llm=self._get_llm("Researcher")
        )

        accountant = Agent(
            role="Accountant",
            goal="Calculate financial ratios using the Calculator tool with proper formula format",
            tools=[CalculatorTool()],
            backstory="""You are a financial analyst who calculates ratios using the Calculator tool.
              Always use the exact format:
              'Formula: [ratio_name] | Calculate: [numbers]'
              If data is not available, input 'None' for the calculation.""",
            llm=self._get_llm("Accountant")
        )

        recommender = Agent(
            role="Recommender",
            goal="Analyze financial data and provide buy, sell, or hold recommendations.",
            backstory="You enjoy making tough decisions and providing clear investment advice.",
            llm=self._get_llm("Recommender")
        )

        blogger = Agent(
            role="Blogger",
            goal="Format the research, calculations, and recommendations into a polished and readable blog post.",
            backstory="You have a knack for turning complex data into engaging, readable content.",
            llm=self._get_llm("Blogger")
        )
        chatbot = Agent(
            role="Chatbot",
            tools=[StockDataTool(self.market_data)],
            goal="Engage in natural conversation about stock market data and provide informed responses",
            backstory="""You are a friendly and knowledgeable AI assistant specializing in stock market 
                   conversations. You can explain complex financial concepts in simple terms and provide context 
                   for market data. You maintain context throughout conversations and can reference previous 
                   analyses when relevant.""",
            llm=self._get_llm("Chatbot")
        )

        return [researcher, accountant, recommender, blogger, chatbot]



    def _get_llm(self, agent_name):
        """
        Return the LLM (model) for a specific agent based on the models_config.
        """
        model_info = self.models_config.get(agent_name)
        if model_info:
            return LLM(
            model=model_info["model"],

            )
        else:
            raise ValueError(f"Model configuration for {agent_name} not provided.")

    def create_task(self, agent, description, expected_output):
        """
        Create a task for a specific agent.
        agent: The agent responsible for the task.
        description: A description of what the task should achieve.
        expected_output: What the task should return.
        """
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    def kickoff(self, tasks, verbose=True):
        """
        Execute the tasks with the pre-defined agents.
        tasks: A list of Task objects that agents need to complete.
        verbose: Whether to print detailed output of the process.
        """
        # Create the crew with the current agents and tasks
        crew = Crew(
            agents=self.agents,
            tasks=tasks,
            verbose=verbose
        )

        # Run the tasks and return the result
        result = crew.kickoff()
        return result