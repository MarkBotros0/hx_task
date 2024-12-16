import unittest
from unittest.mock import patch
from algorithms.drones_tpl import DronesTPL


class TestDroneTPLCalculations(unittest.TestCase):
    """
    Unit tests for the DronesTPL class methods to ensure correct TPL rate calculations.
    """

    @patch('algorithms.drones_tpl.get_parameters')
    def setUp(self, mock_get_parameters):
        """
        Sets up mock data and initializes the DronesTPL instance for testing.
        """
        mock_get_parameters.return_value = {
            "gross_base_rate": {
                "liability": 0.02
            },
            "ilf": {
                "base_limit": 1000000,
                "z": 0.2
            },
        }
        self.drone = DronesTPL()

    def test_get_tpl_base_rate(self):
        """
        Tests that the base rate for TPL is returned correctly based on the drone value.
        """
        result = self.drone._get_tpl_base_rate(0)
        self.assertEqual(result, '')

        result = self.drone._get_tpl_base_rate(1000)
        self.assertEqual(result, 0.02)

    def test_get_tpl_base_layer_premium(self):
        """
        Tests that the base layer premium for TPL is calculated correctly based on the drone value.
        """
        result = self.drone._get_tpl_base_layer_premium(0, 200)
        self.assertEqual(result, '')

        result = self.drone._get_tpl_base_layer_premium(1000, 200)
        self.assertEqual(result, 200000)

    @patch('algorithms.drones_tpl.riebesell')
    def test_get_tpl_ilf(self, mock_riebesell):
        """
        Tests that the ILF is calculated correctly for valid drone values using the Riebesell function.
        """
        result = self.drone._get_tpl_ilf(0, 5000, 500)
        self.assertEqual(result, '')

        mock_riebesell.side_effect = [10, 8]
        result = self.drone._get_tpl_ilf(1000, 5000, 500)
        self.assertEqual(result, 2)

    def test_get_tpl_layer_premium(self):
        """
        Tests that the TPL layer premium is returned correctly for zero drone values.
        """
        result = self.drone._get_tpl_layer_premium(0, 200000, 2)
        self.assertEqual(result, '')

        result = self.drone._get_tpl_layer_premium(1000, 200000, 2)
        self.assertEqual(result, 400000)


if __name__ == '__main__':
    unittest.main()
