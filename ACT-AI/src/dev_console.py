from task_manager import TaskManager
import sys
import time

"""Temporary development console to test functionality prior to API integration"""
class DevConsole:
    def __init__(self):
        self.task_manager = TaskManager()
        self.default_models_config = {
            "Researcher": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"},
            "Accountant": {"model": "gpt-4o-mini", "base_url": "https://api.openai.com/v1"},
            "Recommender": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"},
            "Blogger": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"}
        }

    def configure_ai_crew(self):
        """Configure AI Crew settings"""
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
        else:
            print("Failed to initialize AI Crew. Please check your configuration.")

    def check_requirements(self, initial_check=True):
        """Check if all required variables are set"""
        vars = self.task_manager.get_required_variables(initial_check)
        missing = [k for k, v in vars.items() if not v]

        if missing:
            print("\nMissing required variables:")
            for var in missing:
                print(f"- {var}")
            return False
        return True

    def run_comprehensive_analysis(self):
        """Run comprehensive analysis"""
        if not self.check_requirements(initial_check=True):
            print("\nAI Crew not configured. Configuring now...")
            self.configure_ai_crew()

        stock_symbol = input("\nEnter stock symbol (e.g., TSLA): ").strip().upper()
        self.task_manager.set_company(stock_symbol)

        if self.check_requirements(initial_check=True):
            print(f"\nRunning comprehensive analysis for {stock_symbol}...")
            results = self.task_manager.research_and_calculate()
            return results
        else:
            print("\nCannot proceed - missing required variables")
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

    def run_specific_task(self):
        """Run a specific task type"""
        if not self.check_requirements(initial_check=True):
            print("\nAI Crew not configured. Configuring now...")
            self.configure_ai_crew()

        print("\nAvailable tasks:")
        tasks = {
            1: ("Research", True),  # (task_name, needs_only_initial_check)
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
        print("6. Exit")
        return input("\nSelect an option (1-6): ").strip()

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
                print("\nExiting console... ")
                sys.exit(0)
            else:
                print("\nInvalid option. Please try again.")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    console = DevConsole()
    console.run()