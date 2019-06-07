"""
This module contains a set of functions to validate a VAT number according to
a country VAT format rules. Besides the general regex match, the validation
functions perform some country specific calculations on the digits using
algorithms such as MOD 11 or Lunh's algorithm.

All of these functions are in the format ``validate_vat_XX`` where XX is the
IS0 3166 country code. They receive a string representing a VAT number in that
country format and return ``True`` or ``False`` whether that code is valid or
not.

**Usage**:

>>> validate_vat_pt('PT980405319')
True
>>> validate_vat_pt('PT-980 405 319')
True
>>> validate_vat_pt('80405319')
False

Each function is responsible to sanitize the input (remove preciding country
code, spaces, punctuation, *etc...*)


.. seealso::

   The list of VAT validation algorithms are published here:
   https://ec.europa.eu/taxation_customs/tin/

   This wikipedia page contains a great overview of the different formats:
   https://en.wikipedia.org/wiki/VAT_identification_number
"""
from functools import reduce
from math import floor, ceil
from typing import Callable, Dict, List, Optional
import re


def validate_vat_at(vat: str) -> bool:
    """Validates a VAT number against austrian VAT format specification.
    In Austria is also named "Umsatzsteuer-Identifikationsnummer" (UID).
    The number must contain the letter 'U' followed by 8 digits and the last
    digit is the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """

    def calc_check_digit(code: str) -> int:
        c2, c3, c4, c5, c6, c7, c8 = map(int, code)
        s3 = floor(c3 / 5) + (c3 * 2) % 10
        s5 = floor(c5 / 5) + (c5 * 2) % 10
        s7 = floor(c7 / 5) + (c7 * 2) % 10
        return (10 - (s3 + s5 + s7 + c2 + c4 + c6 + c8 + 4) % 10) % 10

    sanitized_vat = re.sub(r"(^AT)|\s*|\W*", "", vat, flags=re.I)
    if len(sanitized_vat) != 9:
        return False
    if sanitized_vat[0] != "U" and sanitized_vat[0] != "u":
        return False
    if not sanitized_vat[1:].isdigit():
        return False
    return calc_check_digit(sanitized_vat[1:-1]) == int(sanitized_vat[-1])


