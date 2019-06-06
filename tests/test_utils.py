from pathlib import Path
import unittest

from vat_validator.utils import validate_vat


class ValidateVATTestCase(unittest.TestCase):
    def setUp(self):
        self.data_dir = Path(__file__).parent / "data"
        self.vat_examples = []
        for filename in self.data_dir.glob("**/*.txt"):
            country_code, is_valid = filename.stem.split("_")
            with filename.open() as vat_file:
                for vat in vat_file:
                    self.vat_examples.append(
                        (country_code, vat.strip(), is_valid == "VALID")
                    )

    def test_validate_vat_raises_value_error_with_invalid_country_code(self):
        self.assertRaises(ValueError, validate_vat, "ZZ", "")

    def test_validate_vat(self):
        for country_code, vat, is_valid in self.vat_examples:
            self.assertEqual(
                validate_vat(country_code, vat),
                is_valid,
                f"Test for VAT: ({country_code}, {vat}) failed",
            )


if __name__ == "__main__":
    unittest.main()
