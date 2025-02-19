# G330 starformation region OH maser observations

https://archive.sarao.ac.za/proposalid/SSV-20210701-SA-01/target/G330.89-0.36/order/true/

Commissioning

```
Targets: 3 selected out of 3 in catalogue
  ID  Name          Type      RA(J2000)     DEC(J2000)  Tags
   0  J1939-6342    radec     19:39:25.03  -63:42:45.6  fluxcal bpcal delaycal 
   1  G330.89-0.36  radec     16:10:20.54  -52:06:14.9  target
   2  J1726-5529    radec     17:26:49.63  -55:29:40.5  gaincal
```

## CASA data
Selected individual sources for CASA recipe extraction to caracal pipeline
```
# primary calibrator
 ./getms.sh -r 163,3885 --t J1939-6342 https://archive-gw-1.kat.ac.za/1626935818/1626935818_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhcmNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjI2OTU2NjMwLCJwcmVmaXgiOlsiMTYyNjkzNTgxOCJdLCJleHAiOjE2Mjc1NjE0MzAsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.wye2P0SprT-13CZLcWLYhhyeg_NLwgUWFOJUoku2BcKuEnKcUTPQ3uh_AoyY05tUdD0Wvy7WkaNRdLYkvub6Og
# secondary calibrator
 ./getms.sh -r 163,3885 --t J1726-5529 https://archive-gw-1.kat.ac.za/1626935818/1626935818_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhcmNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjI2OTU2NjMwLCJwcmVmaXgiOlsiMTYyNjkzNTgxOCJdLCJleHAiOjE2Mjc1NjE0MzAsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.wye2P0SprT-13CZLcWLYhhyeg_NLwgUWFOJUoku2BcKuEnKcUTPQ3uh_AoyY05tUdD0Wvy7WkaNRdLYkvub6Og
```

## CARACAL data
Wideband data extraction (full data set):   
```
mvftoms.py -f --flags cam
https://archive-gw-1.kat.ac.za/1625501775/1625501775_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhcmNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjI3ODk5MzY3LCJwcmVmaXgiOlsiMTYyNTUwMTc3NSJdLCJleHAiOjE2Mjg1MDQxNjcsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.EX2msmU0UaR-BNk9ybE3GxmPIwvNHTaY_OqTjChBuoGx1UJnYQhnaWtHDNZugbqXfckGasLafqCCUHSX5ukbjA
```
Narrow band data set (10 MHz chunk):   
```
mvftoms.py -f -a --flags cam -C 12709,18834
https://archive-gw-1.kat.ac.za/1625501782/1625501782_sdp_l0.full.rdb?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJrYXQtYXJjaGl2ZS5rYXQuYWMuemEiLCJhdWQiOiJhcmNoaXZlLWd3LTEua2F0LmFjLnphIiwiaWF0IjoxNjI3ODk5MzY3LCJwcmVmaXgiOlsiMTYyNTUwMTc4MiJdLCJleHAiOjE2Mjg1MDQxNjcsInN1YiI6InJ1YnlAc2FyYW8uYWMuemEiLCJzY29wZXMiOlsicmVhZCJdfQ.vTg4NmDeOcrtftLqHC9_b9ni8XrXLRpHO3sEzFRRpRojgCCFwmBksHvsKUlMQzFgJLiUnoltx6gwaTtfrZjP8Q
```
Make data readonly
```
chmod -R-w <filename>.ms
```

## TMUX setup
Using screen/tmux session
### start tmux session
```
tmux new -s g330
```
### attach to tmux session
```
tmux ls
tmux a -t g330
```


## Get data from archive
### symbolic link to data extraction script
```
ln -s katcomm/Users/ruby/oh_masers/bin/getms.sh
```

```
mvftoms.py -f --flags cam <katdaltoken>
```


## CASA on com14
```
./casa --log2term --nologger
```

### inspecting data
View the calibrator data for initial flagging using the calibrators and wideband data.
Some example [notebooks](https://github.com/rubyvanrooyen/data_processing/tree/master/notebooks) are available in the repository.
Use only frequency, time periods and explicit target names to allow mapping of CASA flags to caracal   
However, for the averaging, use the ms information since it is only for visualisation and
smoothing/averaging of the data.


## Caracal
* Extract you data from the archive using `getms.sh`
* Construct the caracal pipeline config file (config-1625501775_sdp_l0-4k.yml)
* Run caracal pipeline process

### Running pipeline
```
source venv3.7/bin/activate
ln -s /scratch/ruby/g330/data/ ms-orig

caracal -c <config_file>.yml

# sw : start-worker
# ew : end-worker
caracal -c wideband_pipeline.yml -sw general -ew transform__calibrators
```

Check caracal config file settings
```
caracal -c wideband_pipeline.yml -sw general -ew general
caracal -c wideband_pipeline.yml -ew inspec
caracal -c wideband_pipeline.yml -sw transform__target
```

To quickly clean up the temporary output products generated by caracal
```
make clean
```
To remove all output, as well as
```
make clobber
```


## Implementation
### Wideband data processing
* Run the basic CARACAL workers to create an MS file of calibrator sources
`caracal -c run-g330-4k.yml -sw general -ew prep__calibrators`
* Initial cycle of flagging, calibration and inspection using CARACAL workers
`caracal -c run-g330-4k.yml -sw flag__calibrators -ew inspect`
* Selfcal and imaging <TBD>

### Narrow band data processing
* Run the basic CARACAL workers to create an MS file of calibrator sources    
Initial cycle of flagging, calibration and inspection using CARACAL workers
`caracal -c run-g330-32k.yml -ew flag__calibrators


## Imaging and spectral line analysis
```
wsclean -j 8 -name G330_89_0_36-wide.clean -size 8192 8192  -scale 1.5arcsec -weight briggs -0.5 -niter 20000 -threshold 0.0 -channels-out 7 -pol I -fit-spectral-pol 3 -auto-threshold 10  -auto-mask 15 -padding 1.2 -mgain 0.85 -join-channels -fit-beam 1625501775_sdp_l0-G330_89_0_36-corr.ms
```

```
casa --log2term

run spectral-analysis.py

run make-cubes.py

viewer('G330.878-0.367-1665.40184MHz.clean.contsub.velocity.image')
imagename='G330.878-0.367-1665.40184MHz.clean.contsub.velocity.image'
mom0_file='G330.878-0.367-1665.40184MHz.clean.contsub.velocity.mom0'
immoments(imagename=imagename, outfile=mom0_file, excludepix=[-100, 0.00022893], moments=[0])

viewer('G330.954-0.182-1665.40184MHz.clean.contsub.velocity.image')
mom0_file='G330.954-0.182-1665.40184MHz.clean.contsub.velocity.mom0'
imagename='G330.954-0.182-1665.40184MHz.clean.contsub.velocity.image'
immoments(imagename=imagename, outfile=mom0_file, excludepix=[-100, 0.00022893], moments=[0])

run get-spectrum.py
```

-fin-
