import class_BBRobot
import class_Camera
import class_PID
import time
import threading
import numpy as np
import cv2
from math import *

loopNum = 0

K_PID = [0.021, 0.00013, 0.007] #Golf perfect!!!!

#K_PID = [0.023, 0.00013, 0.007] #Perfect pingpong

#K_PID = [0, 0, 0]

w = 1
lim = 19

Robot = class_BBRobot.BBrobot()
camera = class_Camera.Camera()
pid = class_PID.PID(K_PID, w, lim)




LOOKUP_TABLE = np.loadtxt("data2.txt", delimiter="|", dtype=str)

# Robot.set_up()
print("Starting")
Robot.Initialize_posture()
pz_ini = Robot.ini_pos[2]


x = -1
y = -1
goal = [0, 0]
D2R = pi / 180
R2D = 1 / D2R

unit_pos = [0, 0]
last_unit_pos = [0, 0]
vel = [0, 0]
alpha = 0
angles = [0,0,0]
last_alpha = 0
beta = 0
last_beta = 0
frame_time = 0
last_frame_time = 0
last_pos = [0,0]
TOL = 0.025
DIST_THRESH = 0.1
ERR_THRESH = 0.5 #1.5
C1 = 0.625
C2 = 0.1
prev_angles = [0.0, 0.0, 0.0]

last_x = 0
last_y = 0
centre_pos = camera.find_centre()

centre_x, centre_y = camera.convertResToCm(centre_pos[0], centre_pos[1])
goal = [centre_x, centre_y]
while(1):
    
    start = time.time()
    x, y = camera.find_ball()
    

    Current_value = [-x, -y]

    if (x != -1 and y != -1):
        x, y = camera.convertResToCm(x, y)
        
        dist_to_last_pos = sqrt((x-last_pos[0])**2 +(y - last_pos[1])**2)
        

        
        if dist_to_last_pos > ERR_THRESH:    
            
            alpha, beta = pid.compute(goal, Current_value)
            
            

            alpha = round(alpha, 0)
            beta = round(beta,0)

                
            i = int((alpha+30)%61+((beta+30)%61)*61+1)
                

            angles = [float(LOOKUP_TABLE[i][2]),float(LOOKUP_TABLE[i][3]),float(LOOKUP_TABLE[i][4])]
            
            if (abs(x) < 0.05 and abs(y) < 0.05):
                angles = prev_angles
            if not (angles[0] == 0 and angles[1] == 0 and angles[2] == 0): 
                prev_angles=angles
                Robot.send_angles(angles)
            last_pos = [x,y]
            prev_angles = angles
        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
Robot.Initialize_posture()

camera.clean_up_cam()
