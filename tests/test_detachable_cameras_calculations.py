import unittest
from unittest.mock import patch
from algorithms.detachable_cameras import DetachableCameras


class TestDetachableCameras(unittest.TestCase):
    """
    Unit tests for the DetachableCameras class methods to ensure correct calculations for hull rates and premiums.
    """

    @patch('algorithms.detachable_cameras.load_dataset')
    @patch('algorithms.detachable_cameras.get_parameters')
    def setUp(self, mock_get_parameters, mock_load_dataset):
        """
        Sets up mock data and initializes the DetachableCameras instance for testing.
        """
        mock_get_parameters.return_value = {
            "gross_base_rate": {"hull": 1000},
            "max_take_off_weight": {10: 1.5, 20: 2.0}
        }

        mock_load_dataset.return_value = {
            "drones": [
                {"hull_final_rate": 150, "has_detachable_camera": True, "value": 1000},
                {"hull_final_rate": 200, "has_detachable_camera": True, "value": 1500},
                {"hull_final_rate": 120, "has_detachable_camera": False, "value": 500}
            ],
            "detachable_cameras": [
                {"value": 1000},
                {"value": 2000},
                {"value": 0}
            ]
        }

        self.detachable_cameras = DetachableCameras()

    def test_get_detachable_camera_hull_rate(self):
        """
        Tests that the hull rate for a detachable camera is calculated correctly based on the drone dataset.
        """
        result = self.detachable_cameras._get_detachable_camera_hull_rate(1000)
        self.assertEqual(result, 200)

        result = self.detachable_cameras._get_detachable_camera_hull_rate(0)
        self.assertEqual(result, '')

    def test_get_detachable_camera_hull_premium(self):
        """
        Tests that the hull premium for a detachable camera is calculated correctly based on its value and hull rate.
        """
        result = self.detachable_cameras._get_detachable_camera_hull_premium(
            1000, 200)
        self.assertEqual(result, 200000)

        result = self.detachable_cameras._get_detachable_camera_hull_premium(
            0, 200)
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
