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

VERBOSE=True
DEBUG=True


if len(sys.argv) < 2:
    msg = f'Usage: {sys.argv[0]} <filename.ms>'
    raise SystemExit(msg)
msfile=sys.argv[1]
if DEBUG: print(msfile)


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
# ## -- Read observational information from MS --


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
if DEBUG or VERBOSE:
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


def read_direction(dir_rad):
    ra_rad = dir_rad[0]
    dec_rad = dir_rad[1]
    return SkyCoord(ra_rad*u.radian, dec_rad*u.radian, frame='icrs')


def deg2hms(degs_):
    HH = int(degs_/15)
    MM = int((degs_/15 - HH)*60)
    SS = ((degs_/15 - HH)*60 - MM)*60
    return f'{HH}h{MM}m{SS:.2f}s'


# extract per scan information
[scan_list, scan_idx, num_scans] = np.unique(scan_id, return_index=True, return_counts=True)

print('\nMeerKAT Resolution @ 1.6654 GHz = 4.92 arcsec')
print('\nDateTime\t\t\t\t\t\t\t Scan\t nRows')
for scan, idx, num in zip(scan_list, scan_idx, num_scans):
    starttime = datetime.utcfromtimestamp(scan_time[idx] - interval[idx]/2. - epoch)
    endtime = datetime.utcfromtimestamp(scan_time[idx+num-1] + interval[idx+num-1]/2. - epoch)
    print(f'{starttime} to {endtime}\t {scan}\t {num}')

    dtime = (endtime-starttime).total_seconds()
    obs_time = starttime + timedelta(seconds=dtime/2.)
    obs_time = obs_time.replace(tzinfo=timezone.utc)
    obs_ts = obs_time.timestamp()
    new_scan_time = obs_ts + epoch# + interval[idx]/2.
    print(f'Calc comet phase center to time centroid {obs_time}')

    # how far does comet travel over scan time
    t = ts.from_datetime(obs_time)
    apparent = meerkat.at(t).observe(comet).apparent()
    ra, dec, distance = apparent.radec()
    _67P_phase_center = SkyCoord(ra.hours*u.hour, dec.degrees*u.degree, frame='icrs')
    print(f'Comet phase center @ obs time {obs_time} = {_67P_phase_center}')
    ra_hms = ra.hms()
    ra_str = f'{int(ra_hms[0])}h{int(ra_hms[1])}m{ra_hms[2]:.3f}s'
    dec_dms = dec.signed_dms()
    dec_str = f'{int(dec_dms[0]*int(dec_dms[1]))}d{int(dec_dms[2])}m{dec_dms[3]:.3f}s'

    print(f'Scan{str(scan).zfill(2)} @ obs time {obs_time}:\n\tComet phase center {_67P_phase_center} \n\t (ra, dec) = ({ra_str}, {dec_str})')

    # inspecting current phase center set to occulation target 3C39
    with pt.table(msfile+'/FIELD') as tb:
        target_ = tb.getcol("NAME")[0]
        # Phase center.
        phase_ = tb.getcol("PHASE_DIR")[0][0]  # [rad]
        phase_direction = read_direction(phase_)
        print(f'Original phase center: ({str(phase_direction.ra)}, {str(phase_direction.dec)})')
        obs_time_ = datetime.utcfromtimestamp(tb.getcol("TIME")[0]-epoch)
        obs_time_ = obs_time_.replace(tzinfo=timezone.utc)
        print(f'Original phase center on occulation target {target_} observed @ {obs_time_}: ({deg2hms(phase_direction.ra.degree)}, {str(phase_direction.dec)})')

    scan_str = f'Scan{str(scan).zfill(2)}'
    dt = t.utc_strftime(format="%Y-%b-%d %H:%M:%S")
    phasecenter = f'J2000 {ra_str} {dec_str}'
    print(f'Generate this input from MS: {scan_str}, {dt}, {phasecenter}')
    print('Rephasing phase center')
    os.system("chgcentre {} {} {}".format(msfile, ra_str, dec_str))
    # rename target to comet
    with pt.table(msfile+'/FIELD', readonly=False) as tb:
        tb.putcol('NAME', "comet67P")
        tb.putcol('TIME', new_scan_time)
        tb.flush()

    with pt.table(msfile+'/FIELD') as tb:
        target_ = tb.getcol("NAME")[0]
        # Phase center.
        phase_ = tb.getcol("PHASE_DIR")[0][0]  # [rad]
        phase_direction = read_direction(phase_)
        obs_time_ = datetime.utcfromtimestamp(tb.getcol("TIME")[0]-epoch)
        print(f'Updated phase center on comet {target_} observed @ {obs_time_}: ({deg2hms(phase_direction.ra.degree)}, {str(phase_direction.dec)})')

# -fin-
