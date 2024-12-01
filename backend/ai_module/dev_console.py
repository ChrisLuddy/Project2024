from task_manager import TaskManager
import sys
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DevConsole:
    def __init__(self):
        self.task_manager = TaskManager()
        self.default_models_config = {
            "Researcher": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
            "Accountant": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
            "Recommender": {"model": "gemini/gemini-1.5-flash", "base_url": " "},
            "Blogger": {"model": "gemini/gemini-1.5-flash", "base_url": " "}
        }
        self.backend_authenticated = False

    def configure_ai_crew(self):
        """Configure AI Crew settings and backend authentication"""
        print("\n=== AI Crew Configuration ===")
        use_default = input("Use default configuration? (y/n): ").lower() == 'y'

        if use_default:
            api_key = input("Enter API key (press Enter for default): ").strip() or None
            success = self.task_manager.initialize_ai_crew(api_key, self.default_models_config)
        else:
            api_key = input("Enter API key: ").strip()

            models_config = {}
            for role in ["Researcher", "Accountant", "Recommender", "Blogger"]:
                print(f"\nConfiguration for {role}:")
                model = input(f"Enter model for {role}: ")
                base_url = input(f"Enter base URL for {role}: ")
                models_config[role] = {"model": model, "base_url": base_url}

            success = self.task_manager.initialize_ai_crew(api_key, models_config)

        if success:
            print("AI Crew configuration complete!")

            self.authenticate_backend()
        else:
            print("Failed to initialize AI Crew. Please check your configuration.")

    def authenticate_backend(self):
        """Authenticate with the backend API"""
        print("\n=== Backend Authentication ===")
        username = input("Enter backend username (default: SuperAdmin): ").strip() or "SuperAdmin"
        password = input("Enter backend password (default: password_123): ").strip() or "password_123"

        if self.task_manager.backend_client:
            if self.task_manager.backend_client.authenticate(username, password):
                print("Successfully authenticated with backend!")
                self.backend_authenticated = True
            else:
                print("Failed to authenticate with backend. Some functionality may be limited.")
                self.backend_authenticated = False
        else:
            print("Backend client not initialized. Please configure AI Crew first.")

    def check_requirements(self, initial_check=True):
        """Check if all required variables and authentication are set"""
        vars = self.task_manager.get_required_variables(initial_check)
        missing = [k for k, v in vars.items() if not v]

        if not self.backend_authenticated:
            missing.append('backend_authentication')

        if missing:
            print("\nMissing required variables:")
            for var in missing:
                print(f"- {var}")
            return False
        return True

    def run_comprehensive_analysis(self):
        """Run comprehensive analysis"""
        if not self.check_requirements(initial_check=True):
            print("\nMissing requirements. Configuring now...")
            self.configure_ai_crew()

            if not self.backend_authenticated:
                self.authenticate_backend()

        stock_symbol = input("\nEnter stock symbol (e.g., TSLA): ").strip().upper()
        self.task_manager.set_company(stock_symbol)

        if self.check_requirements(initial_check=True):
            print(f"\nRunning comprehensive analysis for {stock_symbol}...")
            results = self.task_manager.research_and_calculate()
            return results
        else:
            print("\nCannot proceed - missing required variables or authentication")
            return None

    def view_specific_results(self):
        """View specific results from the analysis"""
        if not self.task_manager.get_all_results():
            print("\nNo analysis results available. Run an analysis first.")
            return

        print("\nAvailable result types:")
        results = self.task_manager.get_all_results()
        for i, key in enumerate(results.keys(), 1):
            print(f"{i}. {key.replace('_', ' ').title()}")

        choice = input("\nEnter number to view (or 'all' for all results): ").strip()

        if choice.lower() == 'all':
            self.task_manager.print_results()
        else:
            try:
                idx = int(choice) - 1
                key = list(results.keys())[idx]
                print(f"\n{key.replace('_', ' ').title()} results:")
                print(results[key])
            except (ValueError, IndexError):
                print("Invalid choice")

    def post_research_forecast(self):
        """Create and post a research forecast to backend"""
        if not self.check_requirements(initial_check=True):
            print("\nMissing requirements. Configuring now...")
            self.configure_ai_crew()

            if not self.backend_authenticated:
                self.authenticate_backend()

        stock_symbol = input("\nEnter stock symbol (e.g., TSLA): ").strip().upper()
        user_id = input("\nEnter user ID (press Enter for default 1): ").strip()
        user_id = int(user_id) if user_id else 1

        self.task_manager.set_company(stock_symbol)

        if self.check_requirements(initial_check=True):
            print(f"\nCreating research forecast for {stock_symbol} (User ID: {user_id})...")
            forecast_id = self.task_manager.create_and_post_research_forecast(user_id=user_id)

            if forecast_id:
                print(f"\nSuccessfully posted forecast with ID: {forecast_id}")
                print(f"Forecast created by User ID: {user_id}")
            else:
                print("\nFailed to create and post forecast")
        else:
            print("\nCannot proceed - missing required variables or authentication")

    def run_specific_task(self):
        """Run a specific task type"""
        if not self.check_requirements(initial_check=True):
            print("\nAI Crew not configured. Configuring now...")
            self.configure_ai_crew()

        print("\nAvailable tasks:")
        tasks = {
            1: ("Research", True),
            2: ("Calculations", False),
            3: ("Risk Assessment", False),
            4: ("Blog Creation", False),
            5: ("Profit/Loss Analysis", True),
            6: ("Tax/Fee Analysis", True)
        }

        for num, (task, _) in tasks.items():
            print(f"{num}. {task}")

        choice = input("\nSelect task number: ").strip()

        try:
            choice = int(choice)
            if not self.task_manager.company:
                stock_symbol = input("\nEnter stock symbol (e.g., TSLA): ").strip().upper()
                self.task_manager.set_company(stock_symbol)

            # Check requirements based on task type
            initial_check = tasks.get(choice, (None, True))[1]
            if not self.check_requirements(initial_check):
                print("\nMissing required variables for this task")
                return

            if choice == 1:
                tasks = self.task_manager._create_research_task()
            elif choice == 2:
                tasks = self.task_manager._create_calculation_task()
            elif choice == 3:
                tasks = self.task_manager._create_risk_assessment_task()
            elif choice == 4:
                tasks = self.task_manager._create_blog_tasks()
            elif choice == 5:
                tasks = self.task_manager._create_profit_loss_calculator_tasks()
            elif choice == 6:
                tasks = self.task_manager._create_tax_fee_calculator_tasks()

            result = self.task_manager.ai_crew.kickoff(tasks)
            print("\nTask Result:")
            print(result)

        except Exception as e:
            print(f"\nError running task: {str(e)}")

    def display_menu(self):
        """Display the main menu options"""
        print("\n=== AI Financial Assistant Development Console ===")
        print("1. Configure AI Crew")
        print("2. Run Comprehensive Analysis")
        print("3. Run Specific Task")
        print("4. View Analysis Results")
        print("5. Check Configuration Status")
        print("6. Re-authenticate Backend")
        print("7. Post Research Forecast")
        print("8. Exit")
        return input("\nSelect an option (1-8): ").strip()

    def run(self):
        """Main console loop"""
        print("Welcome to the AI Financial Assistant Development Console")

        while True:
            choice = self.display_menu()

            if choice == '1':
                self.configure_ai_crew()
            elif choice == '2':
                self.run_comprehensive_analysis()
            elif choice == '3':
                self.run_specific_task()
            elif choice == '4':
                self.view_specific_results()
            elif choice == '5':
                self.check_requirements()
            elif choice == '6':
                self.authenticate_backend()
            elif choice == '7':
                self.post_research_forecast()
            elif choice == '8':
                print("\nExiting console... ")
                sys.exit(0)
            else:
                print("\nInvalid option. Please try again.")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    console = DevConsole()
    console.run()