from simplecoremidi import MIDISource
from musi import C, Buffer, Tap, If, Eval, midi, math, waves, play, countdown


class Notes:
    quarter = 0.25


def bpm(b):
    return 60.0 / b

beat = bpm(120)

phrase_sync = waves.Tick(C(beat * 16.0))

noteseq = [60, 64, 68, 70, 77]
notes = midi.NoteSequencer(0, noteseq,
                           math.LinScale(C(0.1), C(1.0),
                                         waves.Sine(C(beat * 16.0))),
                           dur_f=C(0.1),
                           sync_f=phrase_sync)
drums = midi.Mix(
    midi.NoteSequencer(1, [36], C(beat)),
    midi.NoteSequencer(1, [None, 38], C(beat)),
    )
bass = midi.Mix(
    Eval(waves.Sequencer(
            [midi.NoteSequencer(0, [48], C(beat)),
             C(())],
            C(beat * 4)
            )
         )
    )

song = midi.Mix(notes, drums, bass)


def emitter():
    source = MIDISource("sequence emitter")
    def logsend(data):
        print data
        source.send(data)
    countdown()
    play(song, source.send)


if __name__=='__main__':
    emitter()
