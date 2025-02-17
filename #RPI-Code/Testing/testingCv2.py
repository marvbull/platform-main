import cv2
import numpy

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
ball_color_lower = numpy.array([20, 100, 100]) 
ball_color_upper = numpy.array([30, 255, 255])

if not cap.isOpened():
    print("error")
else:
    print("Success")
cap.release()