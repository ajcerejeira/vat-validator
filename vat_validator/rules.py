"""
This module contains a set of functions that validate a VAT number according to
a country VAT format rules.

.. seealso::

   The list of VAT validation algorithms are published here:
   https://ec.europa.eu/taxation_customs/tin/

   This wikipedia page contains a great overview of the different formats:
   https://en.wikipedia.org/wiki/VAT_identification_number
"""
from math import floor, ceil
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
    c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    s3 = floor(c3 / 5) + (c3 * 2) % 10
    s5 = floor(c5 / 5) + (c5 * 2) % 10
    s7 = floor(c7 / 5) + (c7 * 2) % 10
    r = s3 + s5 + s7
    check_digit = (10 - (r + c2 + c4 + c6 + c8 + 4) % 10) % 10
    return check_digit == c9


def belgium_vat_rule(vat: str) -> bool:
    """Validates a VAT number against belgian VAT format specification.
    In Belgium is also named "BTW identificatienummer" (BTW-nr).
    The number must contain 10 digits starting with 0 or 1. The old numbering
    schema had 9 digits, and is also accepted by this function.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(BE)?([01]?\d{9})$', vat)
    if not match:
        return False
    number = match.group(2)
    # If the VAT is in the old format, convert it to the new one
    if len(number) == 9:
        number = '0' + number
    check_digits = (97 - int(number[:8])) % 97
    return check_digits == int(number[8:10])


def bulgaria_vat_rule(vat: str) -> bool:
    """Validates a VAT number against bulgarian VAT format specification.
    In Bulgary is also named "Identifikacionen nomer po DDS" (ДДС номер	).
    The number must contain 9 or 10 digits. It assumes one of four formats:
    "legal entities", "physical persons", "foreigners" and "miscellaneous".

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(BG)?(\d{9})(\d?)$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    c10 = int(match.group(3)) if match.group(3) else None

    def legal_entities_style() -> bool:
        if c10 is not None:
            return False
        r1 = ((1 * c1 + 2 * c2 + 3 * c3 + 4 * c4 + 5 * c5 + 6 * c6 + 7 * c7 +
               8 * c8) % 11)
        r2 = ((3 * c1 + 4 * c2 + 5 * c3 + 6 * c4 + 7 * c5 + 8 * c6 + 9 * c7 +
               10 * c8) % 11)
        return ((c9 == r1) or (r1 == 10 and r2 == 10 and c9 == 0) or
                (r1 == 10 and r2 != 10 and c9 == r2))

    def physical_persons_style() -> bool:
        if c10 is None:
            return False
        r = (2 * c1 + 4 * c2 + 8 * c3 + 5 * c4 + 10 * c5 + 9 * c6 + 7 * c7 +
             3 * c8 + 6 * c9) % 11
        return (r == 10 and c10 == 0) or (c10 == r)

    def foreigners_style() -> bool:
        if c10 is None:
            return False
        r = (21 * c1 + 19 * c2 + 17 * c3 + 13 * c4 + 11 * c5 + 9 * c6 +
             7 * c7 + 3 * c8 + 1 * c9) % 10
        return c10 == r

    def other_style() -> bool:
        if c10 is None:
            return False
        r = 11 - (4 * c1 + 3 * c2 + 2 * c3 + 7 * c4 + 6 * c5 + 5 * c6 +
                  4 * c7 + 3 * c8 + 2 * c9) % 11
        return r != 10 and ((r == 11 and r == 0) or (c10 == r))

    return (legal_entities_style() or
            physical_persons_style() or
            foreigners_style() or
            other_style())


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
    *digits, last_digit = map(int, match.group(2))
    product = 10
    for digit in digits:
        soma = (digit + product) % 10
        if soma == 0:
            soma = 10
        product = (2 * soma) % 11
    return (product + last_digit) % 10 == 1


