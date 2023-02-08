import board
import busio
import adafruit_ahtx0
import adafruit_logging as logging

from src.heater_controller.heater_controller_real import HeaterControllerReal
from src.thermobox_controller import ThermoboxController

SDA = board.GP0
SCL = board.GP1
i2c = busio.I2C(SCL, SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)

logger = logging.getLogger("pi-pico-w-thermobox")

heater_controller = HeaterControllerReal(board.LED, board.GP28)
thermobox_controller = ThermoboxController(
    aht20_sensor=sensor,
    heater_controller=heater_controller,
    logger=logger,
    target_temperature=40.0,
    temperature_wobble=0.1,
)

thermobox_controller.run_forever()
