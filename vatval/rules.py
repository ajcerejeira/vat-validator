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
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    double_every_other = (digit * (2 if index % 2 != 0 else 1)
                          for index, digit in enumerate(digits))
    sum_digits = sum(n if n <= 9 else floor(n / 10) + n % 10
                     for n in double_every_other)
    check_digit = int(str(10 - (sum_digits + 4) % 10)[-1])
    return check_digit == last_digit


def belgium_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(BE)?([01]?\d{9})$', vat)
    return bool(match)


def bulgaria_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(BG)?\d{9,10}$', vat)
    return bool(match)


def croatia_vat_rule(vat: str) -> bool:
    """Validates a VAT number against croatian VAT format specification.
    In Croatia is also named "PDV Id. Broj OIB" (PDV-ID; OIB).
    The number must contain 11 digits and the last digit is the check digit.
    It uses MOD 11-10 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(HR)?(\d{11})$', vat)
    if not match:
        return False
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    product = 10
    for digit in digits:
        soma = (digit + product) % 10
        if soma == 0:
            soma = 10
        product = (2 * soma) % 11
    return (product + last_digit) % 10 == 1


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
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    digits_with_weight = zip(digits, [2, 7, 6, 5, 4, 3, 2])
    mod = sum(digit * weight for digit, weight in digits_with_weight) % 11
    check_digit = 0 if mod in [0, 1] else 11 - mod
    return check_digit == last_digit


def estonia_vat_rule(vat: str) -> bool:
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
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    digits_with_weight = zip(digits, [7, 9, 10, 5, 8, 4, 2])
    mod = sum(digit * weight for digit, weight in digits_with_weight) % 11
    check_digit = 0 if mod in [0, 1] else 11 - mod
    return check_digit == last_digit


def france_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(FR)?\w{2}\d{9}', vat)
    return bool(match)


def germany_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(DE)?(\d{9})$', vat)
    return bool(match)


def greece_vat_rule(vat: str) -> bool:
    """Validates a VAT number against greece VAT format specification.
    In Greece is also named "Arithmós Forologikou Mētrṓou" (ΑΦΜ).
    The number must contain 9 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(EL|GR)?(\d{9})$', vat)
    if not match:
        return False
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    digits_with_weight = zip(digits, [256, 128, 64, 32, 16, 8, 4, 2])
    mod = sum(digit * weight for digit, weight in digits_with_weight) % 11
    check_digit = 0 if mod > 9 else mod
    return check_digit == last_digit


def hungary_vat_rule(vat: str) -> bool:
    """Validates a VAT number against hungarian VAT format specification.
    In Hungary is also named "Közösségi adószám" (ΑNUM).
    The number must contain 8 digits and the last digit is the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(HU)?(\d{8})$', vat)
    if not match:
        return False
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    digits_with_weight = zip(digits, [9, 7, 3, 1, 9, 7, 3])
    mod = 10 - sum(digit * weight for digit, weight in digits_with_weight) % 10
    check_digit = 0 if mod == 10 else mod
    return check_digit == last_digit


def ireland_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(IE)?\dS\d{5}L$', vat)
    return bool(match)


def italy_vat_rule(vat: str) -> bool:
    """Validates a VAT number against italien VAT format specification.
    In Italy is also named "Partita IVA" (P.IVA).
    The number must contain 11 digits and the last digit is the check digit.
    It uses Luhn Algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso: https://en.wikipedia.org/wiki/Luhn_algorithm
    """
    match = re.match(r'^(IT)?(\d{11})$', vat)
    if not match:
        return False
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    double_every_other = (digit * (2 if index % 2 != 0 else 1)
                          for index, digit in enumerate(digits))
    sum_digits = sum(number if number <= 9 else number - 9
                     for number in double_every_other)
    check_digit = int(str(sum_digits * 9)[-1])
    return check_digit == last_digit


def latvia_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(LV)?\d{11}$', vat)
    return bool(match)


def lithuania_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(LT)?(\d{9}|\d{12})$', vat)
    return bool(match)


def luxembourg_vat_rule(vat: str) -> bool:
    """Validates a VAT number against luxembourg VAT format specification.
    In Luxembourg is also named "Numéro d'identification à la taxe sur la
    valeur ajoutée" (No. TVA).
    The number must contain 8 digits and the last two digits are the check
    digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(LU)?(\d{8})$', vat)
    if not match:
        return False
    number = match.group(2)
    last_digit = int(number[6:])
    check_digit = int(number[:6]) % 89
    return check_digit == last_digit


