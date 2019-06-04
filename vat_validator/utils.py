from typing import List
from .countries import EU_RULES


def validate_vat(country_code: str, vat: str) -> bool:
    """Validates a VAT number against the given country VAT format
    specification.

    :param country_code: valid IS0 3166 country code
    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    :raises ValueError: when the country code is invalid.
    """
    if country_code not in EU_RULES:
        raise ValueError('Invalid country code')
    rule = EU_RULES[country_code]
    return rule(vat)


def countries_where_vat_is_valid(vat: str) -> List[str]:
    return [country for country, rule in EU_RULES.items() if rule(vat)]
