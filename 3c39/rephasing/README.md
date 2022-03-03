# Adjusting target phase center to repoint

## Rephase comet phase center per integration dump


## Rephase comet phase center per scan
Workflow for calculating and rephasing scans to comet coordinates

Inspect MS to extract scan and datetime information, using this to calculate anticipated comet position from ephemeris
```
python extract-rephase-information.py 1627186165_sdp_l0-3c39-cont.ms
```

Use CASA to split out individual scans
```
CASA <41>: run split-comet-scans.py 1627186165_sdp_l0-3c39-cont.ms comet67P_scans.txt
```

Rephase to desired target by changing the phase centre
```
python rephasing-comet-scans.py
```

-fin-