def validate_vat_be(vat: str) -> bool:
    """Validates a VAT number against belgian VAT format specification.
    In Belgium is also named "BTW identificatienummer" (BTW-nr).
    The number must contain 10 digits starting with 0 or 1. The old numbering
    schema had 9 digits, and is also accepted by this function.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    sanitized_vat = re.sub(r"(^BE)|\s*|\W*", "", vat, flags=re.I)
    # If the VAT is in the old format, convert to the new one
    if len(sanitized_vat) == 9:
        sanitized_vat = "0" + sanitized_vat
    if len(sanitized_vat) != 10:
        return False
    if not sanitized_vat.isdigit():
        return False
    if sanitized_vat[0] != "0" or sanitized_vat[1] == "0":
        return False
    return 97 - int(sanitized_vat[:-2]) % 97 == int(sanitized_vat[-2:])


def validate_vat_bg(vat: str) -> bool:
    """Validates a VAT number against bulgarian VAT format specification.
    In Bulgary is also named "Identifikacionen nomer po DDS" (ДДС номер	).
    The number must contain 9 or 10 digits. It assumes one of four formats:
    "legal entities", "physical persons", "foreigners" and "miscellaneous".

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """

    def calc_check_digit_legal_entity(code: str) -> int:
        check_digit = sum(i * int(ch) for i, ch in enumerate(code, 1)) % 11
        if check_digit == 10:
            check_digit = sum(i * int(ch) for i, ch in enumerate(code, 3)) % 11
        return check_digit % 10

    def calc_check_digit_person(code: str) -> int:
        weights = (2, 4, 8, 5, 10, 9, 7, 3, 6)
        return sum(w * int(ch) for w, ch in zip(weights, code)) % 11 % 10

    def calc_check_digit_foreigner(code: str) -> int:
        weights = (21, 19, 17, 13, 11, 9, 7, 3, 1)
        return sum(w * int(ch) for w, ch in zip(weights, code)) % 10

    def calc_check_digit_misc(code: str) -> Optional[int]:
        weights = (4, 3, 2, 7, 6, 5, 4, 3, 2)
        check_digit = (
            11 - sum(w * int(ch) for w, ch in zip(weights, code)) % 11
        )
        if check_digit == 11:
            return 0
        elif check_digit == 10:
            return None
        else:
            return check_digit

    sanitized_vat = re.sub(r"(^BG)|\s*|\W*", "", vat, flags=re.I)
    if not sanitized_vat.isdigit():
        return False
    if len(sanitized_vat) == 9:
        check_digit = calc_check_digit_legal_entity(sanitized_vat[:-1])
        return check_digit == int(sanitized_vat[-1])
    elif len(sanitized_vat) == 10:
        # Check if it corresponds to a physical person VAT
        check_digit_person = calc_check_digit_person(sanitized_vat[:-1])
        year_is_valid = int(sanitized_vat[:2]) in range(0, 100)
        month_is_valid = int(sanitized_vat[2:4]) in range(1, 41)
        day_is_valid = int(sanitized_vat[4:6]) in range(1, 31)
        date_is_valid = year_is_valid and month_is_valid and day_is_valid
        is_person = (
            check_digit_person == int(sanitized_vat[-1]) and date_is_valid
        )

        # Check if it corresponds to a foreigner VAT
        check_digit_foreigner = calc_check_digit_foreigner(sanitized_vat[:-1])
        is_foreigner = check_digit_foreigner == int(sanitized_vat[-1])

        # Check if ti corresponds to a miscellaneous VAT
        check_digit_misc = calc_check_digit_misc(sanitized_vat[:-1])
        is_miscellaneous = check_digit_misc == int(sanitized_vat[-1])

        return is_person or is_foreigner or is_miscellaneous
    else:
        return False


def validate_vat_cy(vat: str) -> bool:
    """Validates a VAT number against cyprus VAT format specification.
    In Cyprus is also named "Arithmós Engraphḗs phi. pi. a." (ΦΠΑ).
    The number must contain 8 digits followed by a letter that is used to check
    the number.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """

    def calc_check_char(code: str) -> str:
        key = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21]
        check_char = (
            sum(int(ch) for ch in code[1::2])
            + sum(key[int(ch)] for ch in code[::2])
        ) % 26
        return chr(65 + check_char)

    sanitized_vat = re.sub(r"(^CY)|\s*|\W*", "", vat, flags=re.I)
    if not sanitized_vat[:-1].isdigit():
        return False
    if not sanitized_vat[-1].isalpha():
        return False
    if len(sanitized_vat) != 9:
        return False
    if sanitized_vat[0:2] == "12":
        return False
    return calc_check_char(sanitized_vat[:-1]) == sanitized_vat[-1]


def validate_vat_cz(vat: str) -> bool:
    """Validates a VAT number against czech republic VAT format specification.
    In Czech Republic is also named "Daňové identifikační číslo" (DIČ).
    The number must contain 8 to 10 digits depending if it is a legar entity or
    individual.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(CZ)?(\d{8})(\d?)(\d?)$", vat)
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
        year = int("".join(map(str, [c1, c2])))
        month = int("".join(map(str, [c3, c4])))
        day = int("".join(map(str, [c5, c6])))

        return (
            year in range(0, 54)
            and (month in range(1, 13) or month in range(51, 63))
            and day in range(1, 32)
        )

    def individuals_style_2():
        if c9 is None or c10 is not None:
            return False
        a1 = 8 * c2 + 7 * c3 + 6 * c4 + 5 * c5 + 4 * c6 + 3 * c7 + 2 * c8
        a2 = a1 + 11 if a1 % 11 == 0 else ceil(a1 / 11) * 11
        return c9 == [0, 8, 7, 6, 5, 4, 3, 2, 1, 0, 9, 8][a2 - a1]

    def individuals_style_3():
        if c9 is None or c10 is None:
            return False
        r1 = int("".join(map(str, [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])))
        r2 = (
            int("".join(map(str, [c1, c2])))
            + int("".join(map(str, [c3, c4])))
            + int("".join(map(str, [c5, c6])))
            + int("".join(map(str, [c7, c8])))
            + int("".join(map(str, [c9, c10])))
        )
        return r1 % 11 == 0 and r2 % 11 == 0

    return (
        legal_entities_style()
        or individuals_style_1()
        or individuals_style_2()
        or individuals_style_3()
    )


