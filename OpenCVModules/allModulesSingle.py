import cv2
import sys
import numpy as np
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackingModule as htm
import speech_recognition as sr;
import playsound
import os
import random
from gtts import gTTS
import threading
carCascade = cv2.CascadeClassifier('haarCode.xml')
video = cv2.VideoCapture('cars.mp4')

WIDTH = 1280
HEIGHT = 720

faceCascade = cv2.CascadeClassifier('E:\OpenCV\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

def plainFaceRecog():
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)

        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
           break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
    
    
def peopleRecognition():
    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    cv2.startWindowThread()
    
    # open webcam video stream
    cap = cv2.VideoCapture(0)
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
    
        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
    
        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                              (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('frame',frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    
    # When everything done, release the capture
    cap.release()
    # and release the output
    
    # finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)
   
def controlVolume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    #volume.GetMute()
    #volume.GetMasterVolumeLevel()
    
    volRange =  volume.GetVolumeRange();
    
    minVol = volRange[0]
    maxVol = volRange[1]
    
    cap = cv2.VideoCapture(0)
    
    detector = htm.handDetector(detectionCon=0.7);
    
    cap.set(3, wCam)
    cap.set(4, hCam)
    
    pTime = 0;
    vol = 0;
    volBar = 400;
    volPer = 0;
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img);
        
        lmList = detector.findPosition(img, draw = False);
        
        if len(lmList) != 0:
            #print(lmList[4], lmList[8]);
            
            x1,y1 = lmList[4][1], lmList[4][2];
            x2,y2 = lmList[8][1], lmList[8][2];
            
            cx,cy = ((x1+x2)//2, (y1+y2)//2);
            
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3);
            cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
            
            length = math.hypot(x2-x1, y2 - y1);
            #print(length)
            
            #Hand Range 25 : 250
            #Volumne Range -65 : 0
            
            vol = np.interp(length, [25,180], [minVol, maxVol]);
            volBar = np.interp(length, [25,180], [400, 150]);
            volPer = np.interp(length, [25,180], [0, 100]);
            volume.SetMasterVolumeLevel(vol, None)
            
            if length<50:
                cv2.cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)
                
        #For rectange in size
        cv2.rectangle(img, (50, 150), (85, 400), (0,255,0), 3);
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0,255,0), cv2.FILLED);
        cv2.putText(img, f'{int(volPer)}', (40,450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0),2)
            
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime;
        cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0),2)
        
        cv2.imshow("Img", img);
        
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

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
def estimateSpeed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    # ppm = location2[2] / carWidht
    ppm = 8.8
    d_meters = d_pixels / ppm
    #print("d_pixels=" + str(d_pixels), "d_meters=" + str(d_meters))
    fps = 18
    speed = d_meters * fps * 3.6
    return speed

def relative_location(location1, location2):
    posX = location2[0] - location1[0];
    posY = location2[1] - location1[1];
    
    x = location2[0];
    
    if(x>640 and posY>0):
        return "Right and towards you";
    elif(x>640 and posY<0):
        return "Right and away from you";
    elif(x<640 and posY>0):
        return "left and towars you";
    elif(x<640 and posY<0):
        return "left and away from you";
    elif(x == 640 and posY>0):
        return 'Centre and towars you';
    elif(x == 640 and posY<0):
        return 'Centre and away from you';
    else:
        return 'There is a vehicle';
    

def trackMultipleObjects():
    rectangleColor = (0, 255, 0)
    frameCounter = 0
    currentCarID = 0
    fps = 0
    
    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = [None] * 1000
    
    position = [None] * 1000;
    
    
    # Write output to video file
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))


    while True:
        start_time = time.time()
        rc, image = video.read()
        if type(image) == type(None):
            break
        
        image = cv2.resize(image, (WIDTH, HEIGHT))
        resultImage = image.copy()
        
        frameCounter = frameCounter + 1
        
        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image)
            
            if trackingQuality < 7:
                carIDtoDelete.append(carID)
                
        for carID in carIDtoDelete:
            print ('Removing carID ' + str(carID) + ' from list of trackers.')
            print ('Removing carID ' + str(carID) + ' previous location.')
            print ('Removing carID ' + str(carID) + ' current location.')
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)
        
        if not (frameCounter % 10):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))
            
            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)
            
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h
                
                matchCarID = None
            
                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()
                    
                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())
                    
                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h
                
                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                        matchCarID = carID
                
                if matchCarID is None:
                    print ('Creating new tracker ' + str(currentCarID))
                    
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))
                    
                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]

                    currentCarID = currentCarID + 1
        
        #cv2.line(resultImage,(0,480),(1280,480),(255,0,0),5)


        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()
                    
            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())
            
            cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)
            
            # speed estimation
            carLocation2[carID] = [t_x, t_y, t_w, t_h]
        
        end_time = time.time()
        
        if not (end_time == start_time):
            fps = 1.0/(end_time - start_time)
        
        #cv2.putText(resultImage, 'FPS: ' + str(int(fps)), (620, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)


        for i in carLocation1.keys():    
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]
        
                # print 'previous location: ' + str(carLocation1[i]) + ', current location: ' + str(carLocation2[i])
                carLocation1[i] = [x2, y2, w2, h2]
        
                # print 'new previous location: ' + str(carLocation1[i])
                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])
                        position[i] = relative_location([x1, y1, w1, h1], [x2, y2, w2, h2])
                        
                        

                    #if y1 > 275 and y1 < 285:
                    if speed[i] != None and y1 >= 180:
                        #cv2.putText(resultImage, str(int(speed[i])) + " km/hr", (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                        cv2.putText(resultImage, position[i], (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                        
                    
                    #print ('CarID ' + str(i) + ': speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')

                    #else:
                    #    cv2.putText(resultImage, "Far Object", (int(x1 + w1/2), int(y1)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                        #print ('CarID ' + str(i) + ' Location1: ' + str(carLocation1[i]) + ' Location2: ' + str(carLocation2[i]) + ' speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')
        cv2.imshow('result', resultImage)
        # Write the frame into the file 'output.avi'
        #out.write(resultImage)


        if cv2.waitKey(33) == 27:
            break
    
    cv2.destroyAllWindows()
