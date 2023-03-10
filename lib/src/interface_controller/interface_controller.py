import time
from .animations import (
    Color,
    BOOT_ANIMATION,
    TEXT_ANIMATION,
    UPWARD_WIPE_ANIMATION,
    DOWNWARD_WIPE_ANIMATION,
    REPEAT_ANIMATION,
)


KEY_ORDER = [c for c in "C840D951EA62FB73"]
CYCLE_ORDER = [c for c in "0123456789ABCDEF"]


class Mode:
    TEMPERATURE_DISPLAY = "temperature-display"
    TARGET_TEMPERATURE_DISPLAY = "target-temperature-display"
    HEATING_OR_COOLING_DISPLAY = "heating-or-cooling-display"
    TARGET_TEMPERATURE_INPUT = "target-temperature-input"


DISPLAY_MODES_CYCLE_ORDER = [
    Mode.TEMPERATURE_DISPLAY,
    Mode.TARGET_TEMPERATURE_DISPLAY,
    Mode.HEATING_OR_COOLING_DISPLAY,
]

KEY_BEGIN_TEMPERATURE_INPUT = "C"
KEY_END_TEMPERATURE_INPUT = "D"


class Animator:
    def __init__(self, interface_controller, logger):
        self.interface_controller = interface_controller
        self.logger = logger
        self.queue = []
        self.now_playing = None

    def idle(self):
        return not self.queue and not self.now_playing

    def block(self):
        self.logger.debug("Animator blocking")
        while not self.idle():
            self.update()
        self.logger.debug("Animator block finished")

    def interrupt(self):
        self.logger.debug("Animator interrupting")
        self.queue = []
        self.now_playing = None

    # Item format is (action, duration_s, {args})
    def queue_animation(self, items):
        self.logger.debug("Queueing animation")
        for item in items:
            # If item is actually a list
            if isinstance(item, list):
                self.logger.debug("Animation item is sub-animation, queuing elements")
                # Queue the list as an animation
                self.queue_animation(item)
            else:
                self.logger.debug(f"Queuing animation item {item}")
                # Queue the item
                self.queue.append(item)

    def update(self):
        if self.now_playing:
            _, duration_s, _ = self.now_playing["item"]
            # Check if the item is done
            if time.monotonic() - self.now_playing["start_time"] >= duration_s:
                # It's finished, immediately start next one
                self._begin_playing_next_item()
            else:
                # It's not finished, do nothing
                pass
        else:
            # Nothing is playing, start the next item
            self._begin_playing_next_item()

    def _begin_playing_next_item(self):
        if self.queue:
            self.logger.debug(f"Animator playing next item in queue: {self.queue[0]}")
            item = self.queue.pop(0)
            _, duration_s, _ = item
            if duration_s:
                # This item has a duration, start it and record start time
                self.now_playing = {
                    "item": item,
                    "start_time": time.monotonic(),
                }
                self._perform_item_start_action(item)
            else:
                # Perform it immediately, and loop through the queue until we find one with a duration
                self._perform_item_start_action(item)
                self.logger.debug(
                    "Item had no duration, looping through to next queue item"
                )
                self._begin_playing_next_item()
        elif self.now_playing:
            # Nothing left in the queue, stop playing
            self.logger.debug("Animator queue is empty, stopping")
            self.now_playing = None
        else:
            pass

    def _perform_item_start_action(self, item):
        action, _, args = item
        ic = self.interface_controller
        mapping = {
            "set_all_keys": ic.set_all_keys,
            "turn_all_keys_off": ic.turn_all_keys_off,
            "set_key": ic.set_key_by_code,
            "set_row": ic.set_row,
            "set_column": ic.set_column,
            "wait": lambda: None,
        }
        mapping[action](**args)


