from util import save_wav
import sound_recorder

WAVE_OUTPUT_FILENAME = "output.wav"


def main():
    sound_recorder.live_amplitude_spectrum()

    # data = sound_recorder.record(25)

    # save_wav(data, filename=WAVE_OUTPUT_FILENAME, channels=sound_recorder.CHANNELS)


if __name__ == '__main__':
    main()
