"""This module contains a set of functions to validate a VAT number according
to a country VAT format rules. Besides the general regex match, the validation
functions perform some country specific calculations on the digits using
algorithms such as MOD 11 or Lunh's algorithm.

All of these functions are in the format ``vat_is_valid_XX`` where XX is the
IS0 3166 country code. They receive a string representing a VAT number in that
country format and return ``True`` or ``False`` whether that code is valid or
not.

**Usage**:

>>> vat_is_valid_pt('PT980405319')
True
>>> vat_is_valid_pt('PT-980 405 319')
True
>>> vat_is_valid_pt('980405319')
False

Each function is responsible to sanitize the input (remove preceding country
code, spaces, punctuation, *etc...*)


.. seealso::

   The list of VAT validation algorithms are published here:
   https://ec.europa.eu/taxation_customs/tin/

   This wikipedia page contains a great overview of the different formats:
   https://en.wikipedia.org/wiki/VAT_identification_number
"""


from vat_validator.countries import EU_COUNTRY_CODES
from vat_validator.sanitizers import sanitize_vat_pt


def vat_is_valid_at(vat: str) -> bool:
    return False


def vat_is_valid_be(vat: str) -> bool:
    return False


def vat_is_valid_bg(vat: str) -> bool:
    return False


def vat_is_valid_cy(vat: str) -> bool:
    return False


def vat_is_valid_cz(vat: str) -> bool:
    return False


def vat_is_valid_de(vat: str) -> bool:
    return False


def vat_is_valid_dk(vat: str) -> bool:
    return False


def vat_is_valid_ee(vat: str) -> bool:
    return False


def vat_is_valid_el(vat: str) -> bool:
    return False


def vat_is_valid_es(vat: str) -> bool:
    return False


def vat_is_valid_fi(vat: str) -> bool:
    return False


def vat_is_valid_fr(vat: str) -> bool:
    return False


def vat_is_valid_gb(vat: str) -> bool:
    return False


def vat_is_valid_hr(vat: str) -> bool:
    return False


def vat_is_valid_hu(vat: str) -> bool:
    return False


def vat_is_valid_ie(vat: str) -> bool:
    return False


def vat_is_valid_it(vat: str) -> bool:
    return False


def vat_is_valid_lt(vat: str) -> bool:
    return False


def vat_is_valid_lu(vat: str) -> bool:
    return False


def vat_is_valid_lv(vat: str) -> bool:
    return False


def vat_is_valid_mt(vat: str) -> bool:
    return False


def vat_is_valid_nl(vat: str) -> bool:
    return False


def vat_is_valid_pl(vat: str) -> bool:
    return False


def vat_is_valid_pt(vat: str) -> bool:
    sanitized_vat = sanitize_vat_pt(vat)
    if len(sanitized_vat) != 9 or not sanitized_vat.isdigit():
        return False
    digits = [int(digit) for digit in sanitized_vat]
    sum_digits = sum(digit * (9 - pos) for pos, digit in enumerate(digits))
    resto = sum_digits % 11
    if digits[-1] == 0 and resto == 1:
        resto = (sum_digits + 10) % 11
    return resto == 0


def vat_is_valid_ro(vat: str) -> bool:
    return False


def vat_is_valid_se(vat: str) -> bool:
    return False


def vat_is_valid_sl(vat: str) -> bool:
    return False


def vat_is_valid_sk(vat: str) -> bool:
    return False


def vat_is_valid(country_code: str, vat: str) -> bool:
    if country_code not in EU_COUNTRY_CODES:
        raise ValueError("Invalid country code: '{}'".format(country_code))
    validators = {
        "AT": vat_is_valid_at,
        "BE": vat_is_valid_be,
        "BG": vat_is_valid_bg,
        "CY": vat_is_valid_cy,
        "CZ": vat_is_valid_cz,
        "DE": vat_is_valid_de,
        "DK": vat_is_valid_dk,
        "EE": vat_is_valid_ee,
        "EL": vat_is_valid_el,
        "ES": vat_is_valid_es,
        "FI": vat_is_valid_fi,
        "FR": vat_is_valid_fr,
        "GB": vat_is_valid_gb,
        "HR": vat_is_valid_hr,
        "HU": vat_is_valid_hu,
        "IE": vat_is_valid_ie,
        "IT": vat_is_valid_it,
        "LT": vat_is_valid_lt,
        "LU": vat_is_valid_lu,
        "LV": vat_is_valid_lv,
        "MT": vat_is_valid_mt,
        "NL": vat_is_valid_nl,
        "PL": vat_is_valid_pl,
        "PT": vat_is_valid_pt,
        "RO": vat_is_valid_ro,
        "SE": vat_is_valid_se,
        "SL": vat_is_valid_sl,
        "SK": vat_is_valid_sk,
    }
    return validators[country_code](vat)
