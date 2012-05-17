from simplecoremidi import MIDISource
from musi import C, Buffer, Tap, If, Eval, Tempo, midi, math, waves, play, countdown


tempo = Tempo(C(120), 4)

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
bass = midi.Mix(
    Eval(waves.Sequencer(
            [midi.NoteSequencer(0, [48], beat_f),
             C(())],
            tempo.Duration(bars=1),
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
