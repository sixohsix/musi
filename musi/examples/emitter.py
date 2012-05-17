from time import sleep
from simplecoremidi import MIDISource
from musi import C, Buffer, Tap, If, midi, math, waves, play, countdown


def FilterLFO():
    inner_lfo = waves.Sine(C(7.0))
    ramp_per = math.Sub(C(3.0), math.Mul(C(2.9), inner_lfo))
    ramp = waves.Ramp(ramp_per)
    return midi.ControllerChange(
        0, 52,
        math.LinScale(
            C(0), C(72),
            ramp
            )
        )


def Sometimes(probability_f, usual_f, sometimes_f, random_f):
    return If(math.LessThan(random_f, probability_f), sometimes_f, usual_f)


random_f = math.Random(666)
song = midi.Mix(
    FilterLFO(),
    Sometimes(
        math.LinScale(C(0.01), C(0.05), waves.Sine(C(30.0), C(0.25))),
        C(tuple()),
        midi.RandomNotes(0,
                         C(24), C(48),
                         C(0.5), C(0.5),
                         C(0.1), C(0.2),
                         random_f),
        random_f,
        )
    )


def emitter():
    source = MIDISource("random note emitter")
    countdown()
    play(song, source.send)


if __name__=='__main__':
    emitter()