def validate_vat_de(vat: str) -> bool:
    """Validates a VAT number against german VAT format specification.
    In Germany is also named "Umsatzsteuer-Identifikationsnummer" (USt-IdNr).
    The number must contain 9 digits and the first one cannot be 0.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(DE)?(\d{9})$", vat)
    if not match:
        return False
    *c1_c8, c9 = map(int, match.group(2))
    p = reduce(
        lambda x, c: ((2 * (10 if (c + x) % 10 == 0 else (c + x) % 10)) % 11),
        c1_c8,
        10,
    )
    r = 11 - p
    return (c1_c8[0] > 0) and ((r == 10 and c9 == 0) or (c9 == r))


def validate_vat_dk(vat: str) -> bool:
    """Validates a VAT number against dannish VAT format specification.
    In Denmark is also named "Momsregistreringsnummer" (CVR).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://erhvervsstyrelsen.dk/modulus_11
    """

    def checksum(code: str) -> int:
        weights = (2, 7, 6, 5, 4, 3, 2, 1)
        return sum(weight * int(ch) for weight, ch in zip(weights, code)) % 11

    sanitized_vat = re.sub(r"(^DK)|\s*|\W*", "", vat, flags=re.I)
    if not sanitized_vat.isdigit():
        return False
    if len(sanitized_vat) != 8:
        return False
    if sanitized_vat[0] == "0":
        return False
    return checksum(sanitized_vat) == 0


def validate_vat_ee(vat: str) -> bool:
    """Validates a VAT number against estoniaon VAT format specification.
    In Estonia is also named "Käibemaksukohustuslase number" (KMKR).
    The number must contain 9 digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(EE)?(\d{9})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    r = 3 * c1 + 7 * c2 + 1 * c3 + 3 * c4 + 7 * c5 + 1 * c6 + 3 * c7 + 7 * c8
    return c9 == 10 * ceil(r / 10) - r


def validate_vat_el(vat: str) -> bool:
    """Validates a VAT number against greece VAT format specification.
    In Greece is also named "Arithmós Forologikou Mētrṓou" (ΑΦΜ).
    The number must contain 9 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(EL|GR)?(\d{9})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    r = (
        256 * c1
        + 128 * c2
        + 64 * c3
        + 32 * c4
        + 16 * c5
        + 8 * c6
        + 4 * c7
        + 2 * c8
    ) % 11
    return c9 == ((r % 11) % 10)


def validate_vat_es(vat: str) -> bool:
    match = re.match(r"^(ES)?(\w)(\d{7})(\w)$", vat)
    if not match:
        return False
    return bool(match)


def validate_vat_fi(vat: str) -> bool:
    """Validates a VAT number against finnish VAT format specification.
    In Finland is also named "Arvonlisäveronumero" (AVL nro).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11-2 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: http://tarkistusmerkit.teppovuori.fi/tarkmerk.htm#y-tunnus2
    """

    def checksum(code: str) -> int:
        weights = (7, 9, 10, 5, 8, 4, 2, 1)
        return sum(weight * int(ch) for weight, ch in zip(weights, code)) % 11

    sanitized_vat = re.sub(r"(^FI)|\s*|\W*", "", vat, flags=re.I)
    if not sanitized_vat.isdigit():
        return False
    if len(sanitized_vat) != 8:
        return False
    return checksum(sanitized_vat) == 0


def validate_vat_fr(vat: str) -> bool:
    """Validates a VAT number against french VAT format specification.
    In France is also named "Numéro de TVA intracommunautaire" (TVA).
    The number must contain 2 control characters followed by 9 digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(FR?)?(\d{2})(\d{9})", vat)
    if not match:
        return False
    return int(match.group(2)) == (int(match.group(3)) * 100 + 12) % 97


def validate_vat_gb(vat: str) -> bool:
    # TODO
    match = re.match(r"^(GB)?(\d{9}(\d{3})?|[A-Z]{2}\d{3})$", vat)
    return bool(match)


