import math
import time

L = [15, 8.5, 8.5, 15]
        
ini_pos = [0, 0, 12]
pz_max = 11
pz_min = 8
# phi_max = 20 
motor_a_pos = [L[3],0,0]
motor_b_pos = [-L[3]/2, math.sqrt(3)*L[3]/2,0]
motor_c_pos = [-L[3]/2,-math.sqrt(3)*L[3]/2,0]
print("motor a pos: ", motor_a_pos)
print("motor b pos: ", motor_b_pos)
print("motor c pos: ", motor_c_pos)


x = 0
y = 0
z = 12
magnitude = math.sqrt(x**2 + y**2 + z**2)
unit_x = x / magnitude
unit_y = y / magnitude
unit_z = z / magnitude
n = [unit_x, unit_y, unit_z]

print('Normal: ', n)

Pz = z

a_m_z = Pz + (L[3]/(math.sqrt(n[0]**2 + n[2]**2)))*(-n[0])
a_m_x = math.sqrt(L[3]**2 - (ini_pos[2] - a_m_z)**2)
a_m_y = 0


diff_a_x = abs(motor_a_pos[0] - a_m_x)
diff_a_y = abs(motor_a_pos[1] - a_m_y)
diff_a_z = abs(motor_a_pos[2] - a_m_z)

dist_a = math.sqrt(diff_a_x**2 + diff_a_y**2 + diff_a_z**2)

a_r = math.sqrt(diff_a_x**2 + diff_a_y**2)

a_theta = math.degrees(math.acos(a_r/dist_a))
ac_theta = math.degrees(math.acos((dist_a**2 + L[1]**2 - L[2]**2)/(2*L[1]*dist_a)))

motor_a_theta = 180 - a_theta - ac_theta


b_m_x = (L[3]/(math.sqrt(n[0]**2+3*n[1]**2+4*n[2]**2-2*math.sqrt(3)*n[0]*n[1])))*(-n[2])

b_m_y = (L[3]/(math.sqrt(n[0]**2+3*n[1]**2+4*n[2]**2-2*math.sqrt(3)*n[0]*n[1])))*(math.sqrt(3)*n[2])
b_m_z = Pz + (L[3]/(math.sqrt(n[0]**2+3*n[1]**2+4*n[2]**2-2*math.sqrt(3)*n[0]*n[1])))*(-math.sqrt(3)*n[1]+n[0])


diff_b_x = abs(motor_b_pos[0] - b_m_x)
diff_b_y = abs(motor_b_pos[1] - b_m_y)
diff_b_z = abs(motor_b_pos[2] - b_m_z)

dist_b = math.sqrt(diff_b_x**2 + diff_b_y**2 + diff_b_z**2)

b_r = math.sqrt(diff_b_x**2 + diff_b_y**2)
b_theta = math.degrees(math.acos(b_r/dist_b))
bc_theta = math.degrees(math.acos((dist_b**2 + L[1]**2 - L[2]**2)/(2*L[1]*dist_b)))

motor_b_theta = 180 - b_theta - bc_theta

c_m_x = (L[3]/(math.sqrt(n[0]**2+3*n[1]**2+4*n[2]**2-2*math.sqrt(3)*n[0]*n[1])))*(-n[2])
c_m_y = (L[3]/(math.sqrt(n[0]**2+3*n[1]**2+4*n[2]**2-2*math.sqrt(3)*n[0]*n[1])))*(-math.sqrt(3)*n[2])
c_m_z = Pz + (L[3]/(math.sqrt(n[0]**2+3*n[1]**2+4*n[2]**2-2*math.sqrt(3)*n[0]*n[1])))*(math.sqrt(3)*n[1]+n[0])


diff_c_x = abs(motor_c_pos[0] - c_m_x)
diff_c_y = abs(motor_c_pos[1] - c_m_y)
diff_c_z = abs(motor_c_pos[2] - c_m_z)


dist_c = math.sqrt(diff_c_x**2 + diff_c_y**2 + diff_c_z**2)

c_r = math.sqrt(diff_c_x**2 + diff_c_y**2)
c_theta = math.degrees(math.acos(c_r/dist_c))

cc_theta = math.degrees(math.acos((dist_c**2 + L[1]**2 - L[2]**2)/(2*L[1]*dist_c)))
print("bmx ", cc_theta)

motor_c_theta = 180 - c_theta - cc_theta
thetas = [motor_a_theta, motor_b_theta, motor_c_theta]

print("Angles: ", thetas)
