from .base import C

nothing = C(())

def mclamp(val):
    from .math import clamp
    return clamp(0, 127, int(val))


def all_notes_off(now=None):
    from itertools import chain
    return tuple(chain(*((0x90, n, 0) for n in range(127))))


def ControllerChange(channel, ccid, val_f):
    from .base import Buffer
    from . import math
    b = Buffer()
    action = 0xb0 | math.clamp(0, 15, int(channel))
    def cc(now):
        val = int(val_f(now))
        val = b(val)
        if val is not None:
            return ((now, (action, ccid, val)),)
        return ()
    return cc


def UnitControllerChange(channel, ccid, val_f):
    from . import math, C
    return ControllerChange(
        channel, ccid,
        math.Mul(C(127.0), val_f))


def Mix(*mfs):
    from itertools import chain
    def midi_mix(now):
        return chain(*[f(now) for f in mfs])
    return midi_mix


def note(channel, pitch, velo, dur, now):
    from . import math
    channel = math.clamp(0, 15, int(channel))
    action = 0x90 | channel
    pitch = mclamp(int(pitch))
    velo = mclamp(int(velo))
    dur = math.clamp(0, 1000000, dur)  # Notes longer than one million seconds are not supported. Sorry!
    return ((now, (action, pitch, velo)),
            (now + dur, (action, pitch, 0)))


def Note(channel, pitch_f, velo_f=None, dur_f=None):
    from .base import C
    if velo_f is None:
        velo_f = C(1.0)
    if dur_f is None:
        dur_f = C(0.1)
    def gen_note(now):
        pitch = pitch_f(now)
        velo = 127 * velo_f(now)
        dur = dur_f(now)
        if pitch is not None:
            return note(channel, pitch, velo, dur, now)
        else:
            return ()
    return gen_note


def NoteSequencer(channel, note_values, note_rate_f, velo_f=None, dur_f=None, sync_f=None):
    from . import base, math, waves
    period_f = math.Mul(base.C(len(note_values)), note_rate_f)
    seq_f = waves.Sequencer(note_values, period_f, sync_f)
    note_f = Note(channel, seq_f, velo_f, dur_f)
    def note_sequencer(now):
        note = note_f(now)
        if seq_f.changed:
            return note
        return ()
    return note_sequencer


def RandomNotes(channel,
                pitch_min_f, pitch_delta_f,
                velocity_min_f, velocity_delta_f,
                duration_min_f, duration_delta_f,
                random_f=None):
    from . import math
    if random_f is None:
        random_f = math.Random()
    pitch_f = math.LinScale(pitch_min_f, pitch_delta_f, random_f)
    velo_f = math.LinScale(velocity_min_f, velocity_delta_f, random_f)
    dur_f = math.LinScale(duration_min_f, duration_delta_f, random_f)
    return Note(channel, pitch_f, velo_f, dur_f)



class Input(object):
    def __init__(self, recv_midi):
        self.recv_midi = recv_midi
        self.last_read_time = None
        self.midi_buf = ()
    def __call__(self, now):
        if now > self.last_read_time:
            self.midi_buf = self.recv_midi()
            self.last_read_time = now
        return self.midi_buf


class ControllerValue(object):
    def __init__(self, midi_input, channel, ccid, initial_val=0):
        from .math import clamp
        self.action = 0xb0 | clamp(0, 15, int(channel))
        self.ccid = ccid
        self.midi_input = midi_input
        self.ccval = mclamp(initial_val)
    def __call__(self, now):
        inp = self.midi_input(now)
        for i, byte in enumerate(inp):
            if (byte == self.action
                and len(inp) - i > 2
                and inp[i+1] == self.ccid):
                self.ccval = inp[i+2]
        return self.ccval


def UnitControllerValue(midi_input, channel, ccid, initial_val=0.0):
    from . import math, C
    return math.Mul(
        C(1.0 / 127),
        ControllerValue(midi_input, channel, ccid, initial_val * 127.0))


del C
