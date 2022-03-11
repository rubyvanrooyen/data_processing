# part I: Inspect MS and extract scan and datetime information to calculate how far comet travel
# from astropy import units as u
# from astropy.coordinates import SkyCoord
from datetime import datetime
# from skyfield.api import load, Topos
# from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
# from skyfield.data import mpc
import os
from os import F_OK
CASA=True
try:
    from tasks import *
    from taskinit import *
    import casac
except:
    CASA=False
    from datetime import timezone
    import pyrap.tables as pt
    pass

import numpy as np
import os
import sys

VERBOSE=True
DEBUG=False

print(CASA)
if len(sys.argv) < 2:
    msg = 'Usage: {sys.argv[0]} <filename.ms>'
    raise SystemExit(msg)
msfile=sys.argv[1]
basename= os.path.splitext(os.path.basename(msfile))[0]
[mktag, target, _] = basename.split('-')

if DEBUG: print(msfile)

if not CASA:
    ## -- Read observational information from MS --
    with pt.table(msfile) as tb:
        # extract scan numbers and timestamps per scan
        scan_id = tb.getcol('SCAN_NUMBER')
        scan_time = tb.getcol('TIME_CENTROID')
        integration_time = tb.getcol('INTERVAL')

    if DEBUG:
        for id_, time_, int_ in zip(scan_id, scan_time, integration_time):
            print('scan={}, T={}, dT={}'.format(id_, time_, int_))

    # TIME - Mid-point data interval.
    # Time is provided in Modified Julian Date.
    # The CASA/casacore reference epoch (0 time) for timestamps in MeasurementSets is the MJD epoch: 1858/11/17.
    # date -d '1858-11-17 UTC' +%s
    t = datetime(1858, 11, 17, 0, 0, tzinfo=timezone.utc)
    # MJD is -3506716800 than epoch
    if DEBUG: print('MJD is {} than epoch'.format(t.timestamp()))
    epoch=3506716800.
    ## -- Read observational information from MS --


    ## -- Find unique timestamps per integration --
    int_times_arr = []
    int_times = np.unique(scan_time)
    for timestamp in int_times:
        # calculate Topocentric projected position of comet
        obs_time = datetime.utcfromtimestamp(timestamp - epoch)
        obs_time_str = obs_time.strftime('%Y/%m/%d/%H:%M:%S')
        print(timestamp, obs_time, 'YYYY/MM/DD/hh:mm:ss', obs_time_str)
        int_times_arr.append(obs_time_str)
    int_times_arr = np.asarray(int_times_arr)
    np.save('integration_times', int_times_arr)
    ## -- Find unique timestamps per integration --


## -- Split out MS per integration --
int_times = []
target='67P'
if CASA:
    int_times = np.load('integration_times.npy')
    for cnt, obs_time_str in enumerate(int_times):
#         split_dump_ms = '{}-{}-{}.ms'.format(mktag, target, obs_time_str)
        split_dump_ms = '{}-{}-{}.ms'.format(mktag, target, str(cnt))
        print('Split MS for input: {}'.format(split_dump_ms))
        if os.access(split_dump_ms, F_OK):
            print('Deleting existing measurement set {}\n'.format(split_dump_ms))
            os.system('rm -rf ' + split_dump_ms)

        split(vis=msfile, outputvis=split_dump_ms, datacolumn='all', timerange=str(obs_time_str))
## -- Split out MS per integration --


# -fin-
