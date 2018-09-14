import wave
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from queue import Empty
from sound_recorder import SAMPLE_RATE, CHANNELS


def save_wav(sound_data, filename="output.wav", channels=2, sample_size=2, rate=44100):

    """
        Saves sound in wave file. File will be placed in program directory. If file exists it will be overwritten
    :param sound_data: sound data
    :param filename: file name
    :param channels: number sound channels
    :param sample_size: size of sound sample
    :param rate: sound sample rate
    """

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sample_size)
    wf.setframerate(rate)
    wf.writeframes(sound_data)
    wf.close()


def generate_sin_sound(seconds=1, amplitude=2, frequency=5000, rate=44100):
    """
        Generate harmonic sin sound

    :param seconds: sound length
    :param amplitude: sound amplitude
    :param frequency: sound frequency
    :param rate: sample rate
    :return: python list with generated data
    """

    def harmonic_value():
        return amplitude * math.sin(2 * math.pi * i * frequency / rate)

    generated_sound = []
    for i in range(int(rate * seconds)):
        generated_sound.append(harmonic_value())
    return generated_sound


def draw_plot(data, x=None):
    if x is None:
        x = range(len(data))

    plt.plot(x, data, 'r-')
    plt.show()


def amplitude_spectrum(sound_data):

    """
        Returns amplitude spectrum of single-channel sound
    :param sound_data: numpy Int16 array with two channel audio
    :return: amplitude spectrum
    """

    fourier = np.fft.rfft(sound_data)
    return np.abs(fourier) / len(fourier)


def live_spectrum_plot(data_queue, chunk, redraw_interval):

    """
        Creates live spectrum plot. Sound data gets from data_queue
    :param data_queue: queue with sound data for spectrum display
    :param chunk: size of sound
    :param redraw_interval: plot updating interval
    :return:
    """

    plot = plt.figure()
    amplitude_plot = plot.add_subplot(1, 1, 1)

    frequencies = np.fft.rfftfreq(chunk, 1. / SAMPLE_RATE)

    # selects function for retrieving spectrum, depends on number of audio channels
    spectrum_function = two_channel_audio_amplitude_spectrum if CHANNELS == 2 else amplitude_spectrum

    def refresh_amplitude_plot(amplitude_spectre):
        amplitude_plot.clear()
        amplitude_plot.set_ylim(0, 4000)
        amplitude_plot.plot(frequencies, amplitude_spectre, 'r-')

    def animate(frame):
        while True:
            try:
                amplitude_spectre = spectrum_function(data_queue.get_nowait())
                refresh_amplitude_plot(amplitude_spectre)
            except Empty:
                break

    plot_animation = animation.FuncAnimation(plot, animate, interval=redraw_interval)
    plt.show()


def two_channel_audio_amplitude_spectrum(sound_data):

    """
        Returns amplitude spectrum of two-channel sound
    :param sound_data: numpy Int16 matrix (must be two columns) with two channel audio
    :return: amplitude spectrum
    """

    # averaging sound from two channels
    averaged_sound = sound_data.mean(1, dtype='Int16')
    return amplitude_spectrum(averaged_sound)


