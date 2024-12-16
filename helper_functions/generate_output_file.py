import json
from helper_functions.json_file_handler import clear_output_data
from constants.constants import OUTPUT_PATH

output_path = OUTPUT_PATH


def init_output_file(input_data):
    """
    Filter the input data to include input specific fields and then copy the filtered data to a new JSON file.
    Path of output file by default: 'output/data.json', it can be changed from constants/constants.py.
    """
    clear_output_data()

    fields = ["insured",
              "underwriter",
              "broker",
              "brokerage",
              "max_drones_in_air"]

    filtered_data = {key: input_data[key]
                     for key in fields if key in input_data}

    filtered_data["drones"] = [
        {key: drone[key] for key in [
            "serial_number",
            "value",
            "weight",
            "has_detachable_camera",
            "tpl_limit",
            "tpl_excess"]}
        for drone in input_data["drones"]
    ]

    filtered_data["detachable_cameras"] = [
        {key: camera[key] for key in ["serial_number", "value"]}
        for camera in input_data["detachable_cameras"]
    ]

    with open(output_path, 'w') as f:
        json.dump(filtered_data, f, indent=4)
