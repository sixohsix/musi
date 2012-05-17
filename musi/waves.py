from __future__ import absolute_import


class Ramp(object):
    def __init__(self, period_f, offset_f=None, sync_f=None):
        from .base import C
        if sync_f is None:
            sync_f = C(0.0)
        if offset_f is None:
            offset_f = C(0.0)
        self.period_f = period_f
        self.offset_f = offset_f
        self.sync_f = sync_f
        self.v = 0.0
        self.last_now = 0.0
        self.cycled = False
    def __call__(self, now):
        delta = now - self.last_now
        if delta <= 0:
            return self.v
        per = self.period_f(now)
        sync = self.sync_f(now) != 0.0
        if per != 0 and not sync:
            valdelta = delta / per
            next_val = self.v + valdelta
        elif sync:
            next_val = 1.0
        else:
            next_val = self.v
        self.cycled = next_val >= 1.0
        self.v = next_val % 1.0
        self.last_now = now
        return (self.v + self.offset_f(now)) % 1.0


def Tick(period_f):
    ramp = Ramp(period_f)
    def tick(now):
        ramp(now)
        return ramp.cycled
    return tick


def Saw(period_f):
    from .base import C
    from .math import Sub
    return Sub(C(1.0), Ramp(period_f))


def Sine(period_f, offset_f=None, sync_f=None):
    import math
    twopi = 2.0 * math.pi
    ramp = Ramp(period_f, offset_f, sync_f)
    def sine(now):
        return 0.5 + (math.sin(twopi * ramp(now)) / 2.0)
    return sine


class Sequencer(object):
    def __init__(self, values, period_f, sync_f=None):
        self.values = values
        self.nvalues = len(values)
        self.ramp = Ramp(period_f, None, sync_f)
        self.lastpos = None
        self.changed = False
    def __call__(self, now):
        pos = int(self.ramp(now) * self.nvalues) % self.nvalues
        self.changed = self.ramp.cycled or pos != self.lastpos
        self.lastpos = pos
        return self.values[pos]
