from __future__ import print_function
from types import FunctionType, ClassType

def Constant(val):
    def val_f(now):
        return val
    return val_f

C = Constant


class Buffer(object):
    def __init__(self):
        self.val = None
    def __call__(self, val):
        if val == self.val:
            return None
        self.val = val
        return val


def print_(name, val):
    print("{} {}".format(name, val))


def Tap(val_f, name="tap", func=print_):
    def tap(now):
        val = val_f(now)
        func(name, val)
        return val
    return tap


def If(test_f, true_f, false_f):
    def if_(now):
        # Note that we do NOT short-circuit
        test = test_f(now)
        true = true_f(now)
        false = false_f(now)
        return true if test > 0.0 else false
    return if_


def Eval(value_f):
    def eval_(now):
        return value_f(now)(now)
    return eval_


def song_time(now):
    return now


class Tempo(object):
    def __init__(self, bpm_f, bpb):
        def no_zero_bpm(now):
            bpm = bpm_f(now)
            return bpm if bpm != 0.0 else 0.00000001
        self.bpm_f = no_zero_bpm
        self.bpb = bpb

    def song_beats(self, now):
        return int(now / 60.0 * self.bpm_f(now))

    def song_bars(self, now):
        return self.song_beats(now) / self.bpb

    def Duration(self, bars=0, beats=0):
        nbeats = float((bars * self.bpb) + beats)
        def duration(now):
            return 1.0 / (self.bpm_f(now) / nbeats / 60.0)
        return duration
