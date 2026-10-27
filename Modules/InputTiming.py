from math import hypot, isfinite


def positive_number(value, name):
    value = float(value)
    if not isfinite(value) or value <= 0:
        raise ValueError(name + " must be finite and positive")
    return value


def tick_interval(config):
    if "TICK_HZ" in config:
        return 1.0 / positive_number(config["TICK_HZ"], "TICK_HZ")
    # Older profiles may still name the same single frequency LOOP_HZ.
    if "LOOP_HZ" in config:
        return 1.0 / positive_number(config["LOOP_HZ"], "LOOP_HZ")
    return positive_number(config.get("DELAY_SECOND", 1 / 60), "DELAY_SECOND")


def cursor_settings(config):
    # Legacy profiles expressed the initial speed in pixels per 20 Hz tick.
    speed = positive_number(config.get("CURSOR_SPEED", config.get("CURSOR_MOVE_UNIT", 30) * 20), "CURSOR_SPEED")
    multiplier = positive_number(config.get("CURSOR_SLOW_MULTIPLIER", 0.5), "CURSOR_SLOW_MULTIPLIER")
    if multiplier > 1:
        raise ValueError("CURSOR_SLOW_MULTIPLIER must not exceed 1")
    button = config.get("CURSOR_SLOW_BUTTON", "")
    buttons = {"A", "B", "X", "Y", "BACK", "START", "DPAD_UP", "DPAD_DOWN",
               "DPAD_LEFT", "DPAD_RIGHT", "LEFT_SHOULDER", "RIGHT_SHOULDER",
               "LEFT_THUMB", "RIGHT_THUMB", "LEFT_TRIGER", "RIGHT_TRIGER"}
    if button not in buttons and button != "":
        raise ValueError("CURSOR_SLOW_BUTTON must be an XInput button/trigger name or an empty string")
    return speed, button, multiplier


class CursorMotion:
    """Move at a fixed speed in pixels/second, retaining fractional pixels."""

    def __init__(self, speed):
        self.speed = positive_number(speed, "CURSOR_SPEED")
        self.reset()

    def reset(self):
        self.remainder = [0.0, 0.0]

    def step(self, direction, dt, speed_multiplier=1.0):
        # dt is measured and clamped once by the application tick.
        length = hypot(*direction)
        if not length:
            return (0, 0)
        distance = self.speed * speed_multiplier * dt
        movement = []
        for axis, value in enumerate((direction[0], -direction[1])):
            self.remainder[axis] += value / length * distance
            whole_pixels = int(self.remainder[axis])
            self.remainder[axis] -= whole_pixels
            movement.append(whole_pixels)
        return tuple(movement)


class DirectionKeys:
    """Send key transitions once, rather than repeating key-down every frame."""

    def __init__(self, keyboard, mapping):
        self.keyboard = keyboard
        self.mapping = mapping
        self.held = set()

    def update(self, degree):
        if degree is None:
            wanted = set()
        elif degree < 10 or degree > 350:
            wanted = {"up"}
        elif degree < 80:
            wanted = {"up", "right"}
        elif degree < 100:
            wanted = {"right"}
        elif degree < 170:
            wanted = {"down", "right"}
        elif degree < 190:
            wanted = {"down"}
        elif degree < 260:
            wanted = {"down", "left"}
        elif degree < 280:
            wanted = {"left"}
        else:
            wanted = {"up", "left"}
        for name in sorted(self.held - wanted):
            self.keyboard.release(self.mapping[name])
        for name in sorted(wanted - self.held):
            self.keyboard.press(self.mapping[name])
        self.held = wanted
