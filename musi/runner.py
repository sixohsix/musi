import sys

from simplecoremidi import MIDISource
from musi import play, countdown


try:
    input = __builtins__.raw_input
except AttributeError:
    pass


def main(args):
    if not args[1:]:
        print "Usage runner.py <song.py>"
        return 1

    mod = args[1]
    m = __import__(mod, globals(), locals(), ['x'])

    source = MIDISource("musi emitter")
    send_midi = source.send

    countdown()
    while True:
        m = reload(m)
        song = m.song
        print "Playing."
        try:
            play(song, send_midi)
        except KeyboardInterrupt:
            print "Interrupted. Hit enter."
            input()


if __name__=='__main__':
    sys.exit(main(sys.argv))
