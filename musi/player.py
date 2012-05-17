from __future__ import print_function


def play(song, send_midi=None, loop_rate_hz=200):
    from time import time, sleep
    from heapq import heappush, heappop
    from . import midi

    def heappush_all(heap, seq):
        for item in seq:
            heappush(heap, item)


    loop_wait = 1.0 / loop_rate_hz

    if not send_midi:
        from simplecoremidi import MIDISource
        source = MIDISource("musi emitter")
        send_midi = source.send_midi

    frames = []
    start_time = time()
    song_time = 0.0
    try:
        while True:
            heappush_all(frames, song(song_time))
            while frames and (frames[0][0] < song_time):
                midi_out = heappop(frames)
                send_midi(midi_out[1])

            now = time() - start_time
            wait_time = -1.0
            while wait_time < 0.0:
                song_time = song_time + loop_wait
                wait_time = song_time - now
            sleep(wait_time)
    except KeyboardInterrupt:
        send_midi(midi.all_notes_off())


def countdown():
    from time import sleep
    for i in range(4, 0, -1):
        print(i)
        sleep(1)
    print("go")
