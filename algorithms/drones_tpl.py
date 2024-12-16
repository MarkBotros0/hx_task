from helper_functions.riebesell_calculation import riebesell
from parameters.parameters import get_parameters
from helper_functions.json_file_handler import save_dataset, load_dataset


class DronesTPL():
    """
    This class is responsible for performing the third-party liability (TPL) analysis for drones in the dataset.
    """

    def __init__(self):
        """
        Initializes the TPLAnalysis class by loading the necessary parameters 
        and the dataset.
        """
        self.parameters = get_parameters()
        self.data = load_dataset()

    def _get_tpl_base_rate(self, drone_value):
        """
        Determines the TPL base rate for a drone based on its value. 
        """
        if drone_value == 0:
            return ''
        return self.parameters["gross_base_rate"]["liability"]

    def _get_tpl_base_layer_premium(self, drone_value, tpl_base_rate):
        """
        Determines the base layer premium for the TPL coverage of a drone.
        """
        if drone_value == 0:
            return ''
        return (drone_value*tpl_base_rate)

    def _get_tpl_ilf(self, drone_value, tpl_limit, tpl_excess):
        """
        Calculates the Individual Loss Factor (ILF) for the TPL coverage of a drone.
        """
        if drone_value == 0:
            return ''

        ilf_base_limit = self.parameters["ilf"]["base_limit"]
        ilf_z = self.parameters["ilf"]["z"]

        riebesell_1 = riebesell(
            ilf_base_limit, ilf_z, tpl_excess+tpl_limit)
        riebesell_2 = riebesell(
            ilf_base_limit, ilf_z, tpl_excess)

        return riebesell_1 - riebesell_2

    def _get_tpl_layer_premium(self, drone_value, tpl_base_layer_premium, tpl_ilf):
        """
        Calculates the TPL layer premium for a drone.
        """
        if drone_value == 0:
            return ''
        return tpl_ilf * tpl_base_layer_premium

    def performCalculations(self):
        """
        Performs the TPL analysis on all drones in the dataset and return the new dataset.
        """
        for drone in self.data["drones"]:
            tpl_base_rate = self._get_tpl_base_rate(drone["value"])
            tpl_base_layer_premium = self._get_tpl_base_layer_premium(
                drone["value"],
                tpl_base_rate)
            tpl_ilf = self._get_tpl_ilf(
                drone["value"],
                drone["tpl_limit"],
                drone["tpl_excess"])
            tpl_layer_premium = self._get_tpl_layer_premium(
                drone["value"],
                tpl_base_layer_premium,
                tpl_ilf)

            new_fields = {
                "tpl_base_rate": tpl_base_rate,
                "tpl_base_layer_premium": tpl_base_layer_premium,
                "tpl_ilf": tpl_ilf,
                "tpl_layer_premium": tpl_layer_premium
            }

            drone.update(new_fields)
        return self.data
