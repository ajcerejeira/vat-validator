import re

from vat_validator.countries import EU_COUNTRY_CODES


def sanitize_vat_at(vat: str) -> str:
    return re.sub(r"(^AT)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_be(vat: str) -> str:
    return re.sub(r"(^BE)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_bg(vat: str) -> str:
    return re.sub(r"(^BG)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_cy(vat: str) -> str:
    return re.sub(r"(^CY)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_cz(vat: str) -> str:
    return re.sub(r"(^CZ)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_de(vat: str) -> str:
    return re.sub(r"(^DE)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_dk(vat: str) -> str:
    return re.sub(r"(^DK)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_ee(vat: str) -> str:
    return re.sub(r"(^EE)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_el(vat: str) -> str:
    return re.sub(r"(^EL)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_es(vat: str) -> str:
    return re.sub(r"(^ES)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_fi(vat: str) -> str:
    return re.sub(r"(^FI)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_fr(vat: str) -> str:
    return re.sub(r"(^FR)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_gb(vat: str) -> str:
    return re.sub(r"(^GB)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_hr(vat: str) -> str:
    return re.sub(r"(^HR)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_hu(vat: str) -> str:
    return re.sub(r"(^HU)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_ie(vat: str) -> str:
    return re.sub(r"(^IE)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_it(vat: str) -> str:
    return re.sub(r"(^IT)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_lt(vat: str) -> str:
    return re.sub(r"(^LT)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_lu(vat: str) -> str:
    return re.sub(r"(^LU)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_lv(vat: str) -> str:
    return re.sub(r"(^LV)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_mt(vat: str) -> str:
    return re.sub(r"(^MT)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_nl(vat: str) -> str:
    return re.sub(r"(^NL)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_pl(vat: str) -> str:
    return re.sub(r"(^PL)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_pt(vat: str) -> str:
    return re.sub(r"(^PT)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_ro(vat: str) -> str:
    return re.sub(r"(^RO)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_se(vat: str) -> str:
    return re.sub(r"(^SE)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_sl(vat: str) -> str:
    return re.sub(r"(^SL)|(\W*)", "", vat, flags=re.I)


def sanitize_vat_sk(vat: str) -> str:
    return re.sub(r"(^SK)|(\W*)", "", vat, flags=re.I)


def sanitize_vat(country_code: str, vat: str) -> str:
    if country_code not in EU_COUNTRY_CODES:
        raise ValueError("Invalid country code: '{}'".format(country_code))
    sanitizers = {
        "AT": sanitize_vat_at,
        "BE": sanitize_vat_be,
        "BG": sanitize_vat_bg,
        "CY": sanitize_vat_cy,
        "CZ": sanitize_vat_cz,
        "DE": sanitize_vat_de,
        "DK": sanitize_vat_dk,
        "EE": sanitize_vat_ee,
        "EL": sanitize_vat_el,
        "ES": sanitize_vat_es,
        "FI": sanitize_vat_fi,
        "FR": sanitize_vat_fr,
        "GB": sanitize_vat_gb,
        "HR": sanitize_vat_hr,
        "HU": sanitize_vat_hu,
        "IE": sanitize_vat_ie,
        "IT": sanitize_vat_it,
        "LT": sanitize_vat_lt,
        "LU": sanitize_vat_lu,
        "LV": sanitize_vat_lv,
        "MT": sanitize_vat_mt,
        "NL": sanitize_vat_nl,
        "PL": sanitize_vat_pl,
        "PT": sanitize_vat_pt,
        "RO": sanitize_vat_ro,
        "SE": sanitize_vat_se,
        "SL": sanitize_vat_sl,
        "SK": sanitize_vat_sk,
    }
    return sanitizers[country_code](vat)
