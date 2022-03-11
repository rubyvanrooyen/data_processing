# Adjusting target phase center to repoint

## Rephase comet phase center per integration dump
Workflow for calculating and rephasing comet coordinates per integration dumps

Find time interval comet travel over 5'' (beam width)
```
Usage: calc-comet-distance.py <filename.ms> <time [min]>
python calc-comet-distance.py 1627186156_sdp_l0-3c39-corr.ms 3.33
```
```
MeerKAT Resolution @ 1.6654 GHz = 4.92 arcsec
Comet travels 4.9819 [arcsec] in (dt=3.33 [min]): from (1h20m51.957s, 3d42m55.486s) to (1h20m52.265s, 3d42m57.340s)
```
Split out individual MS files for that time interval

Extract individual integration timestamps
```
python split-per-integration.py 1627186156_sdp_l0-3c39-corr.ms
ls -al integration_times.npy
```

Split out integrations into separate MS files
```
casa --log2term
run split-per-integration.py 1627186156_sdp_l0-3c39-corr.ms
```

For each time interval MS, calculate comet phase centre and rephase to desired target by changing the phase centre
```
for file in 1627186156_sdp_l0-3c39-*.ms ; do python rephasing-comet-integration.py $file ; done
```

Concat to new MS file
The script is very bare, so it needs the user to first edit the script to select time chunks,
as well as update the section where the number is extacted to make sure the index agrees with the current naming convension
```
casa --log2term
run concat-comet-integrations.py 1627186156_sdp_l0-3c39-*.ms
```

Image data over all updated MS files
```
wsclean -j 8 -name 'comet67p.wsclean' -size 8192 8192 -scale 1.5arcsec -niter 20000 -weight briggs 0.5 -threshold 0.0 -pol I -mgain 0.85 -padding 1.2 -auto-threshold 10 -auto-mask 15 -channels-out 8 -join-channels -fit-spectral-pol 4 1627186156_sdp_l0-3c39-rephased.ms
```

Build a time series of images as comet travel across 3C39
```
./comet-path-images.sh
```

Align MS filenames with fits images generated to that they are in order of motion
```
comet-path-lists.sh
```


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
