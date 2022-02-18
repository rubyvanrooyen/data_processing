# part II: Use CASA to split out individual scans
import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

if len(sys.argv) < 3:
    msg = 'Usage: {} <filename.ms> <scandata.txt>'.format(sys.argv[0])
    raise SystemExit(msg)
msfile=sys.argv[1]
scanfile=sys.argv[2]

print(msfile)
basename= os.path.splitext(os.path.basename(msfile))[0]
[mktag, target, _] = basename.split('-')

print(scanfile)
with open(scanfile, 'r') as fin:
    scans = fin.readlines()
SCANS = [tuple(scan.strip().split(',')) for scan in scans]
for scan, utc, phasecenter in SCANS:
    print('Generate this input from MS: {}, {}, {}'.format(scan, utc, phasecenter))
    split_scan_ms = '{}-{}-{}.ms'.format(mktag, target, scan)
    print('Split MS for input: {}'.format(split_scan_ms))

    if os.access(split_scan_ms, F_OK):
        print('Deleting existing measurement set {}\n'.format(split_scan_ms))
        os.system('rm -rf ' + split_outputvis)

    scan_nr = int(scan[4:])
    split(vis=msfile, outputvis=split_scan_ms, datacolumn='all', scan=scan_nr)

# -fin-
