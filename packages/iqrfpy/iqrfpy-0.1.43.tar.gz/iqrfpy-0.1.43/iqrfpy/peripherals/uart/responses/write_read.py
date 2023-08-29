"""UART Write Read response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import UartResponseCommands
from iqrfpy.enums.message_types import UartMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator


class WriteReadResponse(IResponseGetterMixin):
    """UART Write Read response class."""

    __slots__ = ('_read_data',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Write Read response constructor.

        Args:
            nadr (int): Device address.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            pdata (List[int], optional): DPA response data. Defaults to None.
            msgid (str, optional): Message ID. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.UART,
            pcmd=UartResponseCommands.WRITE_READ,
            m_type=UartMessages.WRITE_READ,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._read_data = result['readData'] if rcode == ResponseCodes.OK else None

    @property
    def read_data(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: Data read from RX buffer.

        Getter only.
        """
        return self._read_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'WriteReadResponse':
        """DPA response factory method.

        Parses DPA data and constructs :obj:`WriteReadResponse` object.

        Args:
            dpa (bytes): DPA response bytes.
        Returns:
            :obj:`WriteReadResponse`: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = None
        result = None
        if rcode == ResponseCodes.OK:
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'readData': pdata}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'WriteReadResponse':
        """JSON response factory method.

        Parses JSON API response and constructs :obj:`WriteReadResponse` object.

        Args:
            json (dict): JSON API response.
        Returns:
            :obj:`WriteReadResponse`: Response message object.
        """
        JsonValidator.response_received(json=json)
        nadr = Common.nadr_from_json(json=json)
        msgid = Common.msgid_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)
