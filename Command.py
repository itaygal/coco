import threading
from Messages import ReceiveMessage
from TextAnalyzer import TextAnalyzer
import Actions
from TextToSpeech import TextToSpeech

class CommandCenter(ReceiveMessage, threading.Thread):
    __instance = None

    @staticmethod
    def get_instance():
        if CommandCenter.__instance is None:
            CommandCenter()
        return CommandCenter.__instance

    def __init__(self):
        if CommandCenter.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            super(CommandCenter, self).__init__()
            CommandCenter.__instance = self
            self.stop = False
            self.commands = []
            self.init_commands()

    def stop(self):
        self.stop = True

    def init_commands(self):
        self.commands.append(Commad("echo", ["echo", "print"], Actions.print_action))
        self.commands.append(Commad("start music", ["music", "start", "on", "begin", "open", "play"], Actions.start_music))
        self.commands.append(Commad("stop music", ["music", "stop", "end", "close", "off"], Actions.stop_music))
        self.commands.append(Commad("download song", ["download", "song", "youtube"], Actions.download_song))
        self.commands.append(Commad("bye", ["bye"], Actions.stop_run))

    def run(self):
        text_analyzer = TextAnalyzer.get_instance()
        while not self.stop:
            task = self.get_message()
            max_score = 0
            best_matched_command = None
            for command in self.commands:
                similarity_score = text_analyzer.similarity_score(task.get_tokens(), command.get_key_words())
                if max_score < similarity_score:
                    best_matched_command = command
                    max_score = similarity_score
            if best_matched_command is not None:
                result = best_matched_command.perform(task)
                if result:
                    TextToSpeech.get_instance().send_message("successfully performed " + best_matched_command.get_name() + " command")
                else:
                    TextToSpeech.get_instance().send_message("unsuccessfully performed " + best_matched_command.get_name() + " command")

class Task:
    def __init__(self, request, request_tokens):
        super(Task, self).__init__()
        self.request = request
        self.request_tokens = request_tokens

    def get_request(self):
        return self.request

    def get_tokens(self):
        return self.request_tokens

class Commad:
    def __init__(self, name, key_words, action):
        super(Commad, self).__init__()
        self.name = name
        self.key_words = key_words
        self.action = action

    def get_name(self):
        return self.name

    def get_key_words(self):
        return self.key_words

    def perform(self, task):
        return self.action(task)
