from crewai_tools import BaseTool
import re
from typing import Union
import json


class CalculatorTool(BaseTool):
    name: str = "Calculator Tool"
    description: str = (
        "Performs mathematical calculations based on provided values. "
        "Input should be a JSON string containing variable names and their numerical values, "
        "followed by the operation to perform. "
        "Example: '{\"input_str\": \"{\\\"market_price\\\": 254.96, \\\"eps\\\": 2.78, \\\"operation\\\": \\\"market_price / eps\\\"}\"}'"
        "Example: '{\"input_str\": \"{\\\"market_price\\\": 254.96, \\\"eps\\\": 2.78, \\\"operation\\\": \\\"market_price / eps\\\"}\"}' "
    )

    def _run(self, input_str: str) -> Union[float, str]:
        try:
            # Parse the input JSON
            input_data = json.loads(input_str)

            # Extract the operation and variables
            operation = input_data.pop('operation', None)
            if not operation:
                return "Error: No operation specified"

            # Replace variable names with their values in the operation
            for var, value in input_data.items():
                operation = operation.replace(var, str(value))

            # Check if the operation contains only allowed characters
            if not re.match(r'^[\d\+\-\*/\(\)\.\s]+$', operation):
                raise ValueError("Invalid characters in the expression")

            # Evaluate the expression
            result = eval(operation)

            # Round the result to 4 decimal places if it's a float
            if isinstance(result, float):
                result = round(result, 4)

            return result
        except json.JSONDecodeError:
            return "Error: Invalid JSON input"
        except Exception as e:
            return f"Error: {str(e)}"

    def _arun(self, input_str: str) -> Union[float, str]:

        return self._run(input_str)