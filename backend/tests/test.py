from ..scrapers.autoscout import convert_to_year
import unittest

class YearConversionTests(unittest.TestCase):

    def test_invalid_year(self):
        self.assertEqual(convert_to_year("invalid"), 2010, "Should be 2010")

    def test_new(self):
        self.assertEqual(convert_to_year("new"), 2023, "Should be 2023")

    def test_valid_year(self):
        self.assertEqual(convert_to_year("01-2010"), 2010, "Should be 2010")

    def test_valid_year2(self):
        self.assertEqual(convert_to_year("05-2010"), 2010, "Should be 2010")

    def test_valid_year3(self):
        self.assertEqual(convert_to_year("05/2010"), 2010, "Should be 2010")

if __name__ == '__main__':
    unittest.main()