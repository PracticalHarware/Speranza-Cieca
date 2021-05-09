import easyocr
import cv2
import random
import time
import os

import SpeechAndAudioModule as SAM;

def scan_read():

    cap = cv2.VideoCapture(0);
    reader = easyocr.Reader(['en'], gpu= False);
    
    success, img = cap.read();
    
    if not success:
        print('Failed to take picture')
    else:
        cv2.imshow("Image", img);
        
        time.sleep(5)
        
        r = random.randint(1, 10000000)
        img_name = 'image-'+str(r)+'.png'
        cv2.imwrite(img_name, img);
        
        time.sleep(5)
        
        result = reader.readtext(img_name);
        
        for detection in result:
            text = detection[1]
            SAM.speak(text);
            
        os.remove(img_name);
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_read();
