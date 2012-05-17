from simplecoremidi import MIDISource
from musi import C, Buffer, Tap, If, midi, math, waves, play


noteseq = [60, 64, 68, 70, 77]
song = midi.NoteSequencer(0, noteseq,
                          math.LinScale(C(0.1), C(1.0), waves.Sine(C(8.0))),
                          dur_f=C(0.1))

def emitter():
    source = MIDISource("sequence emitter")
    #countdown()
    def logsend(data):
        print data
        source.send(data)
    play(song, logsend)


if __name__=='__main__':
    emitter()
