from flask import Flask, jsonify, request
from task_manager import TaskManager
import logging
from typing import Optional, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
task_manager = TaskManager()


def initialize_task_manager():
    """Initialize and authenticate TaskManager"""
    success = task_manager.initialize_ai_crew(
        api_key=" ",
        # Placeholder models
        models_config={
            "Researcher": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"},
            "Accountant": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"},
            "Recommender": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"},
            "Blogger": {"model": "ollama/mistral:7b", "base_url": "http://localhost:11434"}
        }
    )

    if success:
        if task_manager.authenticate_backend("SuperAdmin", "password_123"):
            logger.info("TaskManager initialized and authenticated successfully")
            return True

    logger.error("Failed to initialize TaskManager")
    return False


def convert_metrics_to_dict(metrics) -> Dict:
    """Convert UsageMetrics to dictionary"""
    if hasattr(metrics, '__dict__'):
        return {
            k: v for k, v in metrics.__dict__.items()
            if not k.startswith('_')
        }
    return {}


@app.route('/ai/forecasts/<forecast_id>', methods=['GET'])
def get_forecast(forecast_id):
    """Endpoint to get forecast by ID"""
    try:
        symbol = request.args.get('symbol')
        if not symbol:
            return jsonify({"error": "Symbol parameter is required"}), 400

        logger.info(f"Received request for forecast ID: {forecast_id}, symbol: {symbol}")

        task_manager.set_company(symbol)
        research_tasks = task_manager._create_research_task()

        # Get the CrewOutput object and convert to string
        crew_output = task_manager.ai_crew.kickoff(research_tasks)
        forecast = str(crew_output)


        # Format response according to backend requirements
        response_data = {
            "id": int(forecast_id) if forecast_id.isdigit() else 1,  # Convert to int if possible
            "forecast": forecast,
            "user_id": 1  # Using default user_id for now
        }

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error processing forecast request: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "task_manager_initialized": bool(task_manager.ai_crew),
        "backend_authenticated": bool(task_manager.backend_client and
                                      task_manager.backend_client.token)
    })


if __name__ == '__main__':
    if initialize_task_manager():
        logger.info("Starting AI Module server on port 5000...")
        app.run(host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to initialize TaskManager. Server not started.")