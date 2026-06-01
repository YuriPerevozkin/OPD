from lab3 import lab3
import unittest


class TestApp(unittest.TestCase):
    def test_payment_1(self):
        payment = lab3.calculate_payment(1_000_000, 10.5 / 12 / 100, 15 * 12)
        self.assertEqual(payment, 11053.989236971684)

    def test_payment_2(self):
        payment = lab3.calculate_payment(2_000_000, 12 / 12 / 100, 20 * 12)
        self.assertEqual(payment, 22021.722671392195)

    def test_payment_3(self):
        payment = lab3.calculate_payment(1_500_000, 15 / 12 / 100, 15 * 12)
        self.assertEqual(payment, 20993.80678116861)

    def test_payment_zero(self):
        payment = lab3.calculate_payment(0, 0, 0)
        self.assertEqual(payment, 0.0)

    def test_payment_is_none(self):
        payment = lab3.calculate_payment(None, None, None)
        self.assertIsNone(payment)


if __name__ == "__main__":
    unittest.main()
