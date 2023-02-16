class ThermoboxController:
    def __init__(
        self,
        aht20_sensor,
        heater_controller,
        interface_controller,
        logger,
        target_temperature,
        temperature_wobble=0.1,
    ):
        self.aht20_sensor = aht20_sensor
        self.heater_controller = heater_controller
        self.interface_controller = interface_controller
        self.logger = logger
        self.target_temperature = target_temperature
        self.temperature_wobble = temperature_wobble
        self.temperature_range = [
            target_temperature,
            target_temperature + temperature_wobble,
        ]

        self.heater_controller.off(self.logger)

    def loop_step(self):
        self.interface_controller.update()

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
