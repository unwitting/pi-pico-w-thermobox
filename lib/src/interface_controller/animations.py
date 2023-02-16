class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (40, 40, 40)
    RED = (255, 0, 0)
    ORANGE = (255, 128, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


def linear_in_out(min, max, steps):
    if steps % 2 != 0:
        raise ValueError("Steps must be even")
    # Linearly ease from min to max and back again
    return [min + (max - min) * (2 * i / steps) for i in range(int(steps / 2))] + [
        max - (max - min) * (2 * i / steps) for i in range(int(steps / 2) + 1)
    ]


def linear_in_out_colors(c1, c2, steps):
    easing = linear_in_out(0, 1, steps)
    return [
        (
            int(c1[0] + (c2[0] - c1[0]) * easing_val),
            int(c1[1] + (c2[1] - c1[1]) * easing_val),
            int(c1[2] + (c2[2] - c1[2]) * easing_val),
        )
        for easing_val in easing
    ]


def LINEAR_IN_OUT_KEY_ANIMATION(
    key_code, duration, color1, color2, turn_off_others=True
):
    steps = 12
    step_wait = duration / (steps + 1)
    colors = linear_in_out_colors(color1, color2, steps)
    anim = [
        (
            "set_key",
            step_wait,
            {
                "key_code": key_code,
                "color": colors[0],
                "turn_off_others": turn_off_others,
            },
        ),
    ]
    for color in colors[1:]:
        anim.append(
            (
                "set_key",
                step_wait,
                {"key_code": key_code, "color": color, "turn_off_others": False},
            )
        )
    return anim


def PULSE_KEY_ANIMATION(key_code, duration, color, turn_off_others=True):
    return LINEAR_IN_OUT_KEY_ANIMATION(
        key_code, duration, Color.BLACK, color, turn_off_others
    )


def UPWARD_WIPE_ANIMATION(duration_s, lead_color, trailing_color):
    step_duration_s = duration_s / 5
    return [
        # Bottom row only
        (
            "set_row",
            step_duration_s,
            {"row": 3, "color": lead_color, "turn_off_others": True},
        ),
        # Second row and trailing bottom row
        (
            "set_row",
            None,
            {"row": 2, "color": lead_color, "turn_off_others": True},
        ),
        (
            "set_row",
            step_duration_s,
            {"row": 3, "color": trailing_color, "turn_off_others": False},
        ),
        # Third row and trailing second row
        (
            "set_row",
            None,
            {"row": 1, "color": lead_color, "turn_off_others": True},
        ),
        (
            "set_row",
            step_duration_s,
            {"row": 2, "color": trailing_color, "turn_off_others": False},
        ),
        # Fourth row and trailing third row
        (
            "set_row",
            None,
            {"row": 0, "color": lead_color, "turn_off_others": True},
        ),
        (
            "set_row",
            step_duration_s,
            {"row": 1, "color": trailing_color, "turn_off_others": False},
        ),
        # Trailing fourth row
        (
            "set_row",
            step_duration_s,
            {"row": 0, "color": trailing_color, "turn_off_others": True},
        ),
        # Off
        ("turn_all_keys_off", None, {}),
    ]


def DOWNWARD_WIPE_ANIMATION(duration_s, lead_color, trailing_color):
    step_duration_s = duration_s / 5
    return [
        # Top row only
        (
            "set_row",
            step_duration_s,
            {"row": 0, "color": lead_color, "turn_off_others": True},
        ),
        # Second row and trailing top row
        (
            "set_row",
            None,
            {"row": 1, "color": lead_color, "turn_off_others": True},
        ),
        (
            "set_row",
            step_duration_s,
            {"row": 0, "color": trailing_color, "turn_off_others": False},
        ),
        # Third row and trailing second row
        (
            "set_row",
            None,
            {"row": 2, "color": lead_color, "turn_off_others": True},
        ),
        (
            "set_row",
            step_duration_s,
            {"row": 1, "color": trailing_color, "turn_off_others": False},
        ),
        # Fourth row and trailing third row
        (
            "set_row",
            None,
            {"row": 3, "color": lead_color, "turn_off_others": True},
        ),
        (
            "set_row",
            step_duration_s,
            {"row": 2, "color": trailing_color, "turn_off_others": False},
        ),
        # Trailing fourth row
        (
            "set_row",
            step_duration_s,
            {"row": 3, "color": trailing_color, "turn_off_others": True},
        ),
        # Off
        ("turn_all_keys_off", None, {}),
    ]


BOOT_ANIMATION = [
    ("set_all_keys", 0.2, {"color": Color.WHITE}),
    ("turn_all_keys_off", 0.2, {}),
    ("set_all_keys", 0.2, {"color": Color.WHITE}),
    ("turn_all_keys_off", 0.2, {}),
    UPWARD_WIPE_ANIMATION(0.5, Color.RED, Color.WHITE),
    ("turn_all_keys_off", 0.2, {}),
    DOWNWARD_WIPE_ANIMATION(0.5, Color.BLUE, Color.WHITE),
    ("turn_all_keys_off", 0.2, {}),
]


def TEXT_ANIMATION(text, per_char_duration_s, color):
    display_chars = list(text.upper().replace(".", "F"))
    animation = [
        PULSE_KEY_ANIMATION(key, per_char_duration_s, color, turn_off_others=True)
        for key in display_chars
    ]
    return [animation, ("turn_all_keys_off", 0.2, {})]


def REPEAT_ANIMATION(animation, times, delay_s=None):
    return [[animation, ("wait", delay_s, {})] for _ in range(times)]
