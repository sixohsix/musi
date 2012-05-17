from simplecoremidi import MIDISource, MIDIDestination
from musi import C, Buffer, Tap, If, Eval, Tempo, midi, math, waves, play, countdown

#
# Connect sequence emitter channel 1 to a synth (eg. Cheetah MS6)
# Connect sequence emitter channel 2 to a drum machine (eg. 606 preset in Live)
# Change tempo by modifying sequence control channel 2 control 1
# Change filter cutoff of a Cheetah MS6 by modifying sequence control channel
#     2 control 2 (outputs to sequence emitter channel 1 cc 52)
#


source = MIDISource("sequence emitter")
dest = MIDIDestination("sequence control")

midi_input = midi.Input(dest.recv)
tempo_control = math.LinScale(
    C(30.0), C(200.0),
    midi.UnitControllerValue(midi_input, 2, 1, 0.5))
filter_control = midi.UnitControllerValue(midi_input, 2, 2)

tempo = Tempo(tempo_control, 4)

beat_f = tempo.Duration(beats=1)
phrase_f = tempo.Duration(bars=4)

phrase_sync = waves.Tick(phrase_f)

noteseq = [60, 64, 68, 70, 77]
notes = midi.NoteSequencer(0, noteseq,
                           math.LinScale(C(0.1), C(1.0),
                                         waves.Sine(phrase_f)),
                           dur_f=C(0.1),
                           sync_f=phrase_sync)
drums = midi.Mix(
    midi.NoteSequencer(1, [36], beat_f),
    midi.NoteSequencer(1, [None, 38], beat_f),
    )

bassline = [48, 48, None, None] * 4 + [51, 51, None, None] * 4
bass = If(math.LessThan(C(8.0), tempo.song_bars),
          midi.NoteSequencer(0, bassline, beat_f),
          midi.nothing)

filter_ = midi.UnitControllerChange(
    0, 52,
    math.Mul(C(0.5), filter_control))

song = midi.Mix(
    notes,
    drums,
    bass,
    filter_,
    )


def emitter():
    def logsend(data):
        print data
        source.send(data)
    countdown()
    play(song, source.send)


if __name__=='__main__':
    emitter()
