"""
    Line and continuum point source sensitity
    From Brad Frank
"""

import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

import numpy as np


if len(sys.argv) < 2:
    msg = 'Usage: {} <filename.ms>'.format(sys.argv[0])
    raise SystemExit(msg)
vis=sys.argv[1]

print(vis)

k = 1.38e03
tb.open(vis+'/ANTENNA')
N = len(tb.getcol('NAME')) 
D = tb.getcol('DISH_DIAMETER')[0]
A = np.pi*(D/2.)**2
tb.close()
tb.open(vis+'/SPECTRAL_WINDOW')
#channel increments or bandwidth can end up being negative after
#conversion to velocity space with cvel
dv = np.absolute(tb.getcol('TOTAL_BANDWIDTH')[0])
Nchan = tb.getcol('NUM_CHAN')[0]
dv_per_chan = np.absolute(tb.getcol('CHAN_WIDTH')[0])
tb.close()
tb.open(vis)

#I am assuming this is a split file with a single field
Nints = len(np.unique(tb.getcol('TIME')[np.where(tb.getcol('FIELD_ID')==0)[0]]))
dt = tb.getcol('EXPOSURE')[0]
T = Nints * dt
# pss_N = np.sqrt(2)*Tsys*k
# pss_D = eff * A * np.sqrt(N*(N-1)*dv*T)
T_eta = 20
pss_N = np.sqrt(2)*T_eta*k
pss_D = A * np.sqrt(N*(N-1)*dv*T)
pss = pss_N / pss_D
# pss_D_per_chan = eff * A * np.sqrt(N*(N-1)*dv_per_chan*T)
pss_D_per_chan = A * np.sqrt(N*(N-1)*dv_per_chan*T)
pss_per_chan = pss_N / pss_D_per_chan

print("\n")
print("\n")
print("Point Source Sensitivity Parameters")
print("-----------------------------------")
print("Total Integration Time [s] = "+str(T))
print("Total Bandwidth [Hz] = "+str(dv))
print("Number of Channels = "+str(Nchan))
print("Number of Antennas = "+str(N))
print("Approximate Dish Area [m^2] = "+str(A))
print("User Input(Tsys/eta [K] = "+str(T_eta))
print("\n")
print("Point Source Sensitivity [Jy] = "+str(pss))
print("Point Source Sensitivity per channel [Jy] = "+str(pss_per_chan[0]))

# -fin-
