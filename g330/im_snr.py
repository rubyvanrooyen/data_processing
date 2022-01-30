"""Calculate expected thermal noise"""

import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

import numpy as np

def rms_noise_AeT(N, B, tau, T_eta ):
    """ Noise calculation using measured Tsys/Eta_ap from tipping curves"""
    k = 1.38e-23  #Boltzmann's constant
    #eta_inf = 0.94 # interferometer efficiency, worst case
    #eta_ap = 0.99 * 0.99 * 0.65
    R = 13.5 / 2.
    area = np.pi * (R**2)
    rms = (1/np.sqrt(2)) * (2*k*T_eta) / (area*np.sqrt(N*(N-1)*B*tau))
    print('Expected rms noise is %.3f mJy'%(rms/1e-29))
    return rms/1e-26  # Jy


if len(sys.argv) < 2:
    msg = 'Usage: {} <filename.ms>'.format(sys.argv[0])
    raise SystemExit(msg)
msfile=sys.argv[1]

print(msfile)

# Array size
tb.open(msfile + '/ANTENNA')
antennas = tb.getcol('NAME')
N = len(antennas)
tb.close()

# Channel width
tb.open(msfile + '/SPECTRAL_WINDOW')
dv = np.mean(tb.getcol('CHAN_WIDTH'))  # Hz
tb.close()

# Total Integration Time
tb.open(msfile)
Nints = len(np.unique(tb.getcol('TIME')))
dt = np.mean(tb.getcol('EXPOSURE'))
T = Nints * dt  # sec
tb.close()

snr = rms_noise_AeT(N, dv, T, 20)  # Jy
threshold = ' '.join([str(3*snr), 'Jy'])
print('Set clean threshold = {}'.format(threshold))

# -fin-
