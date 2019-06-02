from math import floor
from typing import Callable, Dict
import re


def austria_vat_rule(vat: str) -> bool:
    """Validates a VAT number against austrian VAT format specification.
    In Austria is also named "Umsatzsteuer-Identifikationsnummer" (UID).
    The number must contain the letter 'U' followed by 8 digits and the last
    digit is the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(AT)?U(\d{8})$', vat)
    if not match:
        return False
    number = match.group(2)
    double_every_other = (int(digit) * (2 if index % 2 != 0 else 1)
                          for index, digit in enumerate(number[:-1]))
    sum_digits = sum(n if n <= 9 else floor(n / 10) + n % 10
                     for n in double_every_other)
    check_digit = str(10 - (sum_digits + 4) % 10)[-1]
    return check_digit == number[-1]


def belgium_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(BE)?([01]?\d{9})$', vat)
    return bool(match)


def bulgaria_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(BG)?\d{9,10}$', vat)
    return bool(match)


def croatia_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(HR)?(\d{11})$', vat)
    return bool(match)


def cyprus_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(CY)?(\d{9})L$', vat)
    return bool(match)


def czech_republic_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(CZ)?(\d{8,10})$', vat)
    return bool(match)


def denmark_vat_rule(vat: str) -> bool:
    """Validates a VAT number against dannish VAT format specification.
    In Denmark is also named "Momsregistreringsnummer" (CVR).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso: https://erhvervsstyrelsen.dk/modulus_11
    """
    match = re.match(r'^(DK)?(\d{8})$', vat)
    if not match:
        return False
    number = match.group(2)
    coefs = [2, 7, 6, 5, 4, 3, 2, 0]
    res = sum(int(digit) * coefs[index] for index, digit in enumerate(number))
    mod = res % 11
    check_digit = 0 if mod == 0 else 11 - mod
    return check_digit == int(vat[-1])


def estonia_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(EE)?(\d{9})$', vat)
    return bool(match)


def finland_vat_rule(vat: str) -> bool:
    """Validates a VAT number against finnish VAT format specification.
    In Finland is also named "Arvonlisäveronumero" (AVL nro).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11-2 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso: http://tarkistusmerkit.teppovuori.fi/tarkmerk.htm#y-tunnus2
    """
    match = re.match(r'^(FI)?(\d{8})$', vat)
    if not match:
        return False
    number = match.group(2)
    coefs = [7, 9, 10, 5, 8, 4, 2, 0]
    res = sum(int(digit) * coefs[index] for index, digit in enumerate(number))
    mod = res % 11
    check_digit = 0 if mod == 0 else 11 - mod
    return check_digit == int(vat[-1])


def france_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(FR)?\w{2}\d{9}', vat)
    return bool(match)


def germany_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(DE)?(\d{9})$', vat)
    return bool(match)


def greece_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(EL|GR)?\d{9}$', vat)
    return bool(match)


def hungary_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(HU)?\d{8}$', vat)
    return bool(match)


def ireland_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(IE)?\dS\d{5}L$', vat)
    return bool(match)


def italy_vat_rule(vat: str) -> bool:
    """Validates a VAT number against italien VAT format specification.
    In Italy is also named "Partita IVA" (P.IVA).
    The number must contain 11 digits and the last digit is the check digit.
    It uses Luhn Algorithm algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso: https://en.wikipedia.org/wiki/Luhn_algorithm
    """
    match = re.match(r'^(IT)?(\d{11})$', vat)
    if not match:
        return False
    number = match.group(2)
    double_every_other = (int(digit) * (2 if index % 2 != 0 else 1)
                          for index, digit in enumerate(number[:-1]))
    sum_digits = sum(n if n <= 9 else n - 9 for n in double_every_other)
    check_digit = str(sum_digits * 9)[-1]
    return check_digit == vat[-1]


def lithuania_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(LT)?(\d{9}|\d{12})$', vat)
    return bool(match)


def luxembourg_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(LU)?\d{8}$', vat)
    return bool(match)


def latvia_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(LV)?\d{11}$', vat)
    return bool(match)


def malta_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(MT)?\d{8}$', vat)
    return bool(match)


def netherlands_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(NL)?\d{9}B\d{2}$', vat)
    return bool(match)


def poland_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(PL)?\d{10}$', vat)
    return bool(match)


def portugal_vat_rule(vat: str) -> bool:
    """Validates a VAT number against portuguese VAT format specification.
    In Portugal is also named "Número de Identificação Fiscal" (NIF).
    The number must contain 9 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso: https://pt.wikipedia.org/wiki/Número_de_identificação_fiscal
    """
    match = re.match(r'^(PT)?(\d{9})$', vat)
    if not match:
        return False
    number = match.group(2)
    res = sum(int(digit) * (9 - index) for index, digit in enumerate(number))
    mod = res % 11
    if int(vat[-1]) == 0 and mod == 1:
        mod = (res + 10) % 11
    return mod == 0


def romania_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(RO)?\d{2,10}$', vat)
    return bool(match)


def spain_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(ES)?\w\d{7}\w$', vat)
    return bool(match)


def sweden_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(SE)?\d{12}$', vat)
    return bool(match)


def slovenia_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(SI)?\d{8}$', vat)
    return bool(match)


def slovakia_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(SK)?\d{10}$', vat)
    return bool(match)


def united_kingdom_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(GB)?(\d{9}(\d{3})?|[A-Z]{2}\d{3})$', vat)
    return bool(match)


EU_RULES: Dict[str, Callable[[str], bool]] = {
    'AT': austria_vat_rule,
    'BE': belgium_vat_rule,
    'BG': bulgaria_vat_rule,
    'HR': croatia_vat_rule,
    'CY': cyprus_vat_rule,
    'CZ': czech_republic_vat_rule,
    'DE': germany_vat_rule,
    'DK': denmark_vat_rule,
    'EE': estonia_vat_rule,
    'EL': greece_vat_rule,
    'ES': spain_vat_rule,
    'FI': finland_vat_rule,
    'FR': france_vat_rule,
    'GB': united_kingdom_vat_rule,
    'HU': hungary_vat_rule,
    'IE': ireland_vat_rule,
    'IT': italy_vat_rule,
    'LT': lithuania_vat_rule,
    'LU': luxembourg_vat_rule,
    'LV': latvia_vat_rule,
    'MT': malta_vat_rule,
    'NL': netherlands_vat_rule,
    'PL': poland_vat_rule,
    'PT': portugal_vat_rule,
    'RO': romania_vat_rule,
    'SE': sweden_vat_rule,
    'SI': slovenia_vat_rule,
    'SK': slovakia_vat_rule,
}
