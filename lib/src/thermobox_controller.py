class ThermoboxController:
    def __init__(
        self,
        aht20_sensor,
        heater_controller,
        logger,
        target_temperature,
        temperature_wobble=0.1,
    ):
        self.aht20_sensor = aht20_sensor
        self.heater_controller = heater_controller
        self.logger = logger
        self.target_temperature = target_temperature
        self.temperature_wobble = temperature_wobble
        self.temperature_range = [
            target_temperature,
            target_temperature + temperature_wobble,
        ]

        self.heater_controller.off(self.logger)

    def loop_step(self):
        temperature = self.aht20_sensor.temperature
        self.logger.debug("Temperature: %0.3f C" % temperature)

        # humidity = sensor.relative_humidity
        # self.logger.debug("Humidity: %0.1f %%" % humidity)

        if temperature < self.target_temperature:
            self.heater_controller.on(self.logger)
        elif temperature > self.target_temperature + self.temperature_wobble:
            self.heater_controller.off(self.logger)

    def run_forever(self):
        while True:
            self.loop_step()
