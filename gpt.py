import openai

from globals import WAVE_OUTPUT_FILENAME, wrap_text


def transcript_audio():
    print("Audio transcription...")
    audio_file = open(WAVE_OUTPUT_FILENAME, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # print the transcript
    query = transcript.get('text')
    print('>>> Question:', wrap_text(query))
    return query


def get_answer(query):
    if len(query) < 3:
        return ""
    print("Sending request to GPT...")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query,
        max_tokens=1024,
    )
    answer = str.strip(response.choices[0].text)
    print('<<< Answer:', wrap_text(answer))
    return answer
