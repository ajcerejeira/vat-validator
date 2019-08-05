import unittest

from vat_validator.validators import vat_is_valid_pt


class ValidatorsTestCase(unittest.TestCase):
    def setUp(self):
        self.vat_pt_valid = [
            "PT100000010",
            "PT100000029",
            "PT100000037",
            "PT100000193",
            "PT100000053",
            "PT100000061",
            "PT100000070",
            "PT100000096",
            "PT100000100",
            "PT100000118",
            "PT100000134",
            "PT100000142",
            "PT100000150",
            "PT100000177",
            "PT100000185",
            "PT100000193",
            "PT501413197",
            "PT501519246",
            "PT501570691",
            "PT502011378",
            "PT502757191",
            "PT502790610",
            "PT503079502",
            "PT503362999",
            "PT503731552",
            "PT503701378",
            "PT503729108",
            "PT504030108",
            "PT504141066",
            "PT504178873",
            "PT504194739",
            "PT505289385",
            "PT505448173",
            "PT505856468",
            "PT506429210",
            "PT506774287",
            "PT507132831",
            "PT507400011",
            "PT507599470",
            "PT507852605",
            "PT508219612",
            "PT509221785",
            "PT509280285",
            "PT509626416",
            "PT510765009",
            "PT980405319",
            "501442600",
            "504296434",
            "500100144",
            "131546473",
            "PT999999990",
        ]
        self.vat_pt_invalid = [
            "PT999999999",
            "PT502757192",
            "PT100000012",
            "PT100000022",
            "PT100000032",
            "PT100000192",
            "PT100000052",
        ]

    def test_vat_is_valid_pt(self):
        for vat in self.vat_pt_valid:
            self.assertTrue(vat_is_valid_pt(vat), vat)
        for vat in self.vat_pt_invalid:
            self.assertFalse(vat_is_valid_pt(vat))
