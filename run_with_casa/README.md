## Data and tables
Some processing and viewing of data being processed are still done using CASA for testing and
validation as well as to fill in gaps where CARACAL is still being developed.

This folder contains most of the symbolic links and output products for G330 commissioning processing.
G330 is used to build comparison reports between CASA and caracal processing


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

Full description of the commands and the mapping can be found in Google doc
[Caracal calibration implementation vs CASA](https://docs.google.com/document/d/1EObEOszSxN0apS4oGjNVWeoJOEyjHQrFzhQNSMWZ8Fs/edit?usp=sharing)

-fin-
