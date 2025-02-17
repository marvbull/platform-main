import cv2
import numpy as np
import math
class Camera:
    def __init__(self):
        # Initialize camera with OpenCV
        self.cap = cv2.VideoCapture(0)
        self.height = 720 
        self.width = 720 
        self.radius = 35
        self._radius_centre = 15

        self.cap.set(cv2.CAP_PROP_FPS, 30)

        # [Hue, Saturation, Value]
        self.ball_color_lower = np.array([23, 100, 100]) # golf ball values
        self.ball_color_upper = np.array([35, 255, 255]) # golf ball values

        #[RGB]
        # self.ball_color_lower = np.array([140, 100, 0]) # ping pong ball values
        # self.ball_color_upper = np.array([200, 150, 60]) # ping pong ball values


    def find_centre(self):
        ret, frame = self.cap.read()
        while not ret:
            print("Failed to grab frame") 
        
        frame = cv2.resize(frame, (self.height, self.width))
        
        # image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.ball_color_lower, self.ball_color_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            if radius > self._radius_centre: 
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)
                cv2.imshow('frame', frame)
                x -= self.height / 2
                y -= self.width / 2

                return int(x), int(y)
        cv2.imshow('frame', frame)
        
    def find_ball(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return 1, 1  
        
        frame = cv2.resize(frame, (self.height, self.width))
        
        # image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.ball_color_lower, self.ball_color_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            if radius > self.radius: 
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)
                cv2.imshow('frame', frame)
                x -= self.height / 2
                y -= self.width / 2
                
                

                return int(x), int(y)
            
        cv2.imshow('frame', frame)
        return 1, 1  

    def clean_up_cam(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def convertResToCm(self, x, y):

        return (x)*12.9/(self.height/2), (y)*12.9/(self.width/2),
    
    def isBallAtPoint(self, goal_x, goal_y):
        x,y = self.find_ball()
        if (abs(goal_x - x) < self.radius and abs(goal_y - y) < self.radius):
            return True
        else:
            return False