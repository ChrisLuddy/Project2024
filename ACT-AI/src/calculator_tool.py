from crewai_tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = """
    Calculator that accepts both a labeled formula and its numerical calculation.

    Format your input as:
    "Formula: [labeled_expression] | Calculate: [numerical_expression]"

    Examples:
    "Formula: net_income / number_of_shares | Calculate: 1000000 / 500000"
    "Formula: revenue * profit_margin | Calculate: 5000000 * 0.15"
    "Formula: (total_assets - total_liabilities) / equity | Calculate: (1000000 - 400000) / 600000"

    The tool will use only the numerical expression after 'Calculate:' but keep the labeled formula for reference.
    Do not include characters or currency signs after 'Calculate':.
    Include only one Formula per input.
    """

    def _run(self, input_str: str):
        try:
            # Split the input into formula and calculation parts
            if '|' not in input_str:
                return "Error: Please provide both formula and calculation separated by |"

            formula_part, calc_part = input_str.split('|')

            # Extract the numerical calculation
            if 'Calculate:' not in calc_part:
                return "Error: Missing 'Calculate:' in the numerical part"

            calculation = calc_part.split('Calculate:')[1].strip()

            # Validate and perform the calculation
            if not all(c in '0123456789+-*/(). ' for c in calculation):
                return "Error: Calculation can only contain numbers and operators (+, -, *, /, (), .)"

            result = eval(calculation)
            labeled_result = f"Result for {formula_part.strip()}: {round(float(result), 4)}"
            return labeled_result

        except Exception as e:
            return f"Error: Invalid expression - {str(e)}"

    async def _arun(self, input_str: str):
        return self._run(input_str)
