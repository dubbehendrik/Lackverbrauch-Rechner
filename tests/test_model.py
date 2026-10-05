from copy import deepcopy
import unittest
from model import DEFAULTS, METHODS, PLANS, calculate


class MaterialBalanceTests(unittest.TestCase):
    def params(self, **updates):
        return {**deepcopy(DEFAULTS), **updates}

    def test_independent_reference(self):
        # 1 m² * 50 µm -> 0.00005 m³ * 1500 kg/m³ -> 0.075 kg dry.
        r = calculate(self.params(plan=PLANS[1], rate=120.0, shifts=1, net_hours=8.0,
                                 weeks=40.0, days=5))
        self.assertAlmostEqual(r['mass_piece'], 0.25)
        self.assertAlmostEqual(r['litres_piece'], 0.2)
        self.assertAlmostEqual(r['litres_h'], 24)
        self.assertAlmostEqual(r['area_min'], 2)
        year = r['periods'][-1]
        self.assertEqual(year['Stückzahl (rechnerisch)'], 192000)
        self.assertAlmostEqual(year['Lackverbrauch [L]'], 38400)
        self.assertAlmostEqual(year['Lackverlust [L]'], 19200)
        self.assertAlmostEqual(year['Verlustkosten [€]'], 288000)

    def test_pause_changes_spray_flow_not_piece_consumption(self):
        r = calculate(self.params(takt=7/6, pause=10.0))
        no_pause = calculate(self.params(takt=7/6, pause=0.0))
        self.assertAlmostEqual(r['spray'], 1)
        self.assertAlmostEqual(r['spray_litres_min'], 0.2)
        self.assertAlmostEqual(r['litres_min'], 0.2 / (7/6))
        self.assertEqual(r['litres_piece'], no_pause['litres_piece'])
        self.assertEqual(r['periods'], no_pause['periods'])
        self.assertEqual(r['periods'][0]['Vollständige Stücke'], 720)

    def test_three_routes_agree_with_consistent_density(self):
        p = self.params(epsilon=54.5, phi=39.5, rho_lk=1.15)
        estimated = calculate({**p, 'method': METHODS[1]})
        direct = calculate({**p, 'method': METHODS[2]})
        known = calculate({**p, 'rho_fk': estimated['rho_fk']})
        self.assertAlmostEqual(estimated['rho_fk'], 1586.7088607594937)
        for r in (direct, known):
            self.assertAlmostEqual(r['mass_piece'], estimated['mass_piece'])
            self.assertAlmostEqual(r['litres_piece'], estimated['litres_piece'])

    def test_target_inversion_and_month(self):
        p = self.params(plan=PLANS[2], target=100000, period='Jahr')
        r = calculate(p)
        self.assertEqual(r['periods'][-1]['Stückzahl (rechnerisch)'], 100000)
        self.assertAlmostEqual(r['periods'][2]['Lackverbrauch [L]'] * 12,
                               r['periods'][-1]['Lackverbrauch [L]'])
        forward = calculate({**p, 'plan': PLANS[1], 'rate': r['rate']})
        self.assertAlmostEqual(forward['periods'][-1]['Stückzahl (rechnerisch)'], 100000)

    def test_efficiency_and_zero_cost(self):
        low = calculate(self.params(mng=50.0))
        high = calculate(self.params(mng=100.0, price=0.0))
        self.assertAlmostEqual(low['litres_piece'], 2 * high['litres_piece'])
        self.assertEqual(high['loss_piece'], 0)
        self.assertEqual(high['periods'][-1]['Verlustkosten [€]'], 0)

    def test_invalid_inputs(self):
        for updates in [dict(mng=0), dict(epsilon=101), dict(area=float('nan')),
                        dict(pause=70, takt=1), dict(net_hours=9, shift_hours=8),
                        dict(shifts=3, shift_hours=9), dict(days=8), dict(weeks=53),
                        dict(plan=PLANS[2], target=100000000, pause=10), dict(price=-1)]:
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                calculate(self.params(**updates))


if __name__ == '__main__':
    unittest.main()
