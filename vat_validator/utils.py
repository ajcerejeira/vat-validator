from typing import List
import re

from .countries import EU_COUNTRY_CODES, EU_RULES


def validate_vat(country_code: str, vat: str) -> bool:
    """Validates a VAT number against the given country VAT format
    specification. It also takes care of sanitizing the VAT code, removing
    whitespaces and other invalid characters according to the country rules.
    It is not required for the VAT to start with the country code, so for
    example 'PT 980405319' and '980405319' will both yield the same result.

    :param country_code: valid IS0 3166 country code.
    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    :raises ValueError: when the country code is invalid.
    """
    if country_code not in EU_RULES:
        raise ValueError("Invalid country code")
    rule = EU_RULES[country_code]
    return rule(vat)


def countries_where_vat_is_valid(vat: str) -> List[str]:
    """Finds the countries where a given VAT code is valid.

    :param vat: VAT number to validate.
    :return: list of country codes where the given VAT is valid.
    """
    return [country for country, rule in EU_RULES.items() if rule(vat)]


def sanitize_vat(vat: str) -> str:
    """Sanitizes a given VAT code, removing the country prefix, whitespace and
    other non alphanumeric characters.

    :param vat: VAT code to sanitize.
    :return: sanitized VAT code.

    **Example**

    >>> sanitize_vat('PT 502.011.378')
    '502011378'
    """
    prefixes = "|".join(
        r"(^{})".format(country) for country in EU_COUNTRY_CODES
    )
    return re.sub(r"{}|\s*|\W*".format(prefixes), "", vat, flags=re.I)
