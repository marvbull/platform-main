import class_BBRobot
import class_Camera
import class_PID
import time
import threading
import numpy as np
import cv2
from math import *

loopNum = 0

# K_PID = [0.015, 0.0001, 0.0051] # Old values

K_PID = [0.023, 0.00013, 0.007] # Ping pong values 0.00011, 0.005
# K_PID = [0.025, 0.001, 0] # Golf ball values
# K_PID = [1, 1, 1] # New Values
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
# centre_pos = camera.find_centre()
# print("centre pos")
# print(centre_pos)
# centre_x, centre_y = camera.convertResToCm(centre_pos[0], centre_pos[1])
# goal = [centre_x, centre_y]
goal =[100, 0]
while(1):
    start = time.time()
    x, y = camera.find_ball()
    

    Current_value = [-x, -y]

    if (x != -1 and y != -1):   
        alpha, beta = pid.compute(goal, Current_value)
        
        

        alpha = round(alpha, 0)
        beta = round(beta, 0)

            
        i = int((alpha+30)%61+((beta+30)%61)*61+1)
            

        angles = [float(LOOKUP_TABLE[i][2]),float(LOOKUP_TABLE[i][3]),float(LOOKUP_TABLE[i][4])]
        
        if not (angles[0] == 0 and angles[1] == 0 and angles[2] == 0): 
            prev_angles=angles
            Robot.send_angles(angles)
        prev_angles = angles

        if (abs(Current_value[0] - goal[0]) > 35):
            print("bye bye bye bye")
        else:
            goal[0] = -goal[0]

        print(x)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
Robot.Initialize_posture()
camera.clean_up_cam()

