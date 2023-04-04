import textwrap

import pyaudio

# Set audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 100  # adjust this based on your microphone
RECORD_SECONDS = 30
MIN_RECORD_SECONDS = 3  # minimum recording time before detecting silence
WAVE_OUTPUT_FILENAME = "output.wav"


def wrap_text(txt, width=100):
    return '\n'.join(textwrap.wrap(txt, width=width))
