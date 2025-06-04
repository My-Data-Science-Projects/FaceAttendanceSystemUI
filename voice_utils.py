import os
import uuid
import time
from gtts import gTTS
import pygame

def speak_attendance_success(name):
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)

    file_name = f"{uuid.uuid4()}.mp3"
    temp_file_path = os.path.join(temp_dir, file_name)

    try:
        tts = gTTS(text=f"Hey {name}, your attendance marked successfully", lang='en')
        tts.save(temp_file_path)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

        os.remove(temp_file_path)

    except Exception as e:
        print("Voice error:", e)