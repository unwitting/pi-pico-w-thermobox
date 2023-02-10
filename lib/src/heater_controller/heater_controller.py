class HeaterController:
    def __init__(self):
        self.heater_state = False

    def on(self, logger):
        self.heater_state = True

    def off(self, logger):
        self.heater_state = False
