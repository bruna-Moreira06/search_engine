
import json
import os
import time
from datetime import datetime

from django.conf import settings


def embeddings(text):
    """
    Function to encode sentences and obtain their embeddings.

    Args:
        text (str): The input text to be encoded.

    Returns:
        numpy.ndarray: The embeddings of the input text.
    """
    start_time = time.time()  # Start the timer
    # Encode sentences to get their embeddings
    embedding = settings.MODEL.encode(text)

    end_time = time.time()
    execution_time = end_time - start_time
    save_execution_time('embeddings', execution_time)

    return embedding


def save_execution_time(function_name, execution_time):
    """
    Function to save the execution time of a function in a JSON file.

    Args:
        function_name (str): The name of the function.
        execution_time (float): The execution time of the function.
    """
    # Path to the folder where JSON files are stored
    json_folder = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '../', 'benchmarks')

    # Check if the folder exists, otherwise create it
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    # Full path to the JSON file of the function
    file_path = os.path.join(json_folder, f"{function_name}.json")

    data = []
    if os.path.exists(file_path):
        # Load existing data from the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

    # Add the new data
    timestamp = time.strftime('%Y%m%d%H%M%S')
    new_data = {
        'timestamp': timestamp,
        'execution_time': execution_time
    }
    data.append(new_data)

    # Save the updated data to the JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f)


def date_converter(date_string):
    # Convertir la date en objet datetime
    date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

    return date_obj.year, date_obj.month, date_obj.day
