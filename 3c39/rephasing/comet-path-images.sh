
#! /bin/bash


counter=0	
for msfile in `ls -d 1627186156_sdp_l0-67p-*-rephased.ms`
do
  imfile="comet67p.$counter.wsclean"
  counter=$((counter+1))

  wsclean -j 8 -name $imfile -size 8192 8192 -scale 1.5arcsec -niter 20000 -weight briggs 0.5 -threshold 0.0 -pol I -mgain 0.85 -padding 1.2 -auto-threshold 10 -auto-mask 15 -channels-out 8 -join-channels -fit-spectral-pol 4 $msfile

done

# - fin-
