# Determine the length of packed bed reactor required to achieve a desired reactant conversion
# Reactor is packed with solid catalyst pellets which contains catalysts that convert reactants into products
# It considers mass transfer limitation in both external diffusion as well as internal diffusion in the porous structure

# A --> product

# Information about solid pellets
pellet_size = 0.004     # diameter
D_e = 2.66e-8           # effective diffusion coefficient, m2/s
bed_porosity = 0.4      # bed porosity
pellet_density = 2e6    # density of solid pellets, g/m3
S_a = 400.0             # internal surface area of the pellet, m2/g

# Inlet gas condition
P = 500e3               # pressure of the inlet gas, Pa
T = 523.                # temperature, K
R = 8.314               # universal gas constant, m3Pa/molK
u = 3.0                 # flow rate, m/s

# Information about the reaction
n = 2.                  # second order w.r.t. reactant concentration
k = 5e-9                # rate constant


import math
import numpy

def inlet_gas_conc(R, T, P):
    """Inlet concentration of gas"""
    return P/(R*T)

def thiele_modulus(pellet_density, S_a, inlet_gas_conc, D_e, k, n):
    """Return the Thiele modulus of the pellet given the rate constant and reaction order"""
    return pellet_size/2.0*math.sqrt(k*S_a*pellet_density/D_e*inlet_gas_conc**(n-1))
 
def internal_effectiveness_factor(n, thiele_modulus):
    """Return internal effectiveness factor given the reaction order and thiele modulus"""
    return math.sqrt(2./(n+1))*3./thiele_modulus

def ohm():
    """Return the overall effectiveness factor"""
    return internal_effectiveness_factor    # If the internal factor is very small

def packedbed_length(u, inlet_gas_conc, ohm, k, S_a, pellet_density, X):
    """Return the length of packed bed"""
    L = u/(inlet_gas_conc*ohm*k*S_a*pellet_density)*((1/(1-X)) - 1)
    return "%e" %L

def packedbed_conversion():
    """Return the conversion achieveable of the packed bed"""
    pass        # Need to derive this

# Specify the desired conversion
X = 0.8

# Generate results
gconc = inlet_gas_conc(R, T, P)
thiele = thiele_modulus(pellet_density, S_a, gconc, D_e, k, n)
pi = internal_effectiveness_factor(n, thiele)

print gconc
print thiele
print pi
l = packedbed_length(u, gconc, pi, k, S_a, pellet_density, X)
print l  


# Varying flow rate to determine the length required
u = [1.0, 2.0, 3.0, 5.0, 10.0]  # in m/s
l = numpy.zeros(5)
for i in range(len(u)):
    l[i] = packedbed_length(u[i], gconc, pi, k, S_a, pellet_density, X)
print l # in m
# The length required is increasing as there are more reactants flow in


