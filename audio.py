import audioop
import wave

from pynput import keyboard

from globals import FORMAT, CHANNELS, RATE, CHUNK, MIN_RECORD_SECONDS, SILENCE_THRESHOLD, WAVE_OUTPUT_FILENAME
from keyboard import get_key_pressed


def record_audio(audio, device_index):
    # Open microphone stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=device_index,
                        frames_per_buffer=CHUNK)

    print("Recording... press SPACE to finish, ESC to exit")

    # Initialize a buffer to store audio data
    frames = []
    silence_count = 0
    min_record_count = int(RATE / CHUNK * MIN_RECORD_SECONDS)
    record_count = 0

    # Record audio until a short period of silence is detected
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        record_count += 1
        if audioop.rms(data, 2) < SILENCE_THRESHOLD:
            silence_count += 1
        else:
            silence_count = 0
        if record_count > min_record_count and silence_count > int(
                RATE / CHUNK * 0.5):  # adjust the silence period as needed
            break
        key = get_key_pressed()
        if key == keyboard.Key.esc:
            exit(1)
        if key == keyboard.Key.space:
            break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Write audio data to a WAV file
    wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
