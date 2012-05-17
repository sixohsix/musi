import math
from functools import partial
from itertools import chain
from heapq import heappush, heappop
from time import time, sleep
import random

from simplecoremidi import MIDISource, MIDIDestination


LOOP_WAIT = 1.0 / 200  # 200 Hz


def all_notes_off():
    return tuple(chain(*((0x90, n, 0) for n in range(127))))


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


def LFO(period_f, offset_f=C(0.0)):
    twopi = 2.0 * math.pi
    def lfo(now):
        period = period_f(now)
        offset = offset_f(now)
        pos = (((now % period) / period) + offset) % 1.0
        val = (math.sin(twopi * pos) * 0.5) + 0.5
        return val
    return lfo


def Tap(val_f, name="tap "):
    def tap(now):
        val = val_f(now)
        print name + str(val)
        return val
    return tap


def MidiMix(*mfs):
    def midi_mix(now):
        return chain(*[f(now) for f in mfs])
    return midi_mix


def ControllerChange(ccid, val_f):
    b = Buffer()
    def cc(now):
        val = int(val_f(now))
        val = b(val)
        if val is not None:
            return ((now, (0xb0, ccid, val)),)
        return ()
    return cc


def FilterLFO():
    inner_lfo = LFO(C(7.0))
    ramp_per = Sub(C(3.0), Mul(C(2.9), inner_lfo))
    ramp = Ramp(ramp_per)
    return ControllerChange(
        52,
        LinScale(
            C(0), C(72),
            ramp
            )
        )



def _Op(init_val, op_func):
    def Op(*val_fs):
        def op(now):
            val = init_val
            for val_f in val_fs:
                val = op_func(val, val_f(now))
            return val
        return op
    return Op


Mul = _Op(1.0, lambda v0, v1: v0 * v1)
Add = _Op(0.0, lambda v0, v1: v0 + v1)
def Sub(val_f0, val_f1):
    def sub(now):
        return val_f0(now) - val_f1(now)
    return sub


def LinScale(offset_f, range_f, f):
    return Add(offset_f, Mul(range_f, f))


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


def Random(seed=None):
    r = random.Random(seed)
    def rnd(now):
        return r.random()
    return rnd


def Sometimes(probability_f, usual_f, sometimes_f, random_f=None):
    if random_f is None:
        random_f = Random()
    def sometimes(now):
        if random_f(now) < probability_f(now):
            return sometimes_f(now)
        return usual_f(now)
    return sometimes


def RandomMidiNotes(pitch_min_f, pitch_delta_f,
                    velocity_min_f, velocity_delta_f,
                    duration_min_f, duration_delta_f,
                    random_f):
    if random_f is None:
        random_f = Random()
    pitch_f = LinScale(pitch_min_f, pitch_delta_f, random_f)
    velo_f = LinScale(velocity_min_f, velocity_delta_f, random_f)
    dur_f = LinScale(duration_min_f, duration_delta_f, random_f)
    def gen_random_notes(now):
        pitch = int(pitch_f(now))
        velo = int(127.0 * dur_f(now))
        dur = int(dur_f(now))
        return ((now, (0x90, pitch, velo)),
                (now + dur, (0x90, pitch, 0)))
    return gen_random_notes


def maybe_gen_notes(now):
    probability = 0.006
    if random() < probability:
        return gen_random_notes(now)
    else:
        return ()

def heappush_all(heap, seq):
    for item in seq:
        heappush(heap, item)


def countdown():
    for i in range(4, 0, -1):
        print i
        sleep(1)

random_f = Random(1234)

song = MidiMix(
    FilterLFO(),
    Sometimes(
        Mul(C(0.1), LFO(C(30.0), C(0.25))),
        C(tuple()),
        RandomMidiNotes(C(24), C(48), C(0.5), C(0.5), C(0.1), C(1.0), random_f),
        random_f,
        )
    )


def emitter():
    source = MIDISource("random note emitter")

    frames = []

    start_time = time()
    song_time = 0.0

    countdown()

    try:
        while True:
            heappush_all(frames, song(song_time))
            while frames and (frames[0][0] < song_time):
                midi_out = heappop(frames)
                #print "emit {}".format(midi_out[1])
                source.send(midi_out[1])

            now = time() - start_time
            wait_time = -1
            while wait_time < 0:
                song_time = song_time + LOOP_WAIT
                wait_time = song_time - now
            sleep(wait_time)
    except KeyboardInterrupt:
        source.send(all_notes_off())

if __name__=='__main__':
    emitter()
