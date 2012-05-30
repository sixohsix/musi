from __future__ import print_function


LOOP_RATE_HZ = 200


def play(song_f, send_midi=None, loop_rate_hz=LOOP_RATE_HZ):
    from . import midi

    if not send_midi:
        from simplecoremidi import MIDISource
        source = MIDISource("musi emitter")
        send_midi = source.send

    song_f = midi.Output(send_midi, song_f)

    try:
        run(song_f, loop_rate_hz)
    except KeyboardInterrupt:
        send_midi(midi.all_notes_off())
        send_midi((0xfc,))
        raise


def run(song_f, loop_rate_hz=LOOP_RATE_HZ):
    from time import time, sleep
    loop_wait = 1.0 / loop_rate_hz
    start_time = time()
    song_time = 0.0
    loop_times = []
    while True:
        loop_start = time()
        song_f(song_time)
        loop_end = time()

        loop_times.append(loop_end - loop_start)
        while len(loop_times) > 7:
            loop_times.pop(0)
        avg_loop_time = sum(loop_times, 0.0) / len(loop_times)

        now = time() - start_time
        wait_time = -1.0
        while wait_time < 0.0:
            song_time = song_time + loop_wait
            wait_time = song_time - now - avg_loop_time
        sleep(wait_time)


def countdown():
    from time import sleep
    for i in range(4, 0, -1):
        print(i)
        sleep(1)
    print("go")