def cyprus_vat_rule(vat: str) -> bool:
    """Validates a VAT number against cyprus VAT format specification.
    In Cyprus is also named "Arithmós Engraphḗs phi. pi. a." (ΦΠΑ).
    The number must contain 8 digits followed by a letter that is used to check
    the number.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(CY)?(\d{8})([A-Z])$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    c9 = match.group(3)
    k = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21]
    r = (c2 + c4 + c6 + c8 + k[c1] + k[c3] + k[c5] + k[c7]) % 26
    return chr(65 + r) == c9


def czech_republic_vat_rule(vat: str) -> bool:
    """Validates a VAT number against czech republic VAT format specification.
    In Czech Republic is also named "Daňové identifikační číslo" (DIČ).
    The number must contain 8 to 10 digits depending if it is a legar entity or
    individual.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(CZ)?(\d{8})(\d?)(\d?)$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    c9 = int(match.group(3)) if match.group(3) else None
    c10 = int(match.group(4)) if match.group(4) else None

    def legal_entities_style():
        if c9 is not None or c10 is not None:
            return False
        a1 = 8 * c1 + 7 * c2 + 6 * c3 + 5 * c4 + 4 * c5 + 3 * c6 + 2 * c7
        a2 = a1 + 11 if a1 % 11 == 0 else ceil(a1 / 11) * 11
        return c8 == (a2 - a1) % 10

    def individuals_style_1():
        if c9 is None or c10 is not None:
            return False
        year = int(''.join(map(str, [c1, c2])))
        month = int(''.join(map(str, [c3, c4])))
        day = int(''.join(map(str, [c5, c6])))

        return (year in range(0, 54) and
                (month in range(1, 13) or month in range(51, 63)) and
                day in range(1, 32))

    def individuals_style_2():
        if c9 is None or c10 is not None:
            return False
        a1 = 8 * c2 + 7 * c3 + 6 * c4 + 5 * c5 + 4 * c6 + 3 * c7 + 2 * c8
        a2 = a1 + 11 if a1 % 11 == 0 else ceil(a1 / 11) * 11
        return c9 == [0, 8, 7, 6, 5, 4, 3, 2, 1, 0, 9, 8][a2 - a1]

    def individuals_style_3():
        if c9 is None or c10 is None:
            return False
        r1 = int(''.join(map(str, [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])))
        r2 = (int(''.join(map(str, [c1, c2]))) +
              int(''.join(map(str, [c3, c4]))) +
              int(''.join(map(str, [c5, c6]))) +
              int(''.join(map(str, [c7, c8]))) +
              int(''.join(map(str, [c9, c10]))))
        return r1 % 11 == 0 and r2 % 11 == 0

    return (legal_entities_style() or individuals_style_1() or
            individuals_style_2() or individuals_style_3())


def denmark_vat_rule(vat: str) -> bool:
    """Validates a VAT number against dannish VAT format specification.
    In Denmark is also named "Momsregistreringsnummer" (CVR).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://erhvervsstyrelsen.dk/modulus_11
    """
    match = re.match(r'^(DK)?(\d{8})$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    r = 2 * c1 + 7 * c2 + 6 * c3 + 5 * c4 + 4 * c5 + 3 * c6 + 2 * c7 + c8
    return r % 11 == 0


def estonia_vat_rule(vat: str) -> bool:
    """Validates a VAT number against estoniaon VAT format specification.
    In Estonia is also named "Käibemaksukohustuslase number" (KMKR).
    The number must contain 9 digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(EE)?(\d{9})$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    r = 3 * c1 + 7 * c2 + 1 * c3 + 3 * c4 + 7 * c5 + 1 * c6 + 3 * c7 + 7 * c8
    return c9 == 10 * ceil(r / 10) - r


def finland_vat_rule(vat: str) -> bool:
    """Validates a VAT number against finnish VAT format specification.
    In Finland is also named "Arvonlisäveronumero" (AVL nro).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11-2 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: http://tarkistusmerkit.teppovuori.fi/tarkmerk.htm#y-tunnus2
    """
    match = re.match(r'^(FI)?(\d{8})$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    r = (11 - (7 * c1 + 9 * c2 + 10 * c3 + 5 * c4 + 8 * c5 + 4 * c6 + 2 * c7))\
        % 11
    return (r != 10) and ((r == 11 and c8 == 0) or (r == c8))


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
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    r = (256 * c1 + 128 * c2 + 64 * c3 + 32 * c4 + 16 * c5 + 8 * c6 + 4 * c7 +
         2 * c8) % 11
    return c9 == ((r % 11) % 10)


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
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    r = 9 * c1 + 7 * c2 + 3 * c3 + 1 * c4 + 9 * c5 + 7 * c6 + 3 * c7
    return ((r % 10 == 0) and (c8 == 0)) or (10 - (r % 10) == c8)


def ireland_vat_rule(vat: str) -> bool:
    """Validates a VAT number against irish VAT format specification.
    In Ireland is also named "Value added tax identification no." (VAT/CBL).
    The number must be in one of the following formats:

    - 7 digits and 1 letter, optionally followed by another letter
    - 1 digit, 1 letter or "+", "*" and 5 digits and 1 letter

    The number must contain 8 digits and the last digit is the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    def old_style(code: str) -> bool:
        match = re.match(r'^(IE)?(\d)([A-Z+*])(\d{5})([A-W])', code)
        if not match:
            return False
        c1 = int(match.group(2))
        c3, c4, c5, c6, c7 = map(int, match.group(4))
        _, c8 = match.group(3), match.group(5)
        r = (8 * 0 + 7 * c3 + 6 * c4 + 5 * c5 + 4 * c6 + 3 * c7 + 2 * c1) % 23
        check_chars = 'WABCDEFGHIJKLMNOPQRSTUV'
        return c8 == check_chars[r]

    def new_style(code: str) -> bool:
        match = re.match(r'^(IE)?(\d{7})([A-W])([A-IW])?', code)
        if not match:
            return False
        c1, c2, c3, c4, c5, c6, c7 = map(int, match.group(2))
        c8 = match.group(3)
        c9 = 'WABCDEFGHI'.index(match.group(4)) if match.group(4) else 0
        r = (9 * c9 + 8 * c1 + 7 * c2 + 6 * c3 + 5 * c4 + 4 * c5 + 3 * c6 +
             2 * c7) % 23
        check_chars = 'WABCDEFGHIJKLMNOPQRSTUV'
        return (r < len(check_chars)) and (c8 == check_chars[r])

    return old_style(vat) or new_style(vat)


def italy_vat_rule(vat: str) -> bool:
    """Validates a VAT number against italien VAT format specification.
    In Italy is also named "Partita IVA" (P.IVA).
    The number must contain 11 digits and the last digit is the check digit.
    It uses Luhn Algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://en.wikipedia.org/wiki/Luhn_algorithm
    """
    match = re.match(r'^(IT)?(\d{11})$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = map(int, match.group(2))
    d2 = floor(c2 / 5) + ((2 * c2) % 10)
    d4 = floor(c4 / 5) + ((2 * c4) % 10)
    d6 = floor(c6 / 5) + ((2 * c6) % 10)
    d8 = floor(c8 / 5) + ((2 * c8) % 10)
    d10 = floor(c10 / 5) + ((2 * c10) % 10)
    s1 = c1 + c3 + c5 + c7 + c9
    s2 = d2 + d4 + d6 + d8 + d10
    return c11 == (10 - (s1 + s2) % 10) % 10


def latvia_vat_rule(vat: str) -> bool:
    """Validates a VAT number against latvian VAT format specification.
    In Latvia is also named "Pievienotās vērtības nodokļa" (PVN).
    The number must contain 11 digits and can be in one of the following
    formats:

    - 1st digit is bigger than 3, and so use a MOD 11 algorithm
    - 1st digit is 3, 2nd digit is 2, followed by 9 digits
    - 2 digits represent a day of month, followed by 2 digits that represent
      the month, followed by 2 digits that represent the year, followed by 1
      digit equals to 0, 1 or 2, followed  by 4 digits

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    def style_1(code: str) -> bool:
        match = re.match(r'^(LV)?([4-9]\d{10})$', code)
        if not match:
            return False
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = map(int, match.group(2))
        r = 3 - ((9 * c1 + 1 * c2 + 4 * c3 + 8 * c4 + 3 * c5 + 10 * c6 +
                  2 * c7 + 5 * c8 + 7 * c9 + 6 * c10) % 11)
        return (r != -1) and ((r < -1 and c11 == r + 11) or
                              (r > -1 and c11 == r))

    def style_2(code: str) -> bool:
        match = re.match(r'^(LV)?32\d{9}', code)
        return bool(match)

    def style_3(code: str) -> bool:
        match = re.match(r'^(LV)?(\d{2})(\d{2})(\d{2})[012](\d{4})$', code)
        if not match:
            return False
        day, month, year = map(int, match.groups()[1:4])
        return day in range(0, 31) and month in range(0, 12)

    return style_1(vat) or style_2(vat) or style_3(vat)


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
    c1_c6 = int(match.group(2)[:6])
    c7_c8 = int(match.group(2)[6:])
    return c7_c8 == c1_c6 % 89


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
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    c7_c8 = int(''.join(map(str, [c7, c8])))
    r = 37 - (3 * c1 + 4 * c2 + 6 * c3 + 7 * c4 + 8 * c5 + 9 * c6) % 37
    return (r == 0 and c7_c8 == 37) or (c7_c8 == r)


def netherlands_vat_rule(vat: str) -> bool:
    """Validates a VAT number against netherlands VAT format specification.
    In Netherlands is also named "Btw-nummer" Btw-nr.).
    The number must contain 9 digits followed by the letter 'B' followed by 2
    digits.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r'^(NL)?(\d{9})B(\d{2})$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    c11, c12 = map(int, match.group(3))
    r = ((9 * c1 + 8 * c2 + 7 * c3 + 6 * c4 + 5 * c5 + 4 * c6 + 3 * c7 +
          2 * c8) % 11)
    return r != 10 and r == c9


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
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = map(int, match.group(2))
    r = (6 * c1 + 5 * c2 + 7 * c3 + 2 * c4 + 3 * c5 + 4 * c6 + 5 * c7 +
         6 * c8 + 7 * c9) % 11
    return r != 10 and r == c10


def portugal_vat_rule(vat: str) -> bool:
    """Validates a VAT number against portuguese VAT format specification.
    In Portugal is also named "Número de Identificação Fiscal" (NIF).
    The number must contain 9 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://pt.wikipedia.org/wiki/Número_de_identificação_fiscal
    """
    match = re.match(r'^(PT)?(\d{9})$', vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    r = 11 - (9 * c1 + 8 * c2 + 7 * c3 + 6 * c4 + 5 * c5 + 4 * c6 + 3 * c7 +
              2 * c8) % 11
    return ((r == 10 or r == 11) and c9 == 0) or (c9 == r)


def romania_vat_rule(vat: str) -> bool:
    """Validates a VAT number against romanian VAT format specification.
    In Romania is also named "Codul de identificare fiscală" (CIF).
    The number must contain 2 to 10 digits and the last digit is the check
    digit. It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://vatdesk.eu/en/romania/
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
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    r = 11 - ((c1 * 8 + c2 * 7 + c3 * 6 + c4 * 5 + c5 * 4 + c6 * 3 + c7 * 2)
              % 11)
    return (r != 11) and ((r == 10 and c8 == 0) or (c8 == r))


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
