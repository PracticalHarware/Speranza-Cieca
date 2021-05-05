import speech_recognition as sr;
import playsound
import os
import random
from gtts import gTTS

def speak(audio_string):
    tts = gTTS(text = audio_string, lang = 'en');
    r = random.randint(1, 10000000)
    audio_file = 'audio-'+ str(r) + '.mp3';
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file);

r = sr.Recognizer();

def record_audio(ask = False):
    if ask:
        speak(ask);
    with sr.Microphone() as source:
        audio = r.listen(source);
        voice_data = '';
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry I didnt get that")
        except sr.RequestError:
            speak("Sorry, My Speech service is down")
        return voice_data;  
