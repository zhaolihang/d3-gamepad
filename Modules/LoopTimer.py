from dataclasses import dataclass
from math import floor, isfinite
from time import perf_counter, sleep


@dataclass(frozen=True)
class TickContext:
    time: float
    dt: float
    raw_dt: float
    index: int


class LoopTimer:
    """Pace iterations against a monotonic clock without accumulating work time."""

    def __init__(self, interval, max_dt=0.1):
        if not isfinite(interval) or interval <= 0:
            raise ValueError("Loop interval must be finite and positive")
        if not isfinite(max_dt) or max_dt <= 0:
            raise ValueError("Maximum dt must be finite and positive")
        self.interval = interval
        self.max_dt = max_dt
        self.next_tick = perf_counter()
        self.last_tick = self.next_tick - interval
        self.index = 0

    def wait(self):
        remaining = self.next_tick - perf_counter()
        if remaining > 0:
            sleep(remaining)
        now = perf_counter()
        elapsed = max(0.0, now - self.last_tick)
        self.last_tick = now
        # Advance the original schedule; never anchor the next tick to a late wakeup.
        steps = max(1, floor((now - self.next_tick) / self.interval + 1e-7) + 1)
        self.next_tick += steps * self.interval
        self.index += 1
        return TickContext(now, min(elapsed, self.max_dt), elapsed, self.index)
