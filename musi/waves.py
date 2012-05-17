from __future__ import absolute_import
from .base import C
from .math import Sub


class Ramp(object):
    def __init__(self, period_f):
        self.period_f = period_f
        self.v = 0.0
        self.last_now = 0.0
    def __call__(self, now):
        delta = now - self.last_now
        if delta <= 0:
            return self.v
        per = self.period_f(now)
        valdelta = delta / per
        self.v = (self.v + valdelta) % 1.0
        self.last_now = now
        return self.v


def Saw(period_f):
    return Sub(C(1.0), Ramp(period_f))


def Sine(period_f, offset_f=C(0.0)):
    import math
    twopi = 2.0 * math.pi
    def sine(now):
        period = period_f(now)
        offset = offset_f(now)
        pos = (((now % period) / period) + offset) % 1.0
        val = (math.sin(twopi * pos) * 0.5) + 0.5
        return val
    return sine


del C, Sub
