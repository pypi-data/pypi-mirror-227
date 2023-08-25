from __future__ import annotations
import logging
import logging.config
from typing import Optional

from .base import mqtt, MQTTMessage
from .base import GuageInfo, Guage


class ThermometerInfo(GuageInfo):
    """Special information for Thermometer"""

    component: str = "sensor"
    name: str = "My Thermometer"
    object_id: Optional[str] = "my-thermometer"
    device_class: Optional[str] = "temperature"
    unique_id: Optional[str] = "my-thermometer"


class Thermometer(Guage):
    """Implements an MQTT thermometer:
    https://www.home-assistant.io/integrations/sensor.mqtt/
    """

    value_name: str = "temperature"

    def __init__(
        cls,
        mqtt: MQTT = None,
        name: str = "Thermometer",
        device_class="temperature",
    ):
        super(Thermometer, cls).__init__(
            mqtt=mqtt,
            name=name,
            device_class=device_class,
            info_class=ThermometerInfo,
            callback=Thermometer.command_callback,
        )

    @staticmethod
    def command_callback(client: Client, user_data, message: MQTTMessage):
        callback_payload = message.payload.decode()
        logging.info(f"Thermometer received {callback_payload} from HA")
