import board  # type: ignore
import busio  # type: ignore
import adafruit_ahtx0  # type: ignore
from pmk import PMK  # type: ignore
from pmk.platform.rgbkeypadbase import RGBKeypadBase  # type: ignore

from src.heater_controller.heater_controller_real import HeaterControllerReal  # type: ignore
from src.thermobox_controller import ThermoboxController  # type: ignore
from src.interface_controller.interface_controller import InterfaceController  # type: ignore
from src.loggers import DebugLogger, InfoLogger  # type: ignore

keypad_hardware = RGBKeypadBase()
keypad = PMK(keypad_hardware)
## I2C0
# SDA = board.GP0
# SCL = board.GP1
# i2c = busio.I2C(SCL, SDA)
# sensor = adafruit_ahtx0.AHTx0(i2c)

# I2C1
SDA = board.GP10
SCL = board.GP11
i2c = busio.I2C(SCL, SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)

# sensor = adafruit_ahtx0.AHTx0(keypad_hardware.i2c())


heater_controller = HeaterControllerReal(board.LED, board.GP28)
interface_controller = InterfaceController(keypad=keypad, logger=DebugLogger())
thermobox_controller = ThermoboxController(
    aht20_sensor=sensor,
    heater_controller=heater_controller,
    interface_controller=interface_controller,
    logger=InfoLogger(),
    target_temperature=25.0,
    temperature_wobble=0.25,
)

thermobox_controller.run_forever()
