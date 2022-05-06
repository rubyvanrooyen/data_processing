"""
    For maser observations, Doppler correction may be necessary.
    CVEL will apply Doppler correction in the requested reference frame and regrid the data if necessary.
    Doppler-tracking correction:
        Split out a specified velocity range for each source
        The rest frequency and measurement frame (topocentric) is set in the measurement set
        CVEL is then run to apply doppler correction and convert to the LSRK velocity frame
"""
import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

import numpy as np


# global parameters
vis_maser = '1625501782_sdp_l0-G330_89_0_36-corr.ms'
target = 'G330.89-0.36'

# Calibrated, Doppler corrected measurement set with suffix 'cvel.ms'
def regrid_vlsr(cal_target_ms,
                target,
                restfreq,
#                 spw='',
                rm_outvis=False,
                ):

    freq_str =  str(restfreq/1e6)+'MHz' # make a string for cvel input and filename
    # Note if Doppler correction is done, each transition needs to be split out into a separate ms so that the appropriate rest frequency can be applied.
    split_outvis = target+'_'+freq_str+'.ms'
    if os.access(split_outvis, F_OK):
        print 'Deleting existing measurement set '+split_outvis+'\n'
        os.system('rm -rf '+split_outvis)
    split(vis=cal_target_ms,
          outputvis=split_outvis,
          field=target,
#           spw=spw,
          datacolumn='all')

    tb.open(split_outvis+'/SPECTRAL_WINDOW', nomodify=False)
    tb.putcell('REF_FREQUENCY', 0, restfreq)
    tb.close()

    cvel_outvis = target+'_'+freq_str+'.cvel.ms'
    if os.access(cvel_outvis, F_OK):
        print 'Deleting existing measurement set '+cvel_outvis+'\n'
        os.system('rm -rf '+ cvel_outvis)
    cvel(vis=split_outvis,
         outputvis=cvel_outvis,
         mode='velocity',
#          start=start_vel,
#          nchan=nchans,
         interpolation='linear',
         outframe='LSRK',
         restfreq=freq_str)

    if rm_outvis:
        print 'removing intermediate dataset \n'
        os.system('rm -rf '+split_outputvis)

# regrid_vlsr(cal_target_ms=vis_maser,
#             target=target,
#             restfreq=1665.40184e6,
#             spw='0:17250~17550'
#             )

regrid_vlsr(cal_target_ms=vis_maser,
            target=target,
            restfreq=1665.40184e6,
#             spw='0:17250~17550',
            )

# regrid_vlsr(cal_target_ms=vis_maser,
#             target=target,
#             restfreq=1667.35903e6,
# #           spw='0:??~??',
#             )

# -fin-