def malta_vat_rule(vat: str) -> bool:
    """Validates a VAT number against maltese VAT format specification.
    In Malta is also named "Vat reg. no." (VAT No.).
    The number must contain 8 digits and the last two digits are the check
    digits.
    It uses MOD 37 algorithm to calculate the check digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(MT)?(\d{8})$', vat)
    if not match:
        return False
    digits = [int(digit) for digit in match.group(2)[:6]]
    last_digit = int(match.group(2)[6:])
    digits_with_weight = zip(digits, [3, 4, 6, 7, 8, 9])
    mod = 37 - sum(digit * weight for digit, weight in digits_with_weight) % 37
    return mod == last_digit


def netherlands_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(NL)?\d{9}B\d{2}$', vat)
    return bool(match)


def poland_vat_rule(vat: str) -> bool:
    """Validates a VAT number against polish VAT format specification.
    In Poland is also named "numer identyfikacji podatkowej" (NIP).
    The number must contain 10 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(PL)?(\d{10})$', vat)
    if not match:
        return False
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    digits_with_weight = zip(digits, [6, 5, 7, 2, 3, 4, 5, 6, 7])
    mod = sum(digit * weight for digit, weight in digits_with_weight) % 11
    check_digit = 0 if mod > 9 else mod
    return check_digit == last_digit


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
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    digits_with_weight = zip(digits, [9, 8, 7, 6, 5, 4, 3, 2])
    mod = sum(digit * weight for digit, weight in digits_with_weight) % 11
    check_digit = 0 if mod in [0, 1] else 11 - mod
    return check_digit == last_digit


def romania_vat_rule(vat: str) -> bool:
    """Validates a VAT number against romanian VAT format specification.
    In Romania is also named "Codul de identificare fiscală" (CIF).
    The number must contain 2 to 10 digits and the last digit is the check
    digit. It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso: https://vatdesk.eu/en/romania/
    """
    match = re.match(r'^(RO)?(\d{2,10})$', vat)
    if not match:
        return False
    digits = [int(digit) for digit in match.group(2)]
    weights = [7, 5, 3, 2, 1, 7, 5, 3, 2][10 - len(digits):]
    digits_with_weight = zip(digits, weights)
    mod = 10 * sum(digit * weight for digit, weight in digits_with_weight) % 11
    check_digit = 0 if mod == 10 else mod
    return check_digit == digits[-1]


def spain_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(ES)?\w\d{7}\w$', vat)
    return bool(match)


def slovenia_vat_rule(vat: str) -> bool:
    """Validates a VAT number against slovenian VAT format specification.
    In Slovenia is also named "Davčna številka" (ID za DDV).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(SI)?(\d{8})$', vat)
    if not match:
        return False
    *digits, last_digit = [int(digit) for digit in match.group(2)]
    digits_with_weight = zip(digits, [8, 7, 6, 5, 4, 3, 2])
    mod = 11 - sum(digit * weight for digit, weight in digits_with_weight) % 11
    check_digit = 0 if mod == 10 else mod
    return check_digit != 11 and check_digit == last_digit


def slovakia_vat_rule(vat: str) -> bool:
    """Validates a VAT number against slovakian VAT format specification.
    In Slovakia is also named "	Identifikačné číslo pre daň z pridanej hodnoty"
    (IČ DPH).
    The number must contain 10 digits and be divisible by 11.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(SK)?(\d{10})$', vat)
    if not match:
        return False
    return int(match.group(2)) % 11 == 0


def sweden_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(SE)?\d{12}$', vat)
    return bool(match)


def united_kingdom_vat_rule(vat: str) -> bool:
    # TODO
    match = re.match(r'^(GB)?(\d{9}(\d{3})?|[A-Z]{2}\d{3})$', vat)
    return bool(match)


#: Maps a country code to the respective country VAT rule
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
