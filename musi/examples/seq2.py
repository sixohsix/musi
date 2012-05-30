from simplecoremidi import MIDISource, MIDIDestination
from musi import C, Buffer, Tap, If, Eval, Tempo, midi, math, waves, play, countdown, util

#
## Connect sequence emitter channel 1 to a synth (eg. Cheetah MS6)
# Connect sequence emitter channel 2 to a drum machine (eg. 606 preset in Live)


midi.DEBUG = True

kick      = util.parse_seq("x... x... ..x. x...", x=36)
snare     = util.parse_seq(".... x... .... x..x", x=38)
hh_cl     = util.parse_seq("x... x... x... x...", x=42)
clap      = util.parse_seq("xxxx xxxx xxxx xxxx", x=39)

kick_add  = util.parse_seq(".... .... x... ..xx", x=36)
snare_add = util.parse_seq("..x. .... ..x. x...", x=38)
hh_cl_add = util.parse_seq(".... ..x. ..x. ..x.", x=42)


dest = MIDIDestination("sequence dest")

midi_input = midi.Input(dest.recv)

tempo_control = C(120.0)
filter_control = midi.UnitControllerValue(midi_input, 2, 2)

tempo = Tempo(tempo_control, 4)

quarter_f = tempo.Duration(beats=0.25)
beat_f = tempo.Duration(beats=1)
phrase_f = tempo.Duration(bars=4)

bar_sync = waves.Tick(tempo.Duration(bars=1))

warp_quarter_f = math.Mul(
    quarter_f,
    math.Add(waves.Sine(C(5.0)),
             math.Mul(waves.Saw(C(30.0)), C(0.5))
             ),
    C(2.0))

random_f = math.Random(9)

def sometimes_notes(seq, prob_f):
    return If(
        math.LessThan(random_f, prob_f),
        midi.NoteSequencer(1, seq, quarter_f),
        midi.nothing,
        )

drums = midi.Mix(
    midi.StartSend(),
    midi.ClockSend(beat_f),
    midi.NoteSequencer(1, kick, quarter_f),
    midi.NoteSequencer(1, snare, quarter_f),
    midi.NoteSequencer(1, hh_cl, quarter_f),
    midi.NoteSequencer(1, clap,
                       warp_quarter_f,
                       velo_f=math.Add(C(0.1), waves.Sine(C(4.0))),
                       sync_f=bar_sync),
    sometimes_notes(kick_add, C(0.5)),
    sometimes_notes(snare_add, C(0.5)),
    sometimes_notes(hh_cl_add, C(0.5)),
    )

song = midi.Mix(
    drums,
    )


def emitter():
    source = MIDISource("sequence emitter")
    def logsend(data):
        print data
        source.send(data)
    countdown()
    play(song, source.send)


if __name__=='__main__':
    emitter()
