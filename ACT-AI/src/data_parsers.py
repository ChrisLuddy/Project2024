import json

"""
Functions for data parsing in standard formats.
Can be integrated to class methods after API methodology is established.
"""





def string_list_to_list(input_str: str) -> list:
    """
    Convert a string formatted as a list into a Python list.
    """
    try:
        # Remove brackets and split by comma
        cleaned = input_str.strip('[]').strip()

        # If empty string after cleaning, return empty list
        if not cleaned:
            return []

        # Split by comma and strip whitespace/quotes from each item
        items = [item.strip().strip("'\"") for item in cleaned.split(',')]

        # Try to convert numbers to float/int where possible
        converted_items = []
        for item in items:
            try:
                # Try integer first
                if '.' not in item:
                    converted_items.append(int(item))
                else:
                    # Try float if decimal point exists
                    converted_items.append(float(item))
            except ValueError:
                # Keep as string if not a number
                converted_items.append(item)

        return converted_items

    except Exception as e:
        print(f"Error converting string to list: {str(e)}")
        return []


def json_to_dict(json_data):
    """
    Convert JSON data to Python dictionary.

    Args:
        json_data: Can be either a JSON string or a file path to a JSON file

    Returns:
        dict: Converted Python dictionary
    """


    try:
        # First try treating input as a JSON string
        return json.loads(json_data)
    except json.JSONDecodeError:
        try:
            # If that fails, try treating it as a file path
            with open(json_data, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find JSON file: {json_data}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Invalid JSON format in: {json_data}")


def dict_to_json(python_dict, file_path=None, pretty=True):
    """
    Convert Python dictionary to JSON.

    Args:
        python_dict (dict): Python dictionary to convert
        file_path (str, optional): If provided, saves JSON to this file
        pretty (bool): If True, formats JSON with nice indentation

    Returns:
        str: JSON string
    """
    import json

    if not isinstance(python_dict, dict):
        raise TypeError("Input must be a dictionary")

    try:
        # Convert to JSON string with optional pretty printing
        if pretty:
            json_string = json.dumps(python_dict, indent=4, sort_keys=True)
        else:
            json_string = json.dumps(python_dict)

        # If file path is provided, save to file
        if file_path:
            with open(file_path, 'w') as file:
                file.write(json_string)

        return json_string

    except Exception as e:
        raise Exception(f"Error converting dictionary to JSON: {str(e)}")


