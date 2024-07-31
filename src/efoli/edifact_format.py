"""
contains the EdifactFormat enum and helper methods
"""

import re

from .strenum import StrEnum

_PRUEFI_REGEX = r"^[1-9]\d{4}$"
pruefidentifikator_pattern = re.compile(_PRUEFI_REGEX)


# pylint: disable=too-few-public-methods
class EdifactFormat(StrEnum):
    """
    existing EDIFACT formats
    """

    APERAK = "APERAK"
    COMDIS = "COMDIS"  #: communication dispute
    CONTRL = "CONTRL"  #: control messages
    IFTSTA = "IFTSTA"  #: Multimodaler Statusbericht
    INSRPT = "INSRPT"  #: Prüfbericht
    INVOIC = "INVOIC"  #: invoice
    MSCONS = "MSCONS"  #: meter readings
    ORDCHG = "ORDCHG"  #: changing an order
    ORDERS = "ORDERS"  #: orders
    ORDRSP = "ORDRSP"  #: orders response
    PRICAT = "PRICAT"  #: price catalogue
    QUOTES = "QUOTES"  #: quotes
    REMADV = "REMADV"  #: zahlungsavis
    REQOTE = "REQOTE"  #: request quote
    PARTIN = "PARTIN"  #: market partner data
    UTILMD = "UTILMD"  #: utilities master data
    UTILMDG = "UTILMDG"  #: utilities master data for 'Gas'
    UTILMDS = "UTILMDS"  #: utilities master data for 'Strom'
    UTILMDW = "UTILMDW"  #: utilities master data 'Wasser'
    UTILTS = "UTILTS"  #: formula

    def __str__(self) -> str:
        return self.value


_edifact_mapping: dict[str, EdifactFormat] = {
    "99": EdifactFormat.APERAK,
    "29": EdifactFormat.COMDIS,
    "21": EdifactFormat.IFTSTA,
    "23": EdifactFormat.INSRPT,
    "31": EdifactFormat.INVOIC,
    "13": EdifactFormat.MSCONS,
    "39": EdifactFormat.ORDCHG,
    "17": EdifactFormat.ORDERS,
    "19": EdifactFormat.ORDRSP,
    "27": EdifactFormat.PRICAT,
    "15": EdifactFormat.QUOTES,
    "33": EdifactFormat.REMADV,
    "35": EdifactFormat.REQOTE,
    "37": EdifactFormat.PARTIN,
    "11": EdifactFormat.UTILMD,
    "25": EdifactFormat.UTILTS,
    "91": EdifactFormat.CONTRL,
    "92": EdifactFormat.APERAK,
    "44": EdifactFormat.UTILMD,  # UTILMD for GAS since FV2310
    "55": EdifactFormat.UTILMD,  # UTILMD for STROM since FV2310
}


def get_format_of_pruefidentifikator(pruefidentifikator: str) -> EdifactFormat:
    """
    returns the format corresponding to a given pruefi
    """
    if not pruefidentifikator:
        raise ValueError("The pruefidentifikator must not be falsy")
    if not pruefidentifikator_pattern.match(pruefidentifikator):
        raise ValueError(f"The pruefidentifikator '{pruefidentifikator}' is invalid.")
    try:
        return _edifact_mapping[pruefidentifikator[:2]]
    except KeyError as key_error:
        raise ValueError(f"No Edifact format was found for pruefidentifikator '{pruefidentifikator}'.") from key_error
