import pyaudio
import threading

from pynput import keyboard

from audio import record_audio
from gpt import transcript_audio, get_answer
from keyboard import wait_for_key, listen_for_keys
from tts import synthesize_speech


def initialize():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Determine default input device index
    default_device_index = audio.get_default_input_device_info()["index"]

    # Print available input devices
    # print("Available input devices:")
    # for i in range(audio.get_device_count()):
    #   device_info = audio.get_device_info_by_index(i)
    #   print(f"  {i}: {device_info['name']}")

    # Select input device
    device_index = default_device_index  # int(input(f"Select input device [default {default_device_index}]: ") or default_device_index)
    device_info = audio.get_device_info_by_index(device_index)
    print(f"Using input device: {device_info['name']}")

    # start the keypress listener in a separate thread
    keypress_thread = threading.Thread(target=listen_for_keys)
    keypress_thread.daemon = True
    keypress_thread.start()
    return audio, device_index


def finalize(audio):
    audio.terminate()


def main():
    audio, device_index = initialize()
    while True:
        print("Press SPACE to continue or ESC to terminate...")
        key = wait_for_key()
        if key == keyboard.Key.esc:
            break
        record_audio(audio, device_index)
        query = transcript_audio()
        answer = get_answer(query)
        if answer:
            synthesize_speech(answer)
        print('--------------------------------------------------\n')
    finalize(audio)


if __name__ == '__main__':
    main()
    # synthesize_speech(text='The price of cobalt on the market is about $30,000 per 1000 kilograms.')
