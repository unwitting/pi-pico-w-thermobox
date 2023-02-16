class TestSensor:
    def __init__(self, temperature=20.0, humidity=50):
        self.temperature = temperature
        self.humidity = humidity


from lib.src.loggers import NoLogger, DebugLogger, InfoLogger
from lib.src.heater_controller.heater_controller import HeaterController
from lib.src.thermobox_controller import ThermoboxController
from lib.src.interface_controller.interface_controller_mocked import (
    InterfaceControllerMocked,
)

thermobox_controller = ThermoboxController(
    aht20_sensor=TestSensor(temperature=20.0),
    heater_controller=HeaterController(),
    interface_controller=InterfaceControllerMocked(logger=DebugLogger()),
    logger=NoLogger(),
    target_temperature=40.0,
    temperature_wobble=0.1,
)

thermobox_controller.run_forever()
