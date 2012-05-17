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
