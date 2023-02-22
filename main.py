import board  # type: ignore
import busio  # type: ignore
import adafruit_ahtx0  # type: ignore
from pmk import PMK  # type: ignore
from pmk.platform.rgbkeypadbase import RGBKeypadBase  # type: ignore

from src.heater_controller.heater_controller_real import HeaterControllerReal  # type: ignore
from src.thermobox_controller import ThermoboxController  # type: ignore
from src.interface_controller.interface_controller import InterfaceController  # type: ignore
from src.temperature_storage_controller.temperature_storage_controller_real import TemperatureStorageControllerReal  # type: ignore
from src.loggers import DebugLogger, InfoLogger  # type: ignore

keypad_hardware = RGBKeypadBase()
keypad = PMK(keypad_hardware)

# I2C1
SDA = board.GP10
SCL = board.GP11
i2c = busio.I2C(SCL, SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)


heater_controller = HeaterControllerReal(board.LED, board.GP28)
interface_controller = InterfaceController(keypad=keypad, logger=InfoLogger())
temperature_storage_controller = TemperatureStorageControllerReal(
    "/target_temperature.txt",
    "/fs_test.txt",
    logger=InfoLogger(),
)
thermobox_controller = ThermoboxController(
    aht20_sensor=sensor,
    heater_controller=heater_controller,
    interface_controller=interface_controller,
    temperature_storage_controller=temperature_storage_controller,
    logger=InfoLogger(),
    temperature_wobble=0.25,
)

thermobox_controller.run_forever()
