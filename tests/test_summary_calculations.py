import unittest
from unittest.mock import patch
from algorithms.premium_summary import _get_gross_prem_drones_hull, _get_gross_prem_drones_tpl, _get_gross_prem_cameras_hull, _get_gross_prem_total
from algorithms.premium_summary import _get_net_prem_drones_hull, _get_net_prem_drones_tpl, _get_net_prem_cameras_hull, _get_net_prem_total


class TestPremiumSummaryCalculations(unittest.TestCase):

    def test_get_gross_prem_drones_hull(self):
        net_prem_drones_hull = 1000
        brokerage = 0.5
        result = _get_gross_prem_drones_hull(net_prem_drones_hull, brokerage)
        self.assertEqual(result, 2000)

    def test_get_gross_prem_drones_tpl(self):
        net_prem_drones_tpl = 2000
        brokerage = 0.5
        result = _get_gross_prem_drones_tpl(net_prem_drones_tpl, brokerage)
        self.assertEqual(result, 4000)

    def test_get_gross_prem_cameras_hull(self):
        net_prem_cameras_hull = 500
        brokerage = 0.15
        result = _get_gross_prem_cameras_hull(net_prem_cameras_hull, brokerage)
        self.assertEqual(result, 588.2352941176471)

    def test_get_gross_prem_total(self):
        gross_prem_drones_hull = 1111
        gross_prem_drones_tpl = 2500
        gross_prem_cameras_hull = 588
        result = _get_gross_prem_total(
            gross_prem_drones_hull, gross_prem_drones_tpl, gross_prem_cameras_hull)
        self.assertEqual(result, 4199)

    @patch('algorithms.premium_summary._get_net_prem_drones_hull')
    def test_get_net_prem_drones_hull(self, mock_get_net_prem_drones_hull):
        drones = [
            {"hull_premium": 500},
            {"hull_premium": 800},
            {"hull_premium": 1200}
        ]
        mock_get_net_prem_drones_hull.return_value = sum(
            [drone["hull_premium"] for drone in drones])
        result = _get_net_prem_drones_hull(drones)
        self.assertEqual(result, 2500)

    @patch('algorithms.premium_summary._get_net_prem_drones_tpl')
    def test_get_net_prem_drones_tpl(self, mock_get_net_prem_drones_tpl):
        drones = [
            {"tpl_layer_premium": 100},
            {"tpl_layer_premium": 150},
            {"tpl_layer_premium": 200}
        ]
        mock_get_net_prem_drones_tpl.return_value = sum(
            [drone["tpl_layer_premium"] for drone in drones])
        result = _get_net_prem_drones_tpl(drones)
        self.assertEqual(result, 450)

    @patch('algorithms.premium_summary._get_net_prem_cameras_hull')
    def test_get_net_prem_cameras_hull(self, mock_get_net_prem_cameras_hull):
        detachable_cameras = [
            {"hull_premium": 50},
            {"hull_premium": 75},
            {"hull_premium": 100}
        ]
        mock_get_net_prem_cameras_hull.return_value = sum(
            [camera["hull_premium"] for camera in detachable_cameras])
        result = _get_net_prem_cameras_hull(detachable_cameras)
        self.assertEqual(result, 225)

    @patch('algorithms.premium_summary._get_net_prem_drones_hull')
    @patch('algorithms.premium_summary._get_net_prem_drones_tpl')
    @patch('algorithms.premium_summary._get_net_prem_cameras_hull')
    def test_get_net_prem_total(self, mock_get_net_prem_cameras_hull, mock_get_net_prem_drones_tpl, mock_get_net_prem_drones_hull):
        mock_get_net_prem_drones_hull.return_value = 3000
        mock_get_net_prem_drones_tpl.return_value = 4000
        mock_get_net_prem_cameras_hull.return_value = 500

        result = _get_net_prem_total(3000, 4000, 500)
        self.assertEqual(result, 7500)


if __name__ == '__main__':
    unittest.main()
