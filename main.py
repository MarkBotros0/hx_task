from input_data.data import get_input_data
from helper_functions.generate_output_file import init_output_file
from helper_functions.json_file_handler import save_dataset
from algorithms.drones_hull import DronesHull
from algorithms.drones_tpl import DronesTPL
from algorithms.detachable_cameras import DetachableCameras
from algorithms.premium_summary import computeSummary, printSummary, apply_extensions


def perform_and_save_premium_calculations():
    """
    Perform all analysis tasks and save output to output dataset.
    """
    hull_analysis_results = DronesHull().performCalculations()
    save_dataset(hull_analysis_results)

    tpl_analysis_results = DronesTPL().performCalculations()
    save_dataset(tpl_analysis_results)

    detachable_cameras_analysis_results = DetachableCameras().performCalculations()
    save_dataset(detachable_cameras_analysis_results)


def generate_summaries():
    """
    Generate both net and gross summaries. Also, it prints a table of summary results.
    """
    print('\nPremium Summary before applying extensions')
    dataset_with_summary = computeSummary()
    save_dataset(dataset_with_summary)
    printSummary()

    print('Premium Summary after applying extensions')
    new_dataset = apply_extensions(2, 2)
    save_dataset(new_dataset)
    printSummary()


def main():
    """
    Perform the rating calculations replicating the logic of the program. 
    Also, it grenerates an output file that contains all the calculated model fields.

    Run the application using the command-line interface (CLI):
            python main.py
    Run the unit tests using the CLI:
            python -m unittest discover

    All calculations made are reflected on output/data.json
    """

    # Retrieve input data
    input_data = get_input_data()

    # Initialize an output file as a datasource that have input values only
    init_output_file(input_data)

    # Perform model analysis and update output dataset
    perform_and_save_premium_calculations()

    # Calculate and print summary results
    generate_summaries()


if __name__ == '__main__':
    main()
