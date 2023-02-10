import board  # type: ignore
import busio  # type: ignore
import adafruit_ahtx0  # type: ignore

from src.heater_controller.heater_controller_real import HeaterControllerReal
from src.thermobox_controller import ThermoboxController

SDA = board.GP0
SCL = board.GP1
i2c = busio.I2C(SCL, SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)


class Logger:
    def debug(self, message):
        print("DEBUG:", message)

    def info(self, message):
        print("INFO:", message)


heater_controller = HeaterControllerReal(board.LED, board.GP28)
thermobox_controller = ThermoboxController(
    aht20_sensor=sensor,
    heater_controller=heater_controller,
    logger=Logger(),
    target_temperature=26.0,
    temperature_wobble=0.25,
)

thermobox_controller.run_forever()
