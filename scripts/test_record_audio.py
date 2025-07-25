#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "openai",
#     "playsound",
#     "pyaudio",
# ]
# ///

# Testing for https://github.com/ArduPilot/MAVProxy/pull/1588

'''
AI Chat Module voice-to-text class
Randy Mackay, December 2023

AP_FLAKE8_CLEAN
'''


try:
    import pyaudio  # install using, "sudo apt-get install python3-pyaudio"
    import wave     # install with "pip3 install wave"
    from openai import OpenAI
except Exception:
    print("chat: failed to import pyaudio, wave or openai.  See https://ardupilot.org/mavproxy/docs/modules/chat.html")
    exit()

# initializing the global list to keep and update the stop_recording state
stop_recording = [False]


class chat_voice_to_text():
    def __init__(self):
        # initialise variables
        self.client = None
        self.assistant = None

    # set the OpenAI API key
    def set_api_key(self, api_key_str):
        self.client = OpenAI(api_key=api_key_str)

    # check connection to OpenAI assistant and connect if necessary
    # returns True if connection is good, False if not
    def check_connection(self):
        # create connection object
        if self.client is None:
            try:
                self.client = OpenAI()
            except Exception:
                print("chat: failed to connect to OpenAI")
                return False

        # return True if connected
        return self.client is not None

    # record audio from microphone
    # returns filename of recording or None if failed
    def record_audio(self):
        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open stream
        try:
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        except Exception:
            print("chat: failed to connect to microphone")
            return None

        # record until specified time
        frames = []
        while not stop_recording[0]:
            data = stream.read(1024)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # update the recording state back to false globally
        stop_recording[0] = False

        # Save audio file
        wf = wave.open("recording.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()
        return "recording.wav"

    # convert audio to text
    # returns transcribed text on success or None if failed
    def convert_audio_to_text(self, audio_filename):
        # check connection
        if not self.check_connection():
            return None

        # Process with Whisper
        audio_file = open(audio_filename, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text")
        return transcript


if __name__ == "__main__":
    from pathlib import Path
    from playsound import playsound
    filename = chat_voice_to_text().record_audio()
    assert filename == "recording.wav"
    filepath = Path(__file__).parent / filename
    assert filepath.exists()
    assert filepath.is_file()
    print(f"{filepath.stat() = }")
    print(f"Size of {filepath} is {filepath.stat().st_size:,} bytes.")
    playsound(filename, block=True)
    playsound(filepath, block=True)
