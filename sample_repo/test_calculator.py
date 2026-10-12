import unittest
from calculator import safe_double

class CalculatorTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(safe_double(0), 0)
    def test_positive(self):
        self.assertEqual(safe_double(4), 8)
