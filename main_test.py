class TestLogger:
    def debug(self, message):
        print("DEBUG:", message)

    def info(self, message):
        print("INFO:", message)


class TestSensor:
    def __init__(self, temperature=20.0, humidity=50):
        self.temperature = temperature
        self.humidity = humidity


from src.heater_controller.heater_controller import HeaterController
from src.thermobox_controller import ThermoboxController

thermobox_controller = ThermoboxController(
    aht20_sensor=TestSensor(temperature=20.0),
    heater_controller=HeaterController(),
    logger=TestLogger(),
    target_temperature=40.0,
    temperature_wobble=0.1,
)

thermobox_controller.loop_step()
