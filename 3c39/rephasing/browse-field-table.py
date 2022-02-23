from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pyrap.tables as pt
import sys

if len(sys.argv) < 2:
    msg = f'Usage: {sys.argv[0]} <filename.ms>'
    raise SystemExit(msg)
msfile=sys.argv[1]

def read_direction(dir_rad):
    ra_rad = dir_rad[0]
    dec_rad = dir_rad[1]
    return SkyCoord(ra_rad*u.radian, dec_rad*u.radian, frame='icrs')

with pt.table(msfile+'/FIELD') as tb:
    # Direction of delay center.
    delay_ = tb.getcol("DELAY_DIR")[0][0]  # [rad]
    delay_direction = read_direction(delay_)
    print(f'Delay center: ({str(delay_direction.ra)}, {str(delay_direction.dec)})')
    # Phase center.
    phase_ = tb.getcol("PHASE_DIR")[0][0]  # [rad]
    phase_direction = read_direction(phase_)
    print(f'Phase center: ({str(phase_direction.ra)}, {str(phase_direction.dec)})')
    # Reference center
    reference_ = tb.getcol("REFERENCE_DIR")[0][0]  # [rad]
    reference_direction = read_direction(reference_)
    print(f'Reference center: ({str(reference_direction.ra)}, {str(reference_direction.dec)})')

# -fin-
