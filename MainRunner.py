import speech_recognition as sr;
from time import ctime;
import time;
import webbrowser;
from sys import exit;

import playsound
import os
import random
from gtts import gTTS

import VolumeControlModule as VCM;
import PeopleRecognitionModule as PRM;
import VehicleTracking as VT;
import EasyOCRSnapShot as EOCR;

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

def respond(voice_data):
    if "what is your name" in voice_data:
        speak("My name is Helen");
    if "what is the time" in voice_data:
        speak(ctime());
    if 'search' in voice_data:
        search_data = record_audio('What are you looking for?');
        url = 'https://google.com/search?q='+search_data;
        webbrowser.get().open(url);
        speak("Here is what I found for"+search_data);
    if 'find location' in voice_data:
        location_data = record_audio('What is the location?');
        location_data.replace(' ', ',+');
        url = 'https://google.nl/maps/place/'+ location_data + '/&amp;';
        webbrowser.get().open(url);
        speak("Here is the location of " + location_data);
    if ('give directions' in voice_data) or ('get directions' in voice_data) :
        start_data = record_audio('What is the start location');
        destination_data = record_audio('What is the end location');
        start_data.replace(' ', ',+');
        destination_data.replace(' ', ',+');
        url = 'https://www.google.nl/maps/dir/'+ start_data + '/'+destination_data;
        webbrowser.get().open(url);
        speak("Here are the directions from " + start_data + ' to ' + destination_data);
    if 'control volume' in voice_data:
        VCM.control_volume();
        speak('Volume set');
    if 'recognize people' in voice_data:
        PRM.peopleRecognition();
        speak('Done with people recognition');
    if 'detect cars around me' in voice_data:
        VT.trackMultipleObjects()
    if 'read for me' in voice_data:
        EOCR.scan_read();
    if 'exit' in voice_data:
        exit();

time.sleep(1);
speak("Hello, How can i help you")
while True:
    voice_data = record_audio();
    speak(voice_data)
    respond(voice_data);

