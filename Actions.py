from TextToSpeech import TextToSpeech

def print_action(task):
    echo_request_tokens = [word for word in task.get_tokens() if word not in ["echo", "print", "coco"]]
    TextToSpeech.get_instance().send_message(' '.join(echo_request_tokens))
    return True

def start_music(task):
    print("start music")
    return True

def stop_music(task):
    print("stop music")
    return True

def download_song(task):
    print("download_song")
    TextToSpeech.get_instance().send_message("downloading song")

    import youtube_dl
    import uiautomation as automation

    control = automation.GetFocusedControl()
    controlList = []
    while control:
        controlList.insert(0, control)
        control = control.GetParentControl()

    if len(controlList) == 1:
        control = controlList[0]
    else:
        control = controlList[1]

    address_control = automation.FindControl(control, lambda c, d: isinstance(c,  automation.EditControl) and "Address and search bar" in c.Name)

    if address_control is None:
        return False

    try:
        song_url = address_control.CurrentValue()
        import os
        import sys
        import youtube_dl

        project_path = os.path.dirname(sys.argv[0])
        os.chdir(project_path + "//ffprobe")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': project_path + "//downloads//%(title)s.%(ext)s",
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_url])

        os.chdir(project_path)
        return True

    except AttributeError as error:
        return False

def stop_run():
    print("stop_run")
    from SpeechRecognition import SpeechRecognizer
    from Command import CommandCenter
    from TextToSpeech import TextToSpeech

    SpeechRecognizer.get_instance().stop()
    CommandCenter.get_instance().stop()
    TextToSpeech.get_instance().stop()



