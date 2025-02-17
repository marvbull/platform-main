from sympy import symbols, Eq, solve, sqrt, pretty

# Define symbolic variables
x, z, nx, ny, nz, h, L = symbols('x z nx ny nz h L')

# Substitute specific values for constants
nx_val = 0
ny_val = 0
nz_val = 1
h_val = 6.5
L_val = 15
x_solution = 0
z_solution = 0
y_solution = 0

x_solution2 = 0
z_solution2 = 0
y_solution2 = 0

# Define equations
eq1 = Eq((nx - sqrt(3) * ny) * x + nz * (z - h), 0)
eq2 = Eq(4 * x**2 + (h - z)**2, L**2)

eq3 = Eq((nx + sqrt(3) * ny) * x + nz * (z - h), 0)
eq4 = Eq(4 * x**2 + (h - z)**2, L**2)


# Substitute values into the equations
eq1_substituted = eq1.subs({nx: nx_val, ny: ny_val, nz: nz_val, h: h_val, L: L_val})
eq2_substituted = eq2.subs({nx: nx_val, ny: ny_val, nz: nz_val, h: h_val, L: L_val})

eq3_substituted = eq3.subs({nx: nx_val, ny: ny_val, nz: nz_val, h: h_val, L: L_val})
eq4_substituted = eq4.subs({nx: nx_val, ny: ny_val, nz: nz_val, h: h_val, L: L_val})

# Solve the equations for x and z
solutions = solve((eq1_substituted, eq2_substituted), (x, z))

solutions2 = solve((eq3_substituted, eq4_substituted), (x,z))

print("Solutions for x and z where x > 15:")
for solution in solutions:
    x_value = solution[0]
    z_value = solution[1]
    if x_value.evalf() < 7.5 and x_value.evalf() > -22.5:
        print(f"x: {pretty(x_value)}")
        x_solution = x_value
        y_solution = -sqrt(3)*x_solution
        print(f"y: {float(y_solution)}")  
    if z_value.evalf() < 17 and z_value.evalf() > 6.25:
        print(f"z: {pretty(z_value)}")
        z_solution = z_value
        break
for solution in solutions2:
    x_value = solution[0]
    z_value = solution[1]
    if x_value.evalf() < 7.5 and x_value.evalf() > -22.5:
        print(f"x2: {pretty(x_value)}")
        x_solution2 = x_value
        y_solution2 = sqrt(3)*x_solution2
        print(f"y2: {float(y_solution2)}")  
    if z_value.evalf() < 17 and z_value.evalf() > 6.25:
        print(f"z2: {pretty(z_value)}")
        z_solution2 = z_value
        break