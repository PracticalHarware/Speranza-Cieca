import numpy as np
import cv2

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
