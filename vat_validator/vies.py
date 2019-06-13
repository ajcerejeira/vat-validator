"""
This module allows interaction with VIES (VAT Information Exchange Service)
webservice. It can be used to validate VAT codes and fetch other information
from the entity with that VAT.

**Usage**:

>>> check_vat('PT', '502011378')
CheckVATResult(country_code='PT',
               vat='502011378',
               request_date=datetime.date(2019, 6, 6),
               valid=True,
               name='UNIVERSIDADE DO MINHO',
               address='LG DO PACO\\nBRAGA\\n4700-320 BRAGA')

.. seealso::

   VIES on the European Comission website:
   http://ec.europa.eu/taxation_customs/vies/

   The functions hereby described operate on this WSDL url:
   http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl
"""
from datetime import date
from typing import Optional

from zeep import Client
from zeep.cache import InMemoryCache
from zeep.transports import Transport

from .countries import EU_COUNTRY_CODES
from .utils import sanitize_vat


WSDL_URL = "http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"


class CheckVATResult:
    """Represents the result obtained by running the function
    :func:`check_vat`.

    :param country_code: IS0 3166 country code.
    :param vat: VAT number.
    :param request_date: date when this result was queried.
    :param valid: whether this VAT is valid or not.
    :param name: optional name of the entity associated with this VAT.
    :param address: optional address of the entity associated with this VAT.
    """

    def __init__(
        self,
        country_code: str,
        vat: str,
        request_date: date,
        valid: bool,
        name: Optional[str],
        address: Optional[str],
    ):
        self.country_code = country_code
        self.vat = vat
        self.request_date = request_date
        self.valid = valid
        self.name = name
        self.address = address

    def __eq__(self, other) -> bool:
        if not isinstance(other, CheckVATResult):
            return False
        return (
            self.country_code == other.country_code
            and self.vat == other.vat
            and self.request_date == other.request_date
            and self.valid == other.valid
            and self.name == other.name
            and self.address == other.address
        )

    def __str__(self) -> str:
        return "CheckVATResult(country_code='{}', vat='{}', request_date={}, "
        "valid={}, name={}, address={})".format(
            self.country_code,
            self.vat,
            self.request_date,
            self.valid,
            self.name,
            self.address,
        )


def check_vat(country_code: str, vat: str) -> CheckVATResult:
    """Checks if given VAT code is valid and (if possible) fetches the name
    and address of the entity with that code.

    :param country_code: valid IS0 3166 country code.
    :param vat: VAT number to check.
    :return: instance of :class:`CheckVATResult`.
    :raises ValueError: when the country code is invalid or the VAT is empty.
    """
    sanitized_vat = sanitize_vat(vat)
    if country_code not in EU_COUNTRY_CODES:
        raise ValueError("Invalid country code")
    if not sanitized_vat:
        raise ValueError("Empty VAT number")
    transport = Transport(cache=InMemoryCache())
    client = Client(WSDL_URL, transport=transport)
    result = client.service.checkVat(country_code, sanitized_vat)
    return CheckVATResult(
        country_code=result["countryCode"],
        vat=result["vatNumber"],
        request_date=result["requestDate"],
        valid=result["valid"],
        name=result["name"] if result["valid"] else None,
        address=result["address"] if result["valid"] else None,
    )
