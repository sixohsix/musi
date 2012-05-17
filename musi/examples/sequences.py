from simplecoremidi import MIDISource, MIDIDestination
from musi import C, Buffer, Tap, If, Eval, Tempo, midi, math, waves, play, countdown


source = MIDISource("sequence emitter")
dest = MIDIDestination("sequence control")

midi_input = midi.Input(dest.recv)
tempo_control = math.LinScale(C(60.0), C(2.0), midi.ControllerValue(midi_input, 2, 1))
filter_control = midi.ControllerValue(midi_input, 2, 2)

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
bass = midi.Mix(
    Eval(waves.Sequencer(
            [midi.NoteSequencer(0, [48], beat_f),
             C(())],
            tempo.Duration(bars=1),
            )
         )
    )

filter_ = midi.ControllerChange(
    0, 52,
    math.LinScale(C(0.0), C(0.5), filter_control))

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
