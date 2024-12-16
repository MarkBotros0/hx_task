import unittest
from unittest.mock import patch
from algorithms.drones_hull import DronesHull


class TestDroneMethods(unittest.TestCase):
    """
    Unit tests for the DronesHull class methods to ensure correct hull rate calculations.
    """

    @patch('algorithms.drones_hull.get_parameters')
    def setUp(self, mock_get_parameters):
        """
        Sets up mock data and initializes the DronesHull instance for testing.
        """
        mock_get_parameters.return_value = {
            "gross_base_rate": {"hull": 0.08},
            "max_take_off_weight": {
                "0 - 5kg": 1,
                "5 - 10kg": 1.2,
                "10 - 20kg": 1.6,
                "> 20": 2.5
            }
        }
        self.drone_hull = DronesHull()

    def test_get_hull_base_rate(self):
        """
        Tests that the base rate for the hull is returned correctly based on the drone value.
        """
        result = self.drone_hull._get_hull_base_rate(0)
        self.assertEqual(result, '')

        result = self.drone_hull._get_hull_base_rate(1000)
        self.assertEqual(result, 0.08)

    def test_get_hull_weight_adjustment(self):
        """
        Tests that the weight adjustment for the hull is returned correctly based on the drone's weight class.
        """
        result = self.drone_hull._get_hull_weight_adjustment(0, 1)
        self.assertEqual(result, '')

        result = self.drone_hull._get_hull_weight_adjustment(1000, "10 - 20kg")
        self.assertEqual(result, 1.6)

    def test_get_hull_final_rate(self):
        """
        Tests that the final hull rate is calculated correctly based on drone value, weight adjustment, and base rate.
        """
        result = self.drone_hull._get_hull_final_rate(0, 100, 1.2)
        self.assertEqual(result, '')

        result = self.drone_hull._get_hull_final_rate(1000, 100, 1.2)
        self.assertEqual(result, 120)

    def test_get_hull_premium(self):
        """
        Tests that the hull premium is calculated correctly based on the final hull rate.
        """
        result = self.drone_hull._get_hull_premium(0, 120)
        self.assertEqual(result, '')

        result = self.drone_hull._get_hull_premium(1000, 120)
        self.assertEqual(result, 120000)


if __name__ == '__main__':
    unittest.main()
