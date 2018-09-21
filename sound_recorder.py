import sounddevice as sd
from queue import Queue
import numpy as np
import util
import time

CHUNK = 2048

CHANNELS = 2

SAMPLE_RATE = 44100

DEFAULT_RECORD_SECONDS = 5

PLOT_REDRAW_INTERVAL = 1


def live_amplitude_spectrum():
    sound_data_queue = Queue()

    def record_callback(in_data, frames, time, status):
        sound_data_queue.put(in_data.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=CHUNK,
                        dtype="Int16", callback=record_callback):

        util.live_spectrum_plot(data_queue=sound_data_queue, chunk=CHUNK, redraw_interval=5)


def record(record_seconds=DEFAULT_RECORD_SECONDS):
    recorded_data = Queue()

    def record_callback(in_data, frames, time, status):
        recorded_data.put(in_data.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                        blocksize=CHUNK, dtype="Int16", callback=record_callback):

        while recorded_data.qsize() < (SAMPLE_RATE / CHUNK * record_seconds):
            time.sleep(20)            
            pass

    recorded_sound = np.array([recorded_data.get() for _ in range(recorded_data.qsize())])
    return recorded_sound
