import unittest

from repair_shop import estimate_minutes, repair_total, service_label


class ShopTests(unittest.TestCase):
    def test_invoice_total(self):
        self.assertEqual(repair_total(1200, [200, 500]), 1900)
        self.assertEqual(repair_total(1200, []), 1200)

    def test_estimate(self):
        self.assertEqual(estimate_minutes(["flat", "inspection"]), 40)
        self.assertEqual(estimate_minutes([]), 0)

    def test_label(self):
        self.assertEqual(service_label("brake_adjustment"), "Brake Adjustment")


if __name__ == "__main__":
    unittest.main()
