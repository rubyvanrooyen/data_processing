## Data and tables
Test data for G330 was created by extracting the calibrator observations and using them to
build comparison reports between CASA and caracal processing


## CASA on com14 using singularity
Not doing a new CASA installation, using the old singularity image to view the data with CASA
Basic bash prompt inside the container
```
singularity shell -B /scratch/ruby /scratch/shared/containers/singularity/sarao_science.simg
```
or
```
singularity exec -B /scratch/ruby /scratch/shared/containers/singularity/sarao_science.simg /bin/bash --norc
```

CASA binary lives in:`ls /usr/src/casa/casa-release-5.3.0-143.el7/bin/`
for convenience, create a symbolic link: `ln -s /usr/src/casa/casa-release-5.3.0-143.el7/bin/casa`
```
./casa --log2term
./casa --log2term --nologger
```


## Calibration
```
setjy(vis=msfile, field='J1939-6342', fluxdensity=-1, standard='Perley-Butler 2010')

crosscal:
  ...
  set_model:
    enable: true
    meerkat_skymodel: false
  ...

plotms(vis=msfile, xaxis='freq', yaxis='amp', correlation='XX,YY', field='J1939-6342', ydatacolumn='model', avgtime='5200', averagedata=True, avgbaseline=True, coloraxis='scan')
```


```
crosscal:
  ...
  primary:
    reuse_existing_gains: true
    order: KGBAKGB
    combine: ["", "", "", null, "", "", ""]
    solint: [inf, inf, inf, null, int, int, inf]
    calmode: [a, ap, ap, null, a, ap, ap]
    b_fillgaps: 70
    plotgains: true
  ...
```
```
crosscal:
  ...
  secondary:
    reuse_existing_gains: true
    order: KGAKFI
    apply: B
    combine: ["", "", null, "", "", null]
    solint: [inf, inf, null, 60s, 60s, null]
    calmode: [a, ap, null, a, ap, null]
    plotgains: true
    image:
      npix: 10000
      cell: 0.8
      niter: 100000
      nchans: 8
  ...
```
```
crosscal:
  ...
  apply_cal:
    applyto:
      - fcal
      - bpcal
      - gcal
  ...
```


## Verification
        plots:
          # phaseball plots
          - dir: "phaseballs-{msbase}"
            plots:
              - "-x real -y imag -c CORR --corr IQUV --hline 0: --vline 0:"
              - "-x real -y imag -c SCAN_NUMBER"
              - "-x real -y imag -c ANTENNA1"
          - dir: "phaseballs-bycorr-{msbase}"
            iter_corr:
            plots:
              - "-x real -y imag -c SCAN_NUMBER"
              - "-x real -y imag -c ANTENNA1"
          # normalized phaseballs
          - dir: "normballs-{msbase}"
            col: "CORRECTED_DATA/MODEL_DATA"
            corr: "XX,YY"
            iter_corr:
            plots:
              - "-x real -y imag -c SCAN_NUMBER"
              - "-x real -y imag -c ANTENNA1"
          # block and triangle plots
          - dir: "blockplots-{msbase}"
            plots:
              - "-x BASELINE_M -y FREQ -c amp"
              - "-x ANTENNA1 -y ANTENNA2 -c SCAN_NUMBER --aaxis phase --ared std"
              - "-x ANTENNA1 -y ANTENNA2 -c SCAN_NUMBER --aaxis amp --ared mean"
          # amp/phase versus uv-distance, and uv-coverage coloured by amp/phase
          - dir: "uvdist-{msbase}"
            plots:
              - "-x UV -y amp    -c SCAN_NUMBER"
              - "-x UV -y amp    -c ANTENNA1"
              - "-x UV -y phase  -c ANTENNA1 --corr XX,YY"
              - "-x U  -y V      -c amp"
              - "-x U  -y V      -c phase --cmin -5 --cmax 5"
          # spectral plots
          - dir: "spectra-{msbase}"
            plots:
              - "-x FREQ  -y amp  -c SCAN_NUMBER"
              - "-x FREQ  -y amp  -c ANTENNA1"
              - "-x FREQ  -y real -c CORR --corr IQUV --hline 0:"
-fin-
