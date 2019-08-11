"""
This module allows interaction with VIES (VAT Information Exchange Service)
web service. It can be used to validate VAT codes and fetch other information
from the entity with that VAT.

**Usage**:


>>> check_vat('PT', '502011378')
CheckVATResult(country_code='PT',
               vat='502011378',
               request_date=2019-08-01 00:00:00+02:00,
               valid=True,
               name='UNIVERSIDADE DO MINHO',
               address='LG DO PACO\\nBRAGA\\n4700-320 BRAGA')

.. seealso::

   VIES on the European Comission website:
   http://ec.europa.eu/taxation_customs/vies/

   The functions hereby described operate on this WSDL url:
   http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl
"""
import xml.etree.ElementTree as ET
from datetime import date, datetime
from typing import Optional
from urllib import request

from vat_validator.countries import EU_COUNTRY_CODES
from vat_validator.sanitizers import sanitize_vat


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
        request_date: Optional[date],
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

    def __repr__(self) -> str:
        fields = ", ".join(
            "{}={}".format(attr, repr(value))
            for attr, value in vars(self).items()
        )
        return "CheckVATResult({})".format(fields)


def check_vat(country_code: str, vat: str) -> CheckVATResult:
    """Checks if given VAT code is valid and (if possible) fetches the name
    and address of the entity with that code.

    :param country_code: valid IS0 3166 country code.
    :param vat: VAT number to check.
    :return: instance of :class:`CheckVATResult`.
    :raises ValueError: when the country code is invalid or the VAT is empty.
    """
    if country_code not in EU_COUNTRY_CODES:
        raise ValueError("Invalid country code: '{}'".format(country_code))
    sanitized_vat = sanitize_vat(country_code, vat)

    # Prepare the SOAP request
    envelope = ET.Element(
        "soapenv:Envelope",
        attrib={
            "xmlns:hs": "urn:ec.europa.eu:taxud:vies:services:checkVat:types",
            "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        },
    )
    body = ET.SubElement(envelope, "soapenv:Body")
    action = ET.SubElement(body, "hs:checkVat")
    ET.SubElement(action, "hs:countryCode").text = country_code
    ET.SubElement(action, "hs:vatNumber").text = sanitized_vat
    payload = ET.tostring(envelope, encoding="utf-8")

    # Send the SOAP request to VIES Webservice
    url = "http://ec.europa.eu/taxation_customs/vies/services/checkVatService"
    req = request.Request(url, data=payload)
    res = request.urlopen(req)

    # Parse the result
    res_envelope = ET.fromstring(res.read())
    namespace = "urn:ec.europa.eu:taxud:vies:services:checkVat:types"
    request_date = res_envelope.find(".//{{{}}}requestDate".format(namespace))
    valid = res_envelope.find(".//{{{}}}valid".format(namespace))
    name = res_envelope.find(".//{{{}}}name".format(namespace))
    address = res_envelope.find(".//{{{}}}address".format(namespace))

    return CheckVATResult(
        country_code=country_code,
        vat=sanitized_vat,
        request_date=datetime.strptime(request_date.text, "%Y-%m-%d%z")
        if request_date is not None and request_date.text is not None
        else None,
        valid=valid is not None and valid.text == "true",
        name=name.text if name is not None else None,
        address=address.text if address is not None else None,
    )
