import math
import time
    
class PID:
    def __init__(self, K_PID, weight, lim):
        self.kp = K_PID[0]
        self.ki = K_PID[1]
        self.kd = K_PID[2]
        self.weight = weight  
        self.last_alpha = 0
        self.last_beta = 0
        self.last_error_x = 0
        self.last_error_y = 0
        self.integral_x = 0
        self.integral_y = 0
        self.last_time = None
        self.lim = lim
        self.cap = 11

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def compute(self, Goal, Current_value):
        current_time = time.perf_counter()
        if self.last_time is None:
            self.last_time = current_time
            return 0, 0
       
        error_x = Goal[0] - Current_value[0]
        error_y = Goal[1] - Current_value[1]
        
        self.integral_x += error_x * (current_time - self.last_time)
        self.integral_y += error_y * (current_time - self.last_time)
        
        derivative_x = (error_x - self.last_error_x) / (current_time - self.last_time)
        derivative_y = (error_y - self.last_error_y) / (current_time - self.last_time)
        
        alpha = self.kp * error_x + self.ki * self.integral_x + self.kd * derivative_x
        beta = self.kp * error_y + self.ki * self.integral_y + self.kd * derivative_y
        
        alpha = self.clamp(self.weight * alpha + (1 - self.weight) * self.last_alpha, -self.lim, self.lim)
        beta = - self.clamp(self.weight * beta + (1 - self.weight) * self.last_beta, -self.lim, self.lim)

        self.last_error_x = error_x
        self.last_error_y = error_y
        self.last_alpha = alpha
        self.last_beta = beta
        self.last_time = current_time
        
        return alpha, beta
