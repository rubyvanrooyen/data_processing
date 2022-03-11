# part I: Inspect MS and extract scan and datetime information to calculate how far comet travel
from astropy import units as u
from astropy.coordinates import SkyCoord
from datetime import datetime, timezone
from skyfield.api import load, Topos
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
from skyfield.data import mpc

import numpy as np
import pyrap.tables as pt
import sys

VERBOSE=True
DEBUG=False


def comet_travel_dist(starttime, endtime, comet_, observer_): 
    dtime = (endtime-starttime).total_seconds()/60
    # how far does comet travel over scan time
    starttime= starttime.replace(tzinfo=timezone.utc)
    t = ts.from_datetime(starttime)
    apparent = observer_.at(t).observe(comet_).apparent()
    ra, dec, distance = apparent.radec()
    comet_start = SkyCoord(ra.hours*u.hour, dec.degrees*u.degree, frame='icrs')
    ra_hms = ra.hms()
    start_ra_str = f'{int(ra_hms[0])}h{int(ra_hms[1])}m{ra_hms[2]:.3f}s'
    dec_dms = dec.signed_dms()
    start_dec_str = f'{int(dec_dms[0]*int(dec_dms[1]))}d{int(dec_dms[2])}m{dec_dms[3]:.3f}s'

    endtime= endtime.replace(tzinfo=timezone.utc)
    t = ts.from_datetime(endtime)
    apparent = observer_.at(t).observe(comet_).apparent()
    ra, dec, distance = apparent.radec()
    comet_end = SkyCoord(ra.hours*u.hour, dec.degrees*u.degree, frame='icrs')
    ra_hms = ra.hms()
    end_ra_str = f'{int(ra_hms[0])}h{int(ra_hms[1])}m{ra_hms[2]:.3f}s'
    dec_dms = dec.signed_dms()
    end_dec_str = f'{int(dec_dms[0]*int(dec_dms[1]))}d{int(dec_dms[2])}m{dec_dms[3]:.3f}s'
    return comet_start, comet_end, dtime, start_ra_str, start_dec_str, end_ra_str, end_dec_str

if len(sys.argv) < 3:
    msg = f'Usage: {sys.argv[0]} <filename.ms> <time [min]>'
    raise SystemExit(msg)
msfile=sys.argv[1]
dtime=float(sys.argv[2])

if DEBUG: print(msfile)

## -- Read observational information from MS --
with pt.table(msfile) as tb:
    # extract scan numbers and timestamps per scan
    scan_id = tb.getcol('SCAN_NUMBER')
    scan_time = tb.getcol('TIME_CENTROID')
    integration_time = tb.getcol('INTERVAL')

if DEBUG:
    for id_, time_, int_ in zip(scan_id, scan_time, integration_time):
        print(f'scan={id_}, T={time_}, dT={int_}')

# TIME - Mid-point data interval.
# Time is provided in Modified Julian Date.
# The CASA/casacore reference epoch (0 time) for timestamps in MeasurementSets is the MJD epoch: 1858/11/17.
# date -d '1858-11-17 UTC' +%s
t = datetime(1858, 11, 17, 0, 0, tzinfo=timezone.utc)
# MJD is -3506716800 than epoch
if DEBUG: print(f'MJD is {t.timestamp()} than epoch')
epoch=3506716800.
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


# extract per scan information
[scan_list, scan_idx, num_scans] = np.unique(scan_id, return_index=True, return_counts=True)
if DEBUG or VERBOSE:
    print('\nDateTime\t\t\t\t\t\t\t Scan\t nRows')
    for scan, idx, num in zip(scan_list, scan_idx, num_scans):
        starttime = datetime.utcfromtimestamp(scan_time[idx] - integration_time[idx]/2. - epoch)
        endtime = datetime.utcfromtimestamp(scan_time[idx+num-1] + integration_time[idx+num-1]/2. - epoch)
        print(f'{starttime} to {endtime}\t {scan}\t {num}')

# comet travel distance
print('\nMeerKAT Resolution @ 1.6654 GHz = 4.92 arcsec')

# how many minutes does it take the comet to travel over 5''
starttime = datetime.utcfromtimestamp(scan_time[0] - epoch)
endtime = datetime.utcfromtimestamp(scan_time[0] + dtime*60 - epoch)
start_67P, end_67P, dtime, start_ra_str, start_dec_str, end_ra_str, end_dec_str = comet_travel_dist(starttime, endtime, comet, meerkat)
print(f'\nComet travels {end_67P.separation(start_67P).arcsec:.4f} [arcsec] in (dt={dtime:.2f} [min]): from ({start_ra_str}, {start_dec_str}) to ({end_ra_str}, {end_dec_str})')

# -fin-
