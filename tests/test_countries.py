from pathlib import Path
import unittest

from vat_validator.countries import validate_vat_at
from vat_validator.countries import validate_vat_be, validate_vat_bg
from vat_validator.countries import validate_vat_pl, validate_vat_pt


class CountriesTestCase(unittest.TestCase):
    def setUp(self):
        self.data_dir = Path(__file__).parent / "data"
        self.vat_codes = {}

        for filename in self.data_dir.glob("**/*.txt"):
            country, is_valid = filename.stem.split("_")
            with filename.open() as vat_file:
                self.vat_codes[country] = [
                    (vat.strip(), is_valid == "VALID") for vat in vat_file
                ]

    def test_validate_vat_at(self):
        for vat, is_valid in self.vat_codes["AT"]:
            self.assertEqual(validate_vat_at(vat), is_valid, vat)

    def test_validate_vat_be(self):
        for vat, is_valid in self.vat_codes["BE"]:
            self.assertEqual(validate_vat_be(vat), is_valid, vat)

    def test_validate_vat_bg(self):
        for vat, is_valid in self.vat_codes["BG"]:
            self.assertEqual(validate_vat_bg(vat), is_valid, vat)

    def test_validate_vat_pl(self):
        for vat, is_valid in self.vat_codes["PL"]:
            self.assertEqual(validate_vat_pl(vat), is_valid, vat)

    def test_validate_vat_pt(self):
        for vat, is_valid in self.vat_codes["PT"]:
            self.assertEqual(validate_vat_pt(vat), is_valid, vat)


if __name__ == "__main__":
    unittest.main()
