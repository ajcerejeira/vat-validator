import unittest

from vat_validator.vies import check_vat


class VIESTestCase(unittest.TestCase):
    def test_check_vat_raises_value_error_with_invalid_country_code(self):
        self.assertRaises(ValueError, check_vat, "ZZ", "12345678")

    def test_check_vat_raises_value_error_with_empty_vat(self):
        self.assertRaises(ValueError, check_vat, "PT", "")
