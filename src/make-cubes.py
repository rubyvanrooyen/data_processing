import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

import numpy as np
import matplotlib.pylab as plt

# Create data cubes and make moment 0 map
def make_cubes(msfile,
               cube_namebase,
               freq_str,
               cont_window,
               imsize=8192,
               cellsize='1.5arcsec',
               outframe='LSRK',
               **kwargs):

    # Make a clean cube to extract spectra
    clean_namebase = cube_namebase + '.clean.contsub.velocity'
#     os.system('rm -rf ' + clean_namebase + '.*')
    if os.access(clean_namebase, F_OK):
        rmtables(clean_namebase + '.*')

    clean(vis=msfile,
          imagename=clean_namebase,
          mode='velocity',
          start=kwargs['start_vel'],
          nchan=kwargs['nchan'],
          width=kwargs['width'],
          interpolation='linear', 
          outframe=outframe,
          restfreq=freq_str,
          niter=10000,
          gain=0.85,  # 0.05
          threshold='3mJy',
          psfmode='clark',
          imsize=imsize,
          cell=cellsize,
          mask=kwargs['box_mask'],
          phasecenter=kwargs['phasecenter'],
          pbcor=False,
          interactive=False,
          usescratch=True,
          weighting='briggs',
          robust=0.) 

    # extract moment 0
    mom0_file = clean_namebase + '.mom0'
    if os.access(mom0_file, F_OK):
        rmtables(mom0_file)
#     os.system('rm -rf ' + mom0_file)

    immoments(imagename=clean_namebase + '.image',
              outfile=mom0_file,
              excludepix=[-100, rms],
              moments=[0])

    return clean_namebase, mom0_file


# Extract spectrum
def get_spectrum(image_file, mom0_file, spectrum_basename):
    mom0_stat = imstat(mom0_file)  #, region= region_file)
    x2extract = mom0_stat['maxpos'][0]
    y2extract = mom0_stat['maxpos'][1]
    extractBox = "%d,%d" % (x2extract, y2extract) # copy the position to a string
    cubeSpec = imval(image_file, box=extractBox, stokes='I')
    cubeStat = imstat(image_file)
    cubeHead = imhead(image_file, mode='list')
    nSpec = cubeStat['trc'][3] + 1 # get the number of frequency channels. 
    f0 = float(cubeHead['crval4']) # reference freq in Hz
    df = float(cubeHead['cdelt4']) # channel width in Hz
    i0 = cubeHead['crpix4'] # reference pixel
    freqSpec = (np.arange(nSpec) - i0)*df + f0
    fRest = cubeHead['restfreq'][0]
    velocity = 299792.458 * (1.0 - freqSpec/fRest) # radio convention, km/s

    # First, combine the spectrum into a single array
    spectrum = np.vstack((velocity, cubeSpec['data']))
    spec_file = spectrum_basename + '-spectrum.txt'
    np.savetxt(spec_file, np.transpose(spectrum))

    plt.figure()
    plt.plot(velocity, cubeSpec['data'], 'k-')
    plt.xlabel(r"$V_{lsr}$ (km s$^{-1}$)",fontsize=16) 
    plt.ylabel(r"$S_{\nu}$ (Jy)",fontsize=16)
    plt.title(spectrum_basename)
    im_file = spectrum_basename + '-spectrum.png'
    plt.savefig(imfile)

    rmtables(mom0_file)


restfreq = 1665.40184e6  # Hz
cont_window = '*:1655.64MHz~1664.06MHz;1668.75MHz~1674.56MHz'
masers = ["G330.878-0.367",
          "G330.954-0.182",
          "G331.132-0.244",
          "G331.278-0.188",
          "G331.442-0.186"]
masks = [[4100,4100],
         [4269,4549],
         [3856,4731],
         [3687,5067],
         [3403,5337]]
directions = ["J2000 16h10m20.01 -52d06m07.7",
              "J2000 16h09m52.60 -51d54m53.7",
              "J2000 16h10m59.72 -51d50m22.7",
              "J2000 16h11m26.57 -51d41m56.5",
              "J2000 16h12m12.41 -51d35m09.5"]

# Set MS rest frequency
freq_string=str(restfreq/1e6)+'MHz'
contsub_msfile='1625501782_sdp_l0-G330_89_0_36-corr-1665.40184MHz.cvel.ms.contsub'
for maser, maskcenter, phasecenter in zip(masers, masks, directions):
    print("\n")
    print("Processing {}, in box {}: {}".format(maser, maskcenter, phasecenter))

    cube_namebase = maser + '-' + freq_string
    delta = np.array([80,80])
    centre = np.array(maskcenter)
    box_mask=[centre[0]-delta[0]/2, centre[1]-delta[1]/2,
              centre[0]+delta[0]/2, centre[1]+delta[1]/2]

    [cleancube_msfile,
     mom0_file] = make_cubes(contsub_msfile,
                             cube_namebase,
                             freq_string,
                             cont_window,
                             outframe='LSRK',
                             start_vel='-150km/s',
                             nchan=319,
                             width='0.5km/s',
                             box_mask=box_mask,
                             phasecenter=phasecenter)

    spectrum_basename= maser + '-' + freq_string
    get_spectrum(cleancube_msfile+'.image',
                 mom0_file,
                 spectrum_basename)

# -fin-
