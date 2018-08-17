from TextAnalyzer import TextAnalyzer
from Command import CommandCenter, Task
from Locks import speech_lock
import speech_recognition as sr
import threading
import json
import time

class SpeechRecognizer(threading.Thread):
    __instance = None

    @staticmethod
    def get_instance():
        if SpeechRecognizer.__instance is None:
            SpeechRecognizer()
        return SpeechRecognizer.__instance

    def __init__(self):
        if SpeechRecognizer.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            super(SpeechRecognizer, self).__init__()
            SpeechRecognizer.__instance = self
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.stop = False

    def stop(self):
        self.stop = True

    def run(self):
        text_analyzer = TextAnalyzer.get_instance()
        command_center = CommandCenter.get_instance()
        while not self.stop:
            response = self.recognize_speech_from_mic()
            if response["success"] and response["request"]:
                print("got request " + json.dumps(response))
                request_tokens = text_analyzer.parse(response["request"])
                if text_analyzer.for_coco(request_tokens):
                    command_center.send_message(Task(response["request"], request_tokens))

    def recognize_speech_from_mic(self):
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        audio = None
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            with speech_lock:
                print("waiting for request")
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                except sr.WaitTimeoutError:
                    pass

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "request": None
        }

        if audio is None:
            return response

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["request"] = self.recognizer.recognize_google(audio)
            #response["request"] = self.recognizer.recognize_sphinx(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response