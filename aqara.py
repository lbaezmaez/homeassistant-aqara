import logging

DOMAIN = 'Aqara'

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['https://github.com/fooxy/homeassisitant-pyAqara/archive/v0.3-alpha.zip#pyAqara==0.3']


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup the sensor platform."""
    from pyAqara.sensor import Sensor, HTSensorData, MagnetData, MotionData
    from pyAqara.gateway import AqaraGateway
    # get the gateway and init it's ip / port via whoami
    gateway = AqaraGateway()
    gateway.initGateway()

    # get all sensors and format them for HASS
    sensorItems = []
    dynamicDevices = gateway.get_devicesList()
    for device in dynamicDevices:
        deviceResponse = gateway.get_read(device)
        model = deviceResponse['model']
        sid = deviceResponse['sid']
        # TODO: find a way to get the configured name from the gateway
        if model == 'sensor_ht':
            temperatureSensorData = HTSensorData(gateway)
            sensorItems.append(
                Sensor(temperatureSensorData, sid, sid, 'temperature'))
            humiditySensorData = HTSensorData(gateway)
            sensorItems.append(
                Sensor(humiditySensorData, sid, sid, 'humidity'))
        elif model == 'magnet':
            sensorData = MagnetData(gateway)
            sensorItems.append(Sensor(sensorData, sid, sid, 'magnet'))
        # elif model == 'switch':
            # TODO: figure out how switches work
            # sensorData = SwitchData(gateway)
            # sensorItems.append(Sensor(sensorData, sid, sid, 'switch'))
        elif model == 'motion':
            sensorData = MotionData(gateway)
            sensorItems.append(Sensor(sensorData, sid, sid, 'motion'))
        # TODO: implement support for other sensors
        # elif model ==
        # 'plug/ctrl_neutral1/ctrl_neutral2/gateway'

    add_devices_callback(sensorItems)
    return True