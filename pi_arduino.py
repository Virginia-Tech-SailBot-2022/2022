import cv2
import numpy as np

from threading import Thread

import picamera.array as pca
from picamera import PiCamera
from time import sleep

# image = cv2.imread("buoy.jpg")
#cv2.imshow('Original', image)
# cv2.waitKey(1)

#hsvimg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV);
#cv2.imshow('HSV', hsvimg)
cv2.namedWindow('Track')

#trackbar
def track(x):
    pass
cv2.createTrackbar('Hmin', 'Track', 0, 179, track);
cv2.createTrackbar('Hmax', 'Track', 10, 179, track);
cv2.createTrackbar('Smin', 'Track', 0, 255, track);
cv2.createTrackbar('Smax', 'Track', 255, 255, track);
cv2.createTrackbar('Vmin', 'Track', 0, 255, track);
cv2.createTrackbar('Vmax', 'Track', 255, 255, track);


# for webcam
# cap = cv2.VideoCapture(0)

# for usb-camera (PS3)
# cap = cv2.VideoCapture(0)

#for pi camera
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 5

camera.start_recording('testRecording.h264')

cap=pca.PiRGBArray(camera, size = (640,368))

sleep(0.1)

while True:
    #webcam

    frame = camera.capture("/home/pi/Pictures/img.jpg")
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #image = cv2.imread("buoy.jpg");
    h_min = cv2.getTrackbarPos('Hmin', 'Track')
    h_max = cv2.getTrackbarPos('Hmax', 'Track')
    s_min = cv2.getTrackbarPos('Smin', 'Track')
    s_max = cv2.getTrackbarPos('Smax', 'Track')
    v_min = cv2.getTrackbarPos('Vmin', 'Track')
    v_max = cv2.getTrackbarPos('Vmax', 'Track')
    # print(str(h_min) + " " + str(h_max) + " " + str(s_min) + " " + str(s_max) + " "+ str(v_min) + " " + str(v_max))

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    #mask = cv2.inRange(hsvimg, lower, upper)
    mask2 = cv2.inRange(hsv_frame, lower, upper)
    cv2.imshow('Mask', mask2)

    contours, hierarchy = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    lists = list(contours)
    if len(lists) == 0:
        cv2.imshow('Video', frame)
        continue

    lists.sort(key=cv2.contourArea, reverse=True)
    
    red_area = lists[0]
    (xg, yg, wg, hg) = cv2.boundingRect(red_area)
    cv2.rectangle(frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 3)
    #cv2.drawContours(frame, red_area, -1, (0, 255, 0), 3)
    #cv2.putText(frame, "Area: " + str(cv2.contourArea(red_area)), (xg, yg), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))

    print(str(wg*hg))

    '''
red_area2 = lists[1]
    (xg, yg, wg, hg) = cv2.boundingRect(red_area2)
    cv2.rectangle(frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 3)
'''
#cv2.drawContours(frame, red_area2, -1, (0, 255, 0), 3)
    #print(cv2.contourArea(red_area2))
    #cv2.putText(frame, "Area: " + str(cv2.contourArea(red_area2)), (xg, yg), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
    cv2.imshow('Video', frame)



    #cv2.imshow('Original', image);



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break