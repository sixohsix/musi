def ControllerChange(ccid, val_f):
    from .base import Buffer
    b = Buffer()
    def cc(now):
        val = int(val_f(now))
        val = b(val)
        if val is not None:
            return ((now, (0xb0, ccid, val)),)
        return ()
    return cc


def Mix(*mfs):
    from itertools import chain
    def midi_mix(now):
        return chain(*[f(now) for f in mfs])
    return midi_mix


def RandomNotes(pitch_min_f, pitch_delta_f,
                velocity_min_f, velocity_delta_f,
                duration_min_f, duration_delta_f,
                random_f=None):
    from . import math
    if random_f is None:
        random_f = math.Random()
    pitch_f = math.LinScale(pitch_min_f, pitch_delta_f, random_f)
    velo_f = math.LinScale(velocity_min_f, velocity_delta_f, random_f)
    dur_f = math.LinScale(duration_min_f, duration_delta_f, random_f)
    def gen_random_notes(now):
        pitch = int(pitch_f(now))
        velo = int(127.0 * dur_f(now))
        dur = int(dur_f(now))
        return ((now, (0x90, pitch, velo)),
                (now + dur, (0x90, pitch, 0)))
    return gen_random_notes
