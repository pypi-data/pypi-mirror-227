"""Sensor Read Sensors With Types response message."""

from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import SensorResponseCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes, ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator, JsonValidator
from iqrfpy.utils.sensor_parser import SensorParser, SensorData

__all__ = ['ReadSensorsWithTypesResponse']


class ReadSensorsWithTypesResponse(IResponseGetterMixin):
    """Sensor Read Sensors With Types response class."""

    __slots__ = ('_sensor_data',)

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        """Read Sensors With Types response constructor.

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
            pnum=Standards.SENSOR,
            pcmd=SensorResponseCommands.READ_SENSORS_WITH_TYPES,
            m_type=SensorMessages.READ_SENSORS_WITH_TYPES,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        self._sensor_data: List[SensorData] = result['sensors'] if rcode == ResponseCodes.OK else None

    @property
    def sensor_data(self) -> Optional[List[SensorData]]:
        """:obj:`list` of :obj:`SensorData` or :obj:`None`: Sensor data.

        Getter only.
        """
        return self._sensor_data

    @classmethod
    def from_dpa(cls, dpa: bytes) -> 'ReadSensorsWithTypesResponse':
        """DPA response factory method.

        Parses DPA data and constructs :obj:`ReadSensorsWithTypesResponse` object.

        Args:
            dpa (bytes): DPA response bytes.
        Returns:
            :obj:`ReadSensorsWithTypesResponse`: Response message object.
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
            result = {'sensors': SensorParser.read_sensors_with_types_from_dpa(pdata)}
        return cls(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @classmethod
    def from_json(cls, json: dict) -> 'ReadSensorsWithTypesResponse':
        """JSON response factory method.

        Parses JSON API response and constructs :obj:`ReadSensorsWithTypesResponse` object.

        Args:
            json (dict): JSON API response.
        Returns:
            :obj:`ReadSensorsWithTypesResponse`: Response message object.
        """
        JsonValidator.response_received(json=json)
        msgid = Common.msgid_from_json(json=json)
        nadr = Common.nadr_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        if rcode == ResponseCodes.OK:
            result = {'sensors': SensorParser.read_sensors_with_types_from_json(result['sensors'])}
        return cls(msgid=msgid, nadr=nadr, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata, result=result)