class InterfaceController:
    def __init__(self, keypad, logger):
        self.keypad = keypad
        self.logger = logger
        self.animator = Animator(self, logger)
        self.mode = DISPLAY_MODES_CYCLE_ORDER[0]
        self.target_temperature_input = ""
        self.target_temperature_input_in_progress = ""
        self.target_temperature_input_reset_time = None

        self.display_temperature = None
        self.display_target_temperature = None
        self.display_heating = None

        self.logger.info("Initializing interface controller")

        # One-off update and boot animation
        self.update()
        self.animator.queue_animation(BOOT_ANIMATION)
        self.animator.block()

        self.logger.info("Interface controller initialized")

    def _get_key(self, key_code):
        return self.keypad.keys[KEY_ORDER.index(key_code)]

    def _get_pressed_key(self):
        for key_char in CYCLE_ORDER:
            key = self._get_key(key_char)
            if key.pressed:
                self.logger.debug(f"Key {key_char} is pressed")
                return key_char, key
        return None, None

    def set_display_temperature(self, temperature_str):
        self.display_temperature = temperature_str

    def set_display_target_temperature(self, temperature_str):
        self.display_target_temperature = temperature_str

    def set_display_heating(self, heating):
        self.display_heating = heating

    def update(self):
        self.keypad.update()
        self.animator.update()

        # Check for input
        pressed_code, pressed_key = self._get_pressed_key()
        if pressed_key:
            if (
                pressed_code == KEY_BEGIN_TEMPERATURE_INPUT
                and self.mode in DISPLAY_MODES_CYCLE_ORDER
            ):
                self.mode = Mode.TARGET_TEMPERATURE_INPUT
                self.target_temperature_input_in_progress = ""
                self.animator.interrupt()
                self.turn_all_keys_off()
                self.set_key_by_code(
                    KEY_END_TEMPERATURE_INPUT, Color.ORANGE, turn_off_others=False
                )
                self.target_temperature_input_reset_time = time.monotonic() + 10

        # Are we in an input mode?
        if self.mode == Mode.TARGET_TEMPERATURE_INPUT:
            pressed_code, pressed_key = self._get_pressed_key()
            # Handle temp input
            if pressed_key:
                if pressed_code in "0123456789F":
                    self.target_temperature_input_in_progress += (
                        pressed_code
                        if pressed_code in "0123456789"
                        else "."
                        if pressed_code == "F"
                        else ""
                    )
                    self.target_temperature_input_reset_time = time.monotonic() + 10
                    self.logger.info(
                        f"Target temperature input: {self.target_temperature_input_in_progress}"
                    )
                    ## TODO WERE HERE
                    self.animator.queue_animation(
                        [
                            (
                                "set_key",
                                0.3,
                                {
                                    "key_code": pressed_code,
                                    "color": Color.BLUE,
                                    "turn_off_others": False,
                                },
                            )
                        ]
                    )
                    self.animator.block()
                    self.set_key_by_code(
                        pressed_code, Color.GREY, turn_off_others=False
                    )

                # Handle commit of temperature
                if pressed_code == KEY_END_TEMPERATURE_INPUT:
                    self.logger.debug(
                        f"Committing target temperature input: {self.target_temperature_input}"
                    )
                    self.target_temperature_input = (
                        self.target_temperature_input_in_progress
                    )
                    self.target_temperature_input_reset_time = None
                    self.mode = Mode.TARGET_TEMPERATURE_DISPLAY
                    self.animator.interrupt()
                    self.animator.queue_animation(
                        [
                            (
                                "set_key",
                                0.8,
                                {
                                    "key_code": KEY_END_TEMPERATURE_INPUT,
                                    "color": Color.GREEN,
                                },
                            ),
                            ("turn_all_keys_off", None, {}),
                        ]
                    )
                    return

            # Have we run out of time?
            if time.monotonic() > self.target_temperature_input_reset_time:
                self.logger.debug("Target temperature input timed out")
                self.mode = Mode.TEMPERATURE_DISPLAY
                self.target_temperature_input = ""
            return

        # Only reach here once we're back in a display mode

        # In normal operation, if there's nothing else going on then display
        # whatever's needed for the current mode, and cycle the mode
        if self.animator.idle():
            self.logger.debug(f"Interface controller idle, displaying mode {self.mode}")
            if self.mode == Mode.TEMPERATURE_DISPLAY and self.display_temperature:
                self.display_text(self.display_temperature)

            elif (
                self.mode == Mode.TARGET_TEMPERATURE_DISPLAY
                and self.display_target_temperature
            ):
                self.display_text(self.display_target_temperature, color=Color.ORANGE)

            elif (
                self.mode == Mode.HEATING_OR_COOLING_DISPLAY
                and self.display_heating is not None
            ):
                if self.display_heating:
                    self.animator.queue_animation(
                        REPEAT_ANIMATION(
                            UPWARD_WIPE_ANIMATION(0.5, Color.RED, Color.ORANGE), 3, 0.2
                        )
                    )
                else:
                    self.animator.queue_animation(
                        REPEAT_ANIMATION(
                            DOWNWARD_WIPE_ANIMATION(0.5, Color.BLUE, Color.GREY), 3, 0.2
                        )
                    )

            # Did we do anything? Look at the animator queue and see if it's now doing something
            if not self.animator.idle():
                self.animator.queue_animation([("wait", 5, {})])

            self.mode = DISPLAY_MODES_CYCLE_ORDER[
                (DISPLAY_MODES_CYCLE_ORDER.index(self.mode) + 1)
                % len(DISPLAY_MODES_CYCLE_ORDER)
            ]
            self.logger.debug(f"Interface controller mode cycled to {self.mode}")

    def display_text(self, text, color=Color.WHITE, block=False):
        self.logger.info(f"Displaying text: {text}")
        self.animator.queue_animation(TEXT_ANIMATION(text, 0.75, color=color))
        if block:
            self.animator.block()

    def set_all_keys(self, color):
        for key in self.keypad.keys:
            key.set_led(*color)

    def turn_all_keys_off(self):
        self.set_all_keys((0, 0, 0))

    def set_key_by_code(self, key_code, color, turn_off_others=True):
        if turn_off_others:
            self.turn_all_keys_off()
        self._get_key(key_code).set_led(*color)

    # Set all keys in a row, 0-indexed from top to bottom
    def set_row(self, row, color, turn_off_others=True):
        if turn_off_others:
            self.turn_all_keys_off()
        for i in range(4):
            self.set_key_by_code(
                CYCLE_ORDER[(row * 4) + i], color, turn_off_others=False
            )

    # Set all keys in a column, 0-indexed from left to right
    def set_column(self, column, color, turn_off_others=True):
        if turn_off_others:
            self.turn_all_keys_off()
        for i in range(4):
            self.set_key_by_code(
                CYCLE_ORDER[(i * 4) + column], color, turn_off_others=False
            )
