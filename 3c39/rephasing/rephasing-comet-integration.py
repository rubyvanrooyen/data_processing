# part III: Rephase to desired target by changing the phase center
import numpy as np
import pyrap.tables as pt
import sys
import os

from astropy import units as u
from astropy.coordinates import SkyCoord
from datetime import datetime, timedelta,  timezone
from skyfield.api import load, Topos
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
from skyfield.data import mpc

VERBOSE=False
DEBUG=False


if len(sys.argv) < 2:
    msg = f'Usage: {sys.argv[0]} <filename.ms>'
    raise SystemExit(msg)
msfile=sys.argv[1]


## -- Read observational information from MS --
with pt.table(msfile) as tb:
    # extract scan numbers and timestamps per scan
    scan_id = tb.getcol('SCAN_NUMBER')
    scan_time = tb.getcol('TIME_CENTROID')
    interval = tb.getcol('INTERVAL')

# TIME - Mid-point data interval.
# Time is provided in Modified Julian Date.
# The CASA/casacore reference epoch (0 time) for timestamps in MeasurementSets is the MJD epoch: 1858/11/17.
# date -d '1858-11-17 UTC' +%s
t = datetime(1858, 11, 17, 0, 0, tzinfo=timezone.utc)
# MJD is -3506716800 than epoch
if DEBUG: print(f'MJD is {t.timestamp()} than epoch')
epoch=3506716800.

def read_direction(dir_rad):
    ra_rad = dir_rad[0]
    dec_rad = dir_rad[1]
    return SkyCoord(ra_rad*u.radian, dec_rad*u.radian, frame='icrs')

## -- Read observational information from MS --


## -- Comet ephemeris from MeerKAT viewpoint -- 
# build dataframe for comets
with load.open(mpc.COMET_URL) as f:
    comets = mpc.load_comets_dataframe(f)
    # Keep only the most recent orbit for each comet,
    # and index by designation for fast lookup.
    comets = (comets.sort_values('reference')
              .groupby('designation', as_index=False).last()
              .set_index('designation', drop=False))
# read ephemeris of selected comet
ts = load.timescale()
eph = load('de421.bsp')
sun, earth = eph['sun'], eph['earth']
comet_name = '67P/Churyumov-Gerasimenko'
ephem = comets.loc[comet_name]
if VERBOSE:
    print(f'\n{comet_name} ephemeris')
    print(ephem)
comet = sun + mpc.comet_orbit(ephem, ts, GM_SUN)
if DEBUG:
    print('Comet orbit')
    print(comet)
# Apparent topocentric position
# meerkat = earth + wgs84.latlon(30.7130 * S, 21.4430 * E)
meerkat = earth + Topos('30.7130 S', '21.4430 E')
if DEBUG: print(meerkat)
## -- Comet ephemeris from MeerKAT viewpoint -- 


# extract per scan information
[scan_list, scan_idx, num_scans] = np.unique(scan_id, return_index=True, return_counts=True)

print('\nMeerKAT Resolution @ 1.6654 GHz = 4.92 arcsec')
print('\nDateTime\t\t\t\t\t\t\t Scan\t nRows')
for scan, idx, num in zip(scan_list, scan_idx, num_scans):
    starttime = datetime.utcfromtimestamp(scan_time[idx] - interval[idx]/2. - epoch)
    endtime = datetime.utcfromtimestamp(scan_time[idx+num-1] + interval[idx+num-1]/2. - epoch)
    print(f'{starttime} to {endtime}\t {scan}\t {num}')

    dtime = (endtime-starttime).total_seconds()
    obs_time = starttime+timedelta(seconds=dtime/2.)
    print(f'Calc comet phase center to time centroid {obs_time}')

    # how far does comet travel over scan time
    obs_time = obs_time.replace(tzinfo=timezone.utc)
    t = ts.from_datetime(obs_time)
    apparent = meerkat.at(t).observe(comet).apparent()
    ra, dec, distance = apparent.radec()
    _67P_phase_center = SkyCoord(ra.hours*u.hour, dec.degrees*u.degree, frame='icrs')
    ra_hms = ra.hms()
    ra_str = f'{int(ra_hms[0])}h{int(ra_hms[1])}m{ra_hms[2]:.3f}s'
    dec_dms = dec.signed_dms()
    dec_str = f'{int(dec_dms[0]*int(dec_dms[1]))}d{int(dec_dms[2])}m{dec_dms[3]:.3f}s'

    print(f'Scan{str(scan).zfill(2)} @ obs time {obs_time}:\n\tComet phase center {_67P_phase_center} \n\t (ra, dec) = ({ra_str}, {dec_str})')


    scan_str = f'Scan{str(scan).zfill(2)}'
    dt = t.utc_strftime(format="%Y-%b-%d %H:%M:%S")
    phasecenter = f'J2000 {ra_str} {dec_str}'
    print(f'Generate this input from MS: {scan_str}, {dt}, {phasecenter}')
    with pt.table(msfile+'/FIELD') as tb:
        # Phase center.
        phase_ = tb.getcol("PHASE_DIR")[0][0]  # [rad]
        phase_direction = read_direction(phase_)
        print(f'Original phase center: ({str(phase_direction.ra)}, {str(phase_direction.dec)})')
    print('Rephasing phase center')
    os.system("chgcentre {} {} {}".format(msfile, ra_str, dec_str))
    with pt.table(msfile+'/FIELD') as tb:
        # Phase center.
        phase_ = tb.getcol("PHASE_DIR")[0][0]  # [rad]
        phase_direction = read_direction(phase_)
        print(f'Updated phase center: ({str(phase_direction.ra)}, {str(phase_direction.dec)})')

# -fin-
