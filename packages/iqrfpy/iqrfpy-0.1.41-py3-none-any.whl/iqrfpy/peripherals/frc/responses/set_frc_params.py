"""FRC Set FRC Params response message."""

from typing import Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.peripherals.frc.frc_params import FrcParams
from iqrfpy.enums.commands import FrcResponseCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes, ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['SetFrcParamsResponse']


class SetFrcParamsResponse(IResponseGetterMixin):
    """FRC Set FRC Params response class."""

    __slots__ = ('_frc_params',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        """Set FRC Params response constructor.

        Args:
            nadr (int): Device address.
            hwpid (int, optional): Hardware profile ID. Defaults to 65535, this value ignores HWPID check.
            rcode (int, optional): Response code. Defaults to 128.
            dpa_value (int, optional): DPA value. Defaults to 0.
            msgid (str, optional): Message ID. Defaults to None.
            result (dict, optional): JSON response data. Defaults to None.
        """
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.FRC,
            pcmd=FrcResponseCommands.SET_PARAMS,
            m_type=FrcMessages.SET_PARAMS,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )
        self._frc_params = None
        if rcode == ResponseCodes.OK:
            self._frc_params: FrcParams = FrcParams.from_int(result['frcResponseTime'])

    @property
    def frc_params(self) -> Optional[FrcParams]:
        """:obj:`FrcParams` or :obj:`None`: Previous FRC params.

        Getter only.
        """
        return self._frc_params

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'SetFrcParamsResponse':
        """DPA response factory method.

        Parses DPA data and constructs SetFrcParamsResponse object.

        Args:
            dpa (bytes): DPA response bytes.
        Returns:
            SetFrcParamsResponse: Response message object.
        """
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=9)
            result = {'frcResponseTime': dpa[8]}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'SetFrcParamsResponse':
        """JSON response factory method.

        Parses JSON API response and constructs SetFrcParamsResponse object.

        Args:
            json (dict): JSON API response.
        Returns:
            SetFrcParamsResponse: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid = Common.msgid_from_json(json=json)
        nadr = Common.nadr_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        return cls(msgid=msgid, nadr=nadr, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=result)
