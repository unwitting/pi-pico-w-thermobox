from .interface_controller import InterfaceController


class KeypadMock:
    class KeyMock:
        def __init__(self):
            pass

        def set_led(self, r, g, b):
            pass

        @property
        def pressed(self):
            return False

    def __init__(self):
        self.keys = [self.KeyMock() for _ in range(16)]

    def update(self):
        pass


class InterfaceControllerMocked(InterfaceController):
    def __init__(self, logger):
        super().__init__(keypad=KeypadMock(), logger=logger)
