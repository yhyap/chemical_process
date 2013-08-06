# Simplified model of reaction in the packed bed
# 
# Determine the length of packed bed reactor required to achieve a desired reactant conversion
# Reactor is packed with solid catalyst pellets which contains catalysts that convert reactants into products
# It considers mass transfer limitation in both external diffusion as well as internal diffusion in the porous structure

# A --> product + other product

# Information about solid pellets
pellet_size = 0.003     # diameter, m
D_e = 2.66e-8           # effective diffusion coefficient, m2/s
bed_porosity = 0.4      # bed porosity
pellet_density = 2e6    # density of solid pellets, g/m3
S_a = 400.0             # internal surface area of the pellet, m2/g

# Inlet gas condition
P = 500e3               # pressure of the inlet gas, Pa
T = 573.                # temperature, K
R = 8.314               # universal gas constant, m3Pa/molK
u = 3.0                 # flow rate, m/s

# External mass transfer coefficient
kcac = 2.0e-2

# Information about the reaction
n = 1.                  # order of the reaction w.r.t. reactant conc, 1=first order
k = 5.e-8               # rate constant, unit changes with order of reaction


import math
import numpy
import matplotlib.pyplot

def inlet_gas_conc(R, T, P):
    """Inlet concentration of gas based on ideal gas law"""
    return P/(R*T)

def thiele_modulus(pellet_density, S_a, inlet_gas_conc, D_e, k, n):
    """Return the Thiele modulus of the pellet given the rate constant and reaction order"""
    return pellet_size/2.0*math.sqrt(k*S_a*pellet_density/D_e*inlet_gas_conc**(n-1))
 
def internal_effectiveness_factor(n, thiele_modulus):
    """Return internal effectiveness factor given the reaction order and thiele modulus"""
    return math.sqrt(2./(n+1))*3./thiele_modulus

def overall_effectiveness_factor(internal_effectiveness_factor, kcac, S_a, pellet_density, k):
    """Return the overall effectiveness factor"""
    a = k * S_a * pellet_density / kcac
    return internal_effectiveness_factor / (1 + internal_effectiveness_factor * a)   

def calculate_length(n, u, inlet_gas_conc, ohm, k, S_a, pellet_density, X):
    """Return the length of packed bed"""
    if n == 1:
        L = u/(ohm*pellet_density*k*S_a)*math.log(1/(1-X))
    elif n == 2:
        L = u/(inlet_gas_conc*ohm*k*S_a*pellet_density)*((1/(1-X)) - 1)
    else:
        raise ValueError("Currently the solver can only handle 1st and 2nd order reaction")
    return "%e" %L

def calculate_conversion(n, u, inlet_gas_conc, ohm, k, S_a, pellet_density, L):
    """Return the conversion achieveable of the packed bed"""
    if n == 1:
        X = 1 - math.exp(L*ohm*pellet_density*k*S_a/u)
    elif n == 2:
        X = 1 - (1/(1+(inlet_gas_conc*ohm*k*S_a*pellet_density*L/u)))
    else:
        raise ValueError("Currently the solver can only handle 1st and 2nd order reaction")
    return "%e" %X
    
def deactivation():
    pass

def effective_diffusion_coefficient():
    """Return the effective diffusion coefficient of the catalytic system"""
    pass



######################## TO FIND LENGTH ########################################
# Specify the desired conversion
X = 0.9

# Generate results
gconc = inlet_gas_conc(R, T, P)
phi = thiele_modulus(pellet_density, S_a, gconc, D_e, k, n)
etha = internal_effectiveness_factor(n, phi)
ohm = overall_effectiveness_factor(etha, kcac, S_a, pellet_density, k)
l = calculate_length(n, u, gconc, ohm, k, S_a, pellet_density, X)
print "The following answers are based on pre-determined parameters"
print "The inlet concentration is", gconc, "mol/m^3"
print "Thiele modulus is", phi
print "The internal effectiveness factor is", etha
print "The overall effectiveness factor is", ohm
print "The length of packed bed is", l, "m"
print ""

# Varying flow rate and conversion to determine the length required
n = raw_input("Enter the order of reaction with respect to reactant concentration: ")
u = [1.0, 2.0, 3.0, 5.0, 10.0]  # in m/s
X = [0.6, 0.7, 0.8, 0.9]        # conversion
l = numpy.zeros((len(u), len(X)))
for i in range(len(u)):
    for j in range(len(X)):
        l[i][j] = calculate_length(float(n), u[i], gconc, ohm, k, S_a, pellet_density, X[j])
print "The matrix of length ", l # in m

# Generating plot
def plot_length():
    axes = matplotlib.pyplot.gca()
    axes.set_xlabel('velocity in m/s')
    axes.set_ylabel('Length of packed bed required in m')
    for j in range(len(X)):
        matplotlib.pyplot.plot(l[:][j])
    matplotlib.pyplot.show()

plot_length()




####################### TO FIND CONVERSION ####################################
# Specify the length required
L = 3 # m
n = 2

# Generate results
gconc = inlet_gas_conc(R, T, P)
phi = thiele_modulus(pellet_density, S_a, gconc, D_e, k, n)
etha = internal_effectiveness_factor(n, phi)
ohm = overall_effectiveness_factor(etha, kcac, S_a, pellet_density, k)
X = calculate_conversion(n, u, gconc, ohm, k, S_a, pellet_density, L)

print "The following answers are based on pre-determined parameters"
print "The inlet concentration is", gconc, "mol/m^3"
print "Thiele modulus is", phi
print "The internal effectiveness factor is", etha
print "The overall effectiveness factor is", ohm
print "The conversion of packed bed is", X
print ""

# Varying flow rate and conversion to determine the conversion achieved
n = raw_input("Enter the order of reaction with respect to reactant concentration: ")
u = [1.0, 2.0, 3.0, 5.0, 10.0]  # in m/s
L = [1, 2, 3, 4, 5]        # conversion
X = numpy.zeros((len(u), len(L)))
for i in range(len(u)):
    for j in range(len(L)):
        X[i][j] = calculate_conversion(float(n), u[i], gconc, ohm, k, S_a, pellet_density, L[j])
print "The matrix of conversion ", X