def validate_vat_hr(vat: str) -> bool:
    """Validates a VAT number against croatian VAT format specification.
    In Croatia is also named "PDV Id. Broj OIB" (PDV-ID; OIB).
    The number must contain 11 digits and the last digit is the check digit.
    It uses MOD 11-10 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(HR)?(\d{11})$", vat)
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


def validate_vat_hu(vat: str) -> bool:
    """Validates a VAT number against hungarian VAT format specification.
    In Hungary is also named "Közösségi adószám" (ΑNUM).
    The number must contain 8 digits and the last digit is the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(HU)?(\d{8})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    r = 9 * c1 + 7 * c2 + 3 * c3 + 1 * c4 + 9 * c5 + 7 * c6 + 3 * c7
    return ((r % 10 == 0) and (c8 == 0)) or (10 - (r % 10) == c8)


def validate_vat_ie(vat: str) -> bool:
    """Validates a VAT number against irish VAT format specification.
    In Ireland is also named "Value added tax identification no." (VAT/CBL).
    The number must be in one of the following formats:

    - 7 digits and 1 letter, optionally followed by another letter
    - 1 digit, 1 letter or "+", "*" and 5 digits and 1 letter

    The number must contain 8 digits and the last digit is the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """

    def old_style() -> bool:
        match = re.match(r"^(IE)?(\d)([A-Z+*])(\d{5})([A-W])", vat)
        if not match:
            return False
        c1 = int(match.group(2))
        c3, c4, c5, c6, c7 = map(int, match.group(4))
        _, c8 = match.group(3), match.group(5)
        r = (8 * 0 + 7 * c3 + 6 * c4 + 5 * c5 + 4 * c6 + 3 * c7 + 2 * c1) % 23
        check_chars = "WABCDEFGHIJKLMNOPQRSTUV"
        return c8 == check_chars[r]

    def new_style() -> bool:
        match = re.match(r"^(IE)?(\d{7})([A-W])([A-IW])?", vat)
        if not match:
            return False
        c1, c2, c3, c4, c5, c6, c7 = map(int, match.group(2))
        c8 = match.group(3)
        c9 = "WABCDEFGHI".index(match.group(4)) if match.group(4) else 0
        r = (
            9 * c9
            + 8 * c1
            + 7 * c2
            + 6 * c3
            + 5 * c4
            + 4 * c5
            + 3 * c6
            + 2 * c7
        ) % 23
        check_chars = "WABCDEFGHIJKLMNOPQRSTUV"
        return (r < len(check_chars)) and (c8 == check_chars[r])

    return old_style() or new_style()


def validate_vat_it(vat: str) -> bool:
    """Validates a VAT number against italien VAT format specification.
    In Italy is also named "Partita IVA" (P.IVA).
    The number must contain 11 digits and the last digit is the check digit.
    It uses Luhn Algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://en.wikipedia.org/wiki/Luhn_algorithm
    """
    match = re.match(r"^(IT)?(\d{11})$", vat)
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


def validate_vat_lt(vat: str) -> bool:
    """Validates a VAT number against lithuanian VAT format specification.
    In Lithuania is also named "Pridėtinės vertės mokestis" (PVM KODAS).
    The number must contain 9 or 12 digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """

    def legal_persons_style() -> bool:
        match = re.match(r"^(LT)?(\d{9})$", vat)
        if not match:
            return False
        c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
        if c8 != 1:
            return False
        r1 = (
            1 * c1
            + 2 * c2
            + 3 * c3
            + 4 * c4
            + 5 * c5
            + 6 * c6
            + 7 * c7
            + 8 * c8
        ) % 11
        r2 = (
            3 * c1
            + 4 * c2
            + 5 * c3
            + 6 * c4
            + 7 * c5
            + 8 * c6
            + 9 * c7
            + 1 * c8
        ) % 11
        if r1 % 10 != 0:
            return c9 == r1
        else:
            return (r2 == 10 and c9 == 0) or (c9 == r2)

    def temporary_registered_taxpayers_style() -> bool:
        match = re.match(r"^(LT)?(\d{12})$", vat)
        if not match:
            return False
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12 = map(
            int, match.group(2)
        )
        if c11 != 1:
            return False
        r1 = (
            1 * c1
            + 2 * c2
            + 3 * c3
            + 4 * c4
            + 5 * c5
            + 6 * c6
            + 7 * c7
            + 8 * c8
            + 9 * c9
            + 1 * c10
            + 2 * c11
        ) % 11
        r2 = (
            3 * c1
            + 4 * c2
            + 6 * c4
            + 7 * c5
            + 8 * c6
            + 9 * c7
            + 1 * c8
            + 2 * c9
            + 3 * c10
            + 4 * c11
        ) % 11
        if r1 % 10 != 0:
            return c12 == r1
        else:
            return (r2 == 10 and c12 == 0) or (c12 == r2)

    return legal_persons_style() or temporary_registered_taxpayers_style()


