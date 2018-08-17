import warnings
warnings.filterwarnings("ignore", message="detected Windows; aliasing chunkize to chunkize_serial")
warnings.filterwarnings("ignore", message=".*Conversion of the second argument of issubdtype from .*")
from SpeechRecognition import SpeechRecognizer
from Command import CommandCenter
from TextToSpeech import TextToSpeech


if __name__ == "__main__":
    text_to_speech = TextToSpeech()
    command_center = CommandCenter()
    speech_recognizer = SpeechRecognizer()
    text_to_speech.start()
    command_center.start()
    speech_recognizer.start()
    text_to_speech.send_message("Coco up and running")

