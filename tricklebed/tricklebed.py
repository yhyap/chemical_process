
# PROBLEM:
# Hydrogenation of aromatics in naphtenic lube oil distillate
# Based on sample question in Fogler
# Calculate the percentage of resistance in elementary steps in a trickle bed reactor.


# Information about the trickle bed
h = 1.          # m, height
d = 6.          # m, diameter of the bed
T = 373.        # K, temperature in the reactor
P = 50.         # atm, pressure in the reactor
por = 0.35      # porosity of the bed
dP_dL = 30.     # kPa/m, pressure gradient based on 25 kg gas/m2s

# Information about the hydrogen gas feed
H = 0.0068      # mol/dm^3.atm, hydrogen solubility in the oil
F_0h2 = 0.2     # kg/m2s, hydrogen flow rate

# Information about the inert nitrogen gas
F_0n2 = 0.05    # kg/m2s, nitrogen flow rate

# Information about the liquid (naphtenic lube oil) in the feed
c_0aro = 0.07   # mol/dm^3m concentration of aromatic in the feed
F_oil = 8.      # kg/m2s, superficial liquid flow rate
mu_oil = 3.e-3  # kg/m.s, viscosity of oil
rho_oil = 900   # kg/m3, density of oil
D_aro = 6.e-11  # m2/s, diffusivity of aromatics in oil
D_h2 = 8.e-9    # m2/s, diffusivity of H2 in oil

# Information about the solid catalyst pellets
d_p = 0.003175  # m, pellet diameter
rho_p = 1500.   # kg/m3, density of the pellet
tortuosity = 3.8
por_p = 0.5     # porosity of the pellet
constriction = 0.8 

# Information about the reaction on the catalyst surface
k = 2.e-6       # m6/kmol.kg.s


#########################################################################
def D_eff(D_AB, por, tau, sigma):
    """return the effective diffusion coefficient in the porous catalyst"""
    return D_AB*sigma*por/tau




class Resistance:
    """Resistance class for individual resistance"""
    
    class gas_film:
        pass
    
    class liquid_film:
        pass
    
    class extMT:
        """Resistance in external mass transfer/diffusion"""
        def __init__(self):
            pass
        
        def ext_surface_area(self, rho_p, d_p):
            """Return the external surface area of the pellet"""
            ac = 6./(d_p*rho_p)
            return ac
            
        def Re(self, rho, u, d_p, mu):
            """Return the Reynolds number"""
            return rho*u*d_p/mu
    
        def Sc(self, rho, mu, D_AB):
            """Return the Schmidt number"""
            return mu/(rho*D_AB)
    
        def kc(self, Re, Sc, D_AB, d_p):
            """Return the mass transfer coefficient from bulk liquid to surface"""
            Sh = 0.266*Re**1.15*Sc**(1./3)
            return Sh*D_AB/d_p
            
        def resistance(self, kc, ext_surface_area):
            r = 1./(kc*ext_surface_area)
            return "%e" %r
    
    class reaction:
        def Thiele():
            pass



class Liquid_resistance(Resistance):
    pass

class Gas_resistance(Resistance):
    pass
    

# Determine external mass transfer resistance of aromatics
r = Resistance.extMT()              #@@@@@@@@@@@@@@@@@@@------------
u = F_oil/rho_oil                   # m/s, fluid velocity
ext_sa = r.ext_surface_area(rho_p, d_p)
Re = r.Re(rho_oil, u, d_p, mu_oil)
Sc = r.Sc(rho_oil, mu_oil, D_aro)
kc = r.kc(Re, Sc, D_aro, d_p)
result = r.resistance(kc, ext_sa)

print Re
print Sc
print kc
print result