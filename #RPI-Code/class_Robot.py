# import class_servo as cs
import math
import time
import sympy 
import scipy
from smbus2 import SMBus
import struct

class BBrobot:
    
    def __init__(self):

        # Link lengths L = [Base, Lower Link, Upper Link, Ceiling]
        self.L = [12.15, 7.5, 7.5, 12.9]
        
        self.ini_pos = [0, 0, 9]
        # self.pz_max = 13
        # self.pz_min = 10
        # self.phi_max = 20 
        self.motor_a_pos = [self.L[0],0,0]
        self.motor_b_pos = [-self.L[0]/2, math.sqrt(3)*self.L[0]/2,0]
        self.motor_c_pos = [-self.L[0]/2,-math.sqrt(3)*self.L[0]/2,0]
        # #print("motor a pos: ", self.motor_a_pos)
        # #print("motor b pos: ", self.motor_b_pos)
        # #print("motor c pos: ", self.motor_c_pos)

        self.addr = 0x8
        self.bus = SMBus(1)


    
    def kinema_inv(self, n, Pz):
        start = time.time()
        for i in range(3):
            if (n[i] == 0):
                n[i] = 0.000000000000001
            print(n[i])

        L = self.L
        ax_solution = 0
        ay_solution = 0
        az_solution = 0
        bx_solution = 0
        by_solution = 0
        bz_solution = 0
        cx_solution = 0
        cy_solution = 0
        cz_solution = 0

        ax, az, bz, cz = sympy.symbols('ax, az, bz, cz', positive = True)
        bx, cx = sympy.symbols('bx, cx')

        

        eqa1 = sympy.Eq(n[0] * ax + n[2] * (az - Pz), 0)
        eqa2 = sympy.Eq(ax**2 + (Pz - az)**2, L[3]**2)

        asolutions = sympy.solve((eqa1, eqa2), (ax, az), force = True)
        
        solve1_time = time.time()

        print("Solver 1 time: ", solve1_time-start)
        

        for solution in asolutions:
            x_value = solution[0]
            z_value = solution[1]
            if x_value < 18 and x_value > 8:

                    ax_solution = x_value
                    ay_solution = 0

            else:
                print("xa value wrong: ", x_value)
            if z_value.evalf() < L[1]+L[2] and z_value.evalf() > 6:

                az_solution = z_value
                break
            else:
                print("Out of scope")
                az_solution = z_value
        
        diff_a_x = abs(self.motor_a_pos[0] - ax_solution)
        diff_a_y = abs(self.motor_a_pos[1] - ay_solution)
        diff_a_z = abs(self.motor_a_pos[2] - az_solution)

        dist_a = sympy.sqrt(diff_a_x**2 + diff_a_y**2 + diff_a_z**2)


        a_r = sympy.sqrt(diff_a_x**2 + diff_a_y**2)
        a_theta = math.degrees(math.atan(Pz/a_r))
        ac_theta = math.degrees(math.acos((dist_a**2 + self.L[1]**2 - self.L[2]**2)/(2*self.L[1]*dist_a)))


        motor_a_theta = a_theta - ac_theta
        math_time = time.time()

        print("Math time: ", math_time-solve1_time)

        eq1 = sympy.Eq((n[0] - sympy.sqrt(3) * n[1]) * bx + n[2] * (bz - Pz), 0)
        eq2 = sympy.Eq(4 * bx**2 + (Pz - bz)**2, L[3]**2)

        eq3 = sympy.Eq((n[0] + sympy.sqrt(3) * n[1]) * cx + n[2] * (cz - Pz), 0)
        eq4 = sympy.Eq(4 * cx**2 + (Pz - cz)**2, L[3]**2)


        bsolutions = sympy.solve((eq1, eq2), (bx, bz))
        csolutions = sympy.solve((eq3, eq4), (cx,cz))

        solve2_time = time.time()

        print("Solver 2 time: ", solve2_time - math_time)

        for solution in bsolutions:
            x_value = solution[0]
            z_value = solution[1]
            if x_value.evalf() < 7.5 and x_value.evalf() > -18:
                bx_solution = x_value
                by_solution = -sympy.sqrt(3)*bx_solution
            else:
                print(" x Out of scope: ", x_value)
            if z_value.evalf() <= L[1]+L[2] and z_value.evalf() > 6.25:
                bz_solution = z_value
                break
            else:
                print("z Out of scope: ", z_value)
                bz_solution = z_value

        for solution in csolutions:
            x_value = solution[0]
            z_value = solution[1]
            if x_value.evalf() < 7.5 and x_value.evalf() > -18:
                cx_solution = x_value
                cy_solution = sympy.sqrt(3)*cx_solution
                
            else:
                print("x2 Out of scope: ", x_value)  
            if z_value.evalf() <= L[1]+L[2] and z_value.evalf() > 6.25:
                cz_solution = z_value
                break
            else:
                print("z2 Out of scope: ", z_value)
                cz_solution = z_value

        diff_b_x = abs(self.motor_b_pos[0] - bx_solution)
        diff_b_y = abs(self.motor_b_pos[1] - by_solution)
        diff_b_z = abs(self.motor_b_pos[2] - bz_solution)

        dist_b = sympy.sqrt(diff_b_x**2 + diff_b_y**2 + diff_b_z**2)

        b_r = sympy.sqrt(diff_b_x**2 + diff_b_y**2)
        b_theta = math.degrees(math.atan(Pz/b_r))
        bc_theta = math.degrees(math.acos((dist_b**2 + self.L[1]**2 - self.L[2]**2)/(2*self.L[1]*dist_b)))
        

        motor_b_theta = b_theta - bc_theta

        diff_c_x = abs(self.motor_c_pos[0] - cx_solution)
        diff_c_y = abs(self.motor_c_pos[1] - cy_solution)
        diff_c_z = abs(self.motor_c_pos[2] - cz_solution)

        dist_c = sympy.sqrt(diff_c_x**2 + diff_c_y**2 + diff_c_z**2)
        

        c_r = sympy.sqrt(diff_c_x**2 + diff_c_y**2)
        c_theta = math.degrees(math.atan(Pz/c_r))
        cc_theta = math.degrees(math.acos((dist_c**2 + self.L[1]**2 - self.L[2]**2)/(2*self.L[1]*dist_c)))
        

        motor_c_theta = c_theta - cc_theta
        thetas = [motor_a_theta, motor_b_theta, motor_c_theta]
        return thetas

    
    def control_t_posture(self, pos, t):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        z_for_mag = z*4
        magnitude = sympy.sqrt(x**2 + y**2 + z_for_mag**2)
        unit_x = x / magnitude
        unit_y = y / magnitude
        unit_z = z_for_mag / magnitude
        n = [unit_x, unit_y, unit_z]
        print("Normal: ")
        print(n)
        angles = self.kinema_inv(n, z)
        print("Angles: ")
        print(angles)

        byte_array = struct.pack('3f', angles[0], angles[1], angles[2])
        self.bus.write_i2c_block_data(self.addr, 0, byte_array)
        time.sleep(t)

    def send_angles(self, angles):
        byte_array = struct.pack('3f', angles[0], angles[1], angles[2])
        self.bus.write_i2c_block_data(self.addr, 0, byte_array)
        

    def control_t_posture_with_n(self, n, z, t):
        #print("Normal: ")
        #print(n)

        angles = self.kinema_inv(n, z)
                
        #print("Angles: ")
        #print(angles)

        byte_array = struct.pack('3f', angles[0], angles[1], angles[2])
        self.bus.write_i2c_block_data(self.addr, 0, byte_array)
        time.sleep(t)
    
    def Initialize_posture(self):
        pos = self.ini_pos
        t = 1
        self.control_t_posture(pos, t)