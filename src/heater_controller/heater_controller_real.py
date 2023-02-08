import digitalio
from .heater_controller import HeaterController


class HeaterControllerReal(HeaterController):
    def __init__(self, heater_led_pin, heater_relay_pin):
        super().__init__()
        self.heater_led = digitalio.DigitalInOut(heater_led_pin)
        self.heater_led.direction = digitalio.Direction.OUTPUT
        self.heater_relay = digitalio.DigitalInOut(heater_relay_pin)
        self.heater_relay.direction = digitalio.Direction.OUTPUT

    def on(self, logger):
        if not self.heater_state:
            logger.info("Switching heater on")
            self.heater_led.value = True
            self.heater_relay.value = True
            super().on(logger)

    def off(self, logger):
        if self.heater_state:
            logger.info("Switching heater off")
            self.heater_led.value = False
            self.heater_relay.value = False
            super().off(logger)
