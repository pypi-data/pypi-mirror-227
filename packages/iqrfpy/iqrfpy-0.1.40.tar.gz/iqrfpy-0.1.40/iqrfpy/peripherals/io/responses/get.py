"""IO Get response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import IOResponseCommands
from iqrfpy.enums.message_types import IOMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes, ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['GetResponse']


class GetResponse(IResponseGetterMixin):
    """IO Get response class."""

    __slots__ = ('_port_data',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Get response constructor.

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
            pnum=EmbedPeripherals.IO,
            pcmd=IOResponseCommands.GET,
            m_type=IOMessages.GET,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._port_data = result['ports'] if rcode == ResponseCodes.OK else None

    @property
    def port_data(self) -> Optional[List[int]]:
        """:obj:`list` of :obj:`int` or :obj:`None`: List of port data.

        Getter only.
        """
        return self._port_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'GetResponse':
        """DPA response factory method.

        Parses DPA data and constructs GetResponse object.

        Args:
            dpa (bytes): DPA response bytes.
        Returns:
            GetResponse: Response message object.
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
            result = {'ports': list(dpa[8:])}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'GetResponse':
        """JSON response factory method.

        Parses JSON API response and constructs GetResponse object.

        Args:
            json (dict): JSON API response.
        Returns:
            GetResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid = Common.msgid_from_json(json=json)
        nadr = Common.nadr_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        return cls(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)
