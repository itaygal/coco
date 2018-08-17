This is my voice recognition python project.
It uses Google Web Speech API for voice to text.
It uses my algorithm for matching user request to specific commands (uses gensim word2vec model)
user request must contain the coco key word. For example : "coco download song"
This is user voice command will be matched to the most similar command (using command key words).

Coco project has the following dependencies
	gensim
	gTTs
	SpeechRecognition
	youtube-dl
	pyglet
All can easily be installed using pip

For gensim the GoogleNews-vectors-negative300.bin is needed.
After download place it in main project directory.

Currently supported commands
    "download_song":
        description - while in a youtube page, this will download song as .mp3 and save it in download folder
        key words - ["download", "song", "youtube"]
    "echo":
        description - echo user input
        key words - ["echo", "print"]
    "bye":
        description - shutdown coco
        key words - ["bye"]