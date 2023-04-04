import numpy as np
import requests
import sounddevice as sd

from globals import RATE


def synthesize_speech(text):
    # Set the OpenTTS server URL and MaryTTS voice
    if len(text) > 2000:
        text = "I'm sorry, but it seems the answer is too long"
    elif len(text) < 3:
        text = "I'm sorry, there is nothing to say"

    print('Generating audio response...')

    # voice = "larynx:cmu_ljm-glow_tts"
    voice = "larynx:ljspeech-glow_tts"
    server_url = "http://localhost:5500/api/tts?vocoder=high&denoiserStrength=0.005&voice={}&text={}"\
        .format(voice, text.encode())
    response = requests.get(server_url)

    # Extract the audio data from the response
    buffer = response.content
    audio_data = np.frombuffer(buffer, dtype=np.int16)

    # Play audio
    print('Playing audio')
    sd.play(audio_data, samplerate=RATE/2, blocking=True)
