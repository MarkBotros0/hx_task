from parameters.parameters import get_parameters
from helper_functions.json_file_handler import save_dataset, load_dataset


class DronesHull():
    """
    This class is responsible for performing the hull-related analysis for the drones in the dataset.
    """

    def __init__(self):
        """
        Initializes the HullAnalysis class by loading the necessary parameters 
        and the dataset.
        """
        self.parameters = get_parameters()
        self.data = load_dataset()

    def _get_hull_base_rate(self, drone_value):
        """
        Determines the hull base rate for a drone based on its value. 
        """
        if drone_value == 0:
            return ''
        return self.parameters["gross_base_rate"]["hull"]

    def _get_hull_weight_adjustment(self, drone_value, drone_weight):
        """
        Determines the hull weight adjustment for a drone based on its weight. 
        """
        if drone_value == 0:
            return ''
        return self.parameters["max_take_off_weight"][drone_weight]

    def _get_hull_final_rate(self, drone_value, hull_base_rate, hull_weight_adjustment):
        """
        Calculates the final hull rate for a drone.
        """
        if drone_value == 0:
            return ''
        return hull_base_rate*hull_weight_adjustment

    def _get_hull_premium(self, drone_value, hull_final_rate):
        """
        Calculates the hull premium for a drone.
        """
        if drone_value == 0:
            return ''
        return drone_value*hull_final_rate

    def performCalculations(self):
        """
        Performs the hull analysis on all drones in the dataset and return the new dataset.
        """
        for drone in self.data["drones"]:

            hull_base_rate = self._get_hull_base_rate(drone.get("value"))

            hull_weight_adjustment = self._get_hull_weight_adjustment(
                drone["value"],
                drone["weight"])

            hull_final_rate = self._get_hull_final_rate(
                drone["value"],
                hull_base_rate,
                hull_weight_adjustment)

            hull_premium = self._get_hull_premium(
                drone["value"],
                hull_final_rate)

            new_fields = {
                "hull_base_rate": hull_base_rate,
                "hull_weight_adjustment": hull_weight_adjustment,
                "hull_final_rate": hull_final_rate,
                "hull_premium": hull_premium
            }

            drone.update(new_fields)
        return self.data
