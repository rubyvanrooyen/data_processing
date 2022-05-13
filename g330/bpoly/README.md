Development and implementation of BPOLY prototype in CARACal pipeline

Use wideband data calibration since the data is much less: `run-J1939-6342-4k-bpoly.yml`

Testing various options for NB calibration
* Calibration with BPOLY option
```
caracal -c run-J1939-6342-32k-bpoly.yml
```
* Calibration with B and smoothing
```
caracal -c run-J1939-6342-32k-bpoly.yml -ew crosscal__smooth_bpcal
```

-fin-