def validate_vat_lu(vat: str) -> bool:
    """Validates a VAT number against luxembourg VAT format specification.
    In Luxembourg is also named "Numéro d'identification à la taxe sur la
    valeur ajoutée" (No. TVA).
    The number must contain 8 digits and the last two digits are the check
    digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(LU)?(\d{8})$", vat)
    if not match:
        return False
    c1_c6 = int(match.group(2)[:6])
    c7_c8 = int(match.group(2)[6:])
    return c7_c8 == c1_c6 % 89


def validate_vat_lv(vat: str) -> bool:
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

    def style_1() -> bool:
        match = re.match(r"^(LV)?([4-9]\d{10})$", vat)
        if not match:
            return False
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = map(int, match.group(2))
        r = 3 - (
            (
                9 * c1
                + 1 * c2
                + 4 * c3
                + 8 * c4
                + 3 * c5
                + 10 * c6
                + 2 * c7
                + 5 * c8
                + 7 * c9
                + 6 * c10
            )
            % 11
        )
        return (r != -1) and (
            (r < -1 and c11 == r + 11) or (r > -1 and c11 == r)
        )

    def style_2() -> bool:
        match = re.match(r"^(LV)?32\d{9}", vat)
        return bool(match)

    def style_3() -> bool:
        match = re.match(r"^(LV)?(\d{2})(\d{2})(\d{2})[012](\d{4})$", vat)
        if not match:
            return False
        day, month, year = map(int, match.groups()[1:4])
        return day in range(0, 31) and month in range(0, 12)

    return style_1() or style_2() or style_3()


def validate_vat_mt(vat: str) -> bool:
    """Validates a VAT number against maltese VAT format specification.
    In Malta is also named "Vat reg. no." (VAT No.).
    The number must contain 8 digits and the last two digits are the check
    digits.
    It uses MOD 37 algorithm to calculate the check digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(MT)?(\d{8})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    c7_c8 = int("".join(map(str, [c7, c8])))
    r = 37 - (3 * c1 + 4 * c2 + 6 * c3 + 7 * c4 + 8 * c5 + 9 * c6) % 37
    return (r == 0 and c7_c8 == 37) or (c7_c8 == r)


def validate_vat_nl(vat: str) -> bool:
    """Validates a VAT number against netherlands VAT format specification.
    In Netherlands is also named "Btw-nummer" Btw-nr.).
    The number must contain 9 digits followed by the letter 'B' followed by 2
    digits.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(NL)?(\d{9})B(\d{2})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = map(int, match.group(2))
    c11, c12 = map(int, match.group(3))
    r = (
        9 * c1 + 8 * c2 + 7 * c3 + 6 * c4 + 5 * c5 + 4 * c6 + 3 * c7 + 2 * c8
    ) % 11
    return r != 10 and r == c9


def validate_vat_pl(vat: str) -> bool:
    """Validates a VAT number against polish VAT format specification.
    In Poland is also named "numer identyfikacji podatkowej" (NIP).
    The number must contain 10 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(PL)?(\d{10})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = map(int, match.group(2))
    r = (
        6 * c1
        + 5 * c2
        + 7 * c3
        + 2 * c4
        + 3 * c5
        + 4 * c6
        + 5 * c7
        + 6 * c8
        + 7 * c9
    ) % 11
    return r != 10 and r == c10


def validate_vat_pt(vat: str) -> bool:
    """Validates a VAT number against portuguese VAT format specification.
    In Portugal is also named "Número de Identificação Fiscal" (NIF).
    The number must contain 9 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://pt.wikipedia.org/wiki/Número_de_identificação_fiscal
    """

    def calc_check_digit(code: str) -> int:
        check_digit = sum((9 - i) * int(ch) for i, ch in enumerate(code))
        return (11 - check_digit) % 11 % 10

    sanitized_vat = re.sub(r"(^PT)|\s*|\W*", "", vat, flags=re.I)
    if not sanitized_vat.isdigit():
        return False
    if len(sanitized_vat) != 9:
        return False
    if sanitized_vat[0] == "0":
        return False
    return calc_check_digit(sanitized_vat[:-1]) == int(sanitized_vat[-1])


