import json
import os
from constants.constants import OUTPUT_PATH

output_path = OUTPUT_PATH

def load_dataset():
    with open(output_path, 'r') as file:
        data = json.load(file)  
    return data

def save_dataset(data):
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
                   
def clear_output_data():
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        file.write('{}')