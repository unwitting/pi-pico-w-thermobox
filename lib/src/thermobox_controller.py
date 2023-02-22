DEFAULT_TARGET_TEMPERATURE = 25.0


class ThermoboxController:
    def __init__(
        self,
        aht20_sensor,
        heater_controller,
        interface_controller,
        temperature_storage_controller,
        logger,
        temperature_wobble=0.1,
    ):
        self.aht20_sensor = aht20_sensor
        self.heater_controller = heater_controller
        self.interface_controller = interface_controller
        self.temperature_storage_controller = temperature_storage_controller
        self.logger = logger
        self.temperature_wobble = temperature_wobble
        self.heater_controller.off(self.logger)

        self._set_target_temperature(
            self.temperature_storage_controller.persisted_temperature()
            or DEFAULT_TARGET_TEMPERATURE
        )

    def _set_target_temperature(self, new_target_temperature):
        self.logger.info("New target temperature: %0.1fC" % new_target_temperature)
        self.target_temperature = new_target_temperature
        self.temperature_range = [
            self.target_temperature,
            self.target_temperature + self.temperature_wobble,
        ]
        self.interface_controller.set_display_target_temperature(
            "%.1f" % self.target_temperature
        )
        self.temperature_storage_controller.persist_temperature(self.target_temperature)

    def loop_step(self):
        self.interface_controller.update()

        # Does the interface want to tell us a new target temperature?
        new_target_temperature = self.interface_controller.target_temperature_input
        if new_target_temperature:
            self._set_target_temperature(float(new_target_temperature))
            self.interface_controller.target_temperature_input = ""

        temperature = self.aht20_sensor.temperature
        self.logger.debug("Temperature: %0.3f C" % temperature)

        self.interface_controller.set_display_temperature("%.1f" % temperature)

        if temperature < self.target_temperature:
            self.heater_controller.on(self.logger)
            self.interface_controller.set_display_heating(True)
        elif temperature > self.target_temperature + self.temperature_wobble:
            self.heater_controller.off(self.logger)
            self.interface_controller.set_display_heating(False)

    def run_forever(self):
        while True:
            self.loop_step()