def validate_vat_ro(vat: str) -> bool:
    """Validates a VAT number against romanian VAT format specification.
    In Romania is also named "Codul de identificare fiscală" (CIF).
    The number must contain 2 to 10 digits and the last digit is the check
    digit. It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.

    .. seealso:: https://vatdesk.eu/en/romania/
    """

    def calc_check_digit(code: str) -> int:
        index = 10 - len(code)
        weights = [7, 5, 3, 2, 1, 7, 5, 3, 2][index:]
        check_digit = (
            10
            * sum(weight * int(ch) for weight, ch in zip(weights, code))
            % 11
        )
        return 0 if check_digit == 10 else check_digit

    sanitized_vat = re.sub(r"(^RO)|\s*|\W*", "", vat, flags=re.I)
    if len(sanitized_vat) not in range(2, 11):
        return False
    if not sanitized_vat.isdigit():
        return False
    return calc_check_digit(sanitized_vat) == int(sanitized_vat[-1])


def validate_vat_se(vat: str) -> bool:
    """Validates a VAT number against swedish VAT format specification.
    In Sweden is also named "momsregistreringsnummer" (Momsnr).
    The number must contain 12 digits.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(SE)?(\d{12})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12 = map(
        int, match.group(2)
    )
    s1 = int(c1 / 5) + (c1 * 2) % 10
    s3 = int(c3 / 5) + (c3 * 2) % 10
    s5 = int(c5 / 5) + (c5 * 2) % 10
    s7 = int(c7 / 5) + (c7 * 2) % 10
    s9 = int(c9 / 5) + (c9 * 2) % 10
    r = s1 + s3 + s5 + s7 + s9
    return c10 == (10 - (r + c2 + c4 + c6 + c8) % 10) % 10


def validate_vat_si(vat: str) -> bool:
    """Validates a VAT number against slovenian VAT format specification.
    In Slovenia is also named "Davčna številka" (ID za DDV).
    The number must contain 8 digits and the last digit is the check digit.
    It uses MOD 11 algorithm to calculate the check digit.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(SI)?(\d{8})$", vat)
    if not match:
        return False
    c1, c2, c3, c4, c5, c6, c7, c8 = map(int, match.group(2))
    r = 11 - (
        (c1 * 8 + c2 * 7 + c3 * 6 + c4 * 5 + c5 * 4 + c6 * 3 + c7 * 2) % 11
    )
    return (r != 11) and ((r == 10 and c8 == 0) or (c8 == r))


def validate_vat_sk(vat: str) -> bool:
    """Validates a VAT number against slovakian VAT format specification.
    In Slovakia is also named "Identifikačné číslo pre daň z pridanej hodnoty"
    (IČ DPH).
    The number must contain 10 digits and be divisible by 11.

    :param vat: VAT number to validate.
    :return: ``True`` if the given VAT is valid, ``False`` otherwise.
    """
    match = re.match(r"^(SK)?(\d{10})$", vat)
    if not match:
        return False
    return int(match.group(2)) % 11 == 0


#: Maps a country code to the respective country VAT rule
EU_RULES: Dict[str, Callable[[str], bool]] = {
    "AT": validate_vat_at,
    "BE": validate_vat_be,
    "BG": validate_vat_bg,
    "HR": validate_vat_hr,
    "CY": validate_vat_cy,
    "CZ": validate_vat_cz,
    "DE": validate_vat_de,
    "DK": validate_vat_dk,
    "EE": validate_vat_ee,
    "EL": validate_vat_el,
    "ES": validate_vat_es,
    "FI": validate_vat_fi,
    "FR": validate_vat_fr,
    "GB": validate_vat_gb,
    "HU": validate_vat_hu,
    "IE": validate_vat_ie,
    "IT": validate_vat_it,
    "LT": validate_vat_lt,
    "LU": validate_vat_lu,
    "LV": validate_vat_lv,
    "MT": validate_vat_mt,
    "NL": validate_vat_nl,
    "PL": validate_vat_pl,
    "PT": validate_vat_pt,
    "RO": validate_vat_ro,
    "SE": validate_vat_se,
    "SI": validate_vat_si,
    "SK": validate_vat_sk,
}

#: List of european union country codes
EU_COUNTRY_CODES: List[str] = list(EU_RULES.keys())
