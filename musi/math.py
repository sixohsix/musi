from __future__ import absolute_import
import operator


def _Op(init_val, op_func):
    def Op(*val_fs):
        def op(now):
            val = init_val
            for val_f in val_fs:
                val = op_func(val, val_f(now))
            return val
        return op
    return Op


def _BinOp(op_func):
    def BinOp(left_f, right_f):
        def bin_op(now):
            left = left_f(now)
            right = right_f(now)
            return op_func(left, right)
        return bin_op
    return BinOp



Mul = _Op(1.0, operator.mul)
Add = _Op(0.0, operator.add)
def Sub(val_f0, val_f1):
    def sub(now):
        return val_f0(now) - val_f1(now)
    return sub


def LinScale(offset_f, range_f, f):
    return Add(offset_f, Mul(range_f, f))


def Random(seed=None):
    import random
    r = random.Random(seed)
    def rnd(now):
        return r.random()
    return rnd


LessThan = _BinOp(operator.lt)


def clamp(minv, rangev, val):
    return max(minv, min(minv + rangev, val))


def Clamp(min_f, range_f, val_f):
    def _clamp(now):
        return clamp(min_f(now), range_f(now), val_f(now))
    return _clamp


del operator
