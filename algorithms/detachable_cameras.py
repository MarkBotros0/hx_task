from parameters.parameters import get_parameters
from helper_functions.json_file_handler import load_dataset


class DetachableCameras():
    """
    This class is responsible for analyzing the detachable cameras within the dataset.
    """

    def __init__(self):
        """
        Initializes the DetachableCamerasAnalysis class by loading the necessary parameters 
        and the dataset.
        """
        self.parameters = get_parameters()
        self.data = load_dataset()

    def _get_detachable_camera_hull_rate(self, detachable_camera_value):
        """
        Determines the hull rate for a detachable camera based on the value of the camera 
        and the drones in the dataset.
        """
        if detachable_camera_value == 0:
            return ''

        drones = self.data["drones"]
        max_final_rate = max(
            [drone["hull_final_rate"] for drone in drones
             if drone["has_detachable_camera"] == True and drone["value"] > 0]
        )

        return max_final_rate

    def _get_detachable_camera_hull_premium(self, detachable_camera_value, detachable_camera_hull_rate):
        """
        Calculates the hull premium for a detachable camera based on its value and the determined 
        hull rate. 
        """
        if detachable_camera_value == 0:
            return ''
        return detachable_camera_value*detachable_camera_hull_rate

    def performCalculations(self):
        """
        Performs the analysis on all detachable cameras in the dataset and return the new dataset.
        """
        for camera in self.data["detachable_cameras"]:
            hull_rate = self._get_detachable_camera_hull_rate(camera["value"])
            hull_premium = self._get_detachable_camera_hull_premium(
                camera["value"], hull_rate)

            new_fields = {
                "hull_rate": hull_rate,
                "hull_premium": hull_premium
            }

            camera.update(new_fields)
        return self.data
