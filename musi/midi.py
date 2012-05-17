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


def Mix(*mfs):
    from itertools import chain
    def midi_mix(now):
        return chain(*[f(now) for f in mfs])
    return midi_mix


def RandomNotes(channel,
                pitch_min_f, pitch_delta_f,
                velocity_min_f, velocity_delta_f,
                duration_min_f, duration_delta_f,
                random_f=None):
    from . import math
    channel = math.clamp(0, 15, int(channel))
    action = 0x90 | channel
    if random_f is None:
        random_f = math.Random()
    pitch_f = math.LinScale(pitch_min_f, pitch_delta_f, random_f)
    velo_f = math.LinScale(velocity_min_f, velocity_delta_f, random_f)
    dur_f = math.LinScale(duration_min_f, duration_delta_f, random_f)
    def gen_random_notes(now):
        pitch = math.clamp(0, 127, int(pitch_f(now)))
        velo = math.clamp(0, 127, int(127.0 * velo_f(now)))
        dur = math.clamp(0, 1000000, dur_f(now))  # Notes longer than one million seconds are not supported. Sorry!
        return ((now, (action, pitch, velo)),
                (now + dur, (action, pitch, 0)))
    return gen_random_notes
