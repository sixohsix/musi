from __future__ import absolute_import
from .base import C
from .math import Sub


class Ramp(object):
    def __init__(self, period_f, offset_f=C(0.0)):
        self.period_f = period_f
        self.offset_f = offset_f
        self.v = 0.0
        self.last_now = 0.0
    def __call__(self, now):
        delta = now - self.last_now
        if delta <= 0:
            return self.v
        per = self.period_f(now)
        if per != 0:
            valdelta = delta / per
            self.v = (self.v + valdelta) % 1.0
        self.last_now = now
        return (self.v + self.offset_f(now)) % 1.0


def Saw(period_f):
    return Sub(C(1.0), Ramp(period_f))


def Sine(period_f, offset_f=C(0.0)):
    import math
    twopi = 2.0 * math.pi
    ramp = Ramp(period_f, offset_f)
    def sine(now):
        return 0.5 + (math.sin(twopi * ramp(now)) / 2.0)
    return sine


def Sequencer(values, period_f):
    nvalues = len(values)
    ramp = Ramp(period_f)
    def sequence(now):
        pos = int(ramp(now) * nvalues) % nvalues
        return values[pos]
    return sequence


del C, Sub
