from Messages import ReceiveMessage
from Locks import speech_lock

import threading
from gtts import gTTS
from time import sleep
import os
import pyglet

class TextToSpeech(ReceiveMessage, threading.Thread):
    __instance = None

    @staticmethod
    def get_instance():
        if TextToSpeech.__instance is None:
            TextToSpeech()
        return TextToSpeech.__instance

    def __init__(self):
        if TextToSpeech.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            super(TextToSpeech, self).__init__()
            TextToSpeech.__instance = self
            self.stop = False

    def run(self):
        while not self.stop:
            msg = self.get_message()
            self.speak(msg)

    def stop(self):
        self.stop = True

    def speak(self, msg):
        """Text to speech. For funp."""
        try:
            tts = gTTS(text=msg, lang='en')
            filename = 'temp.mp3'
            tts.save(filename)

            music = pyglet.media.load(filename, streaming=False)
            with speech_lock:
                music.play()
                sleep(music.duration)  # prevent from killing

            os.remove(filename)  # remove temperory file
        except Exception:
            pass