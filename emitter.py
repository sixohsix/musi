import math
from functools import partial
from itertools import chain
from heapq import heappush, heappop
from time import time, sleep
import random

from simplecoremidi import MIDISource, MIDIDestination
from musi import C, Buffer, Tap, If, midi, math, waves

LOOP_WAIT = 1.0 / 200  # 200 Hz


def all_notes_off():
    return tuple(chain(*((0x90, n, 0) for n in range(127))))


def FilterLFO():
    inner_lfo = waves.Sine(C(7.0))
    ramp_per = math.Sub(C(3.0), math.Mul(C(2.9), inner_lfo))
    ramp = waves.Ramp(ramp_per)
    return midi.ControllerChange(
        52,
        math.LinScale(
            C(0), C(72),
            ramp
            )
        )


def Sometimes(probability_f, usual_f, sometimes_f, random_f=None):
    if random_f is None:
        random_f = math.Random()
    return If(math.LessThan(random_f, probability_f), usual_f, sometimes_f)


def heappush_all(heap, seq):
    for item in seq:
        heappush(heap, item)


def countdown():
    for i in range(4, 0, -1):
        print i
        sleep(1)

random_f = math.Random(1234)

song = midi.Mix(
    FilterLFO(),
    Sometimes(
        math.Mul(C(0.1), waves.Sine(C(30.0), C(0.25))),
        C(tuple()),
        midi.RandomNotes(C(24), C(48), C(0.5), C(0.5), C(0.1), C(1.0), random_f),
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
