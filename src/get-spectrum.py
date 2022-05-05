# import os
# from os import F_OK

from tasks import *
from taskinit import *
import casac

import numpy as np
import matplotlib.pylab as plt

# DEBUG=False

#     # Make a clean cube to extract spectra
#     clean_namebase = cube_namebase + '.clean.contsub.velocity'

# Extract spectrum
#def get_spectrum(image_file, mom0_file, spectrum_basename):
# def get_spectrum(spectrum_basename, xloc=None, yloc=None):
def get_spectrum(spectrum_basename, region):
    print(spectrum_basename)
    image_file = spectrum_basename + '.clean.contsub.velocity.image'
    print(image_file)
    mom0_file = spectrum_basename + '.clean.contsub.velocity.mom0'
    print(mom0_file)
    mom0_stat = imstat(mom0_file, region=region)
    x2extract = mom0_stat['maxpos'][0]
    y2extract = mom0_stat['maxpos'][1]
    print(x2extract, y2extract)
    extractBox = "%d,%d" % (x2extract, y2extract) # copy the position to a string
    print(extractBox)
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
    spectrum = cubeSpec['data']
    # First, combine the spectrum into a single array
    outputspectrum = np.vstack((velocity, cubeSpec['data']))
    spec_file = spectrum_basename + '-spectrum.txt'
    np.savetxt(spec_file, np.transpose(outputspectrum))

    plt.figure()
    plt.plot(velocity, cubeSpec['data'], 'k-')
    plt.xlabel(r"$V_{lsr}$ (km s$^{-1}$)",fontsize=16) 
    plt.ylabel(r"$S_{\nu}$ (Jy)",fontsize=16)
    plt.title(spectrum_basename)
    im_file = spectrum_basename + '-spectrum.png'
    plt.savefig(im_file)


## Main section, doing the masers individually and explicitly
restfreq = 1665.40184e6  # Hz
cont_window = '*:1655.64MHz~1664.06MHz;1668.75MHz~1674.56MHz'
# contsub_msfile='1625501782_sdp_l0-G330_89_0_36-corr-1665.40184MHz.cvel.ms.contsub'
contsub_msfile='1625501782_sdp_l0-G330_89_0_36-corr-1665.40184MHz-split.cvel.ms.contsub'
# Set MS rest frequency
freq_string=str(restfreq/1e6)+'MHz'
rms = 0.00022893

maser = "G330.878-0.367"
maskcenter = [4100,4100]
phasecenter = "J2000 16h10m20.01 -52d06m07.7"
print("\n")
print("Processing {}, in box {}: {}".format(maser, maskcenter, phasecenter))
cube_namebase = maser + '-' + freq_string
delta = np.array([80,80])
centre = np.array(maskcenter)
box_mask=[centre[0]-delta[0]/2, centre[1]-delta[1]/2,
          centre[0]+delta[0]/2, centre[1]+delta[1]/2]
region = 'box [ [ {}pix , {}pix] , [{}pix, {}pix ] ]'.format(box_mask[0], box_mask[1], box_mask[2], box_mask[3])
spectrum_basename= maser + '-' + freq_string
get_spectrum(spectrum_basename, region)


maser = "G330.954-0.182"
maskcenter = [4269,4549]
phasecenter = "J2000 16h09m52.60 -51d54m53.7"
print("\n")
print("Processing {}, in box {}: {}".format(maser, maskcenter, phasecenter))
cube_namebase = maser + '-' + freq_string
delta = np.array([80,80])
centre = np.array(maskcenter)
box_mask=[centre[0]-delta[0]/2, centre[1]-delta[1]/2,
          centre[0]+delta[0]/2, centre[1]+delta[1]/2]
region = 'box [ [ {}pix , {}pix] , [{}pix, {}pix ] ]'.format(box_mask[0], box_mask[1], box_mask[2], box_mask[3])
spectrum_basename= maser + '-' + freq_string
get_spectrum(spectrum_basename, region)


maser = "G331.132-0.244"
maskcenter = [3856,4731]
phasecenter = "J2000 16h10m59.72 -51d50m22.7"
print("\n")
print("Processing {}, in box {}: {}".format(maser, maskcenter, phasecenter))
cube_namebase = maser + '-' + freq_string
delta = np.array([80,80])
centre = np.array(maskcenter)
box_mask=[centre[0]-delta[0]/2, centre[1]-delta[1]/2,
          centre[0]+delta[0]/2, centre[1]+delta[1]/2]
region = 'box [ [ {}pix , {}pix] , [{}pix, {}pix ] ]'.format(box_mask[0], box_mask[1], box_mask[2], box_mask[3])
spectrum_basename= maser + '-' + freq_string
get_spectrum(spectrum_basename, region)


maser = "G331.278-0.188"
maskcenter = [3687,5067]
phasecenter = "J2000 16h11m26.57 -51d41m56.5"
print("\n")
print("Processing {}, in box {}: {}".format(maser, maskcenter, phasecenter))
cube_namebase = maser + '-' + freq_string
delta = np.array([80,80])
centre = np.array(maskcenter)
box_mask=[centre[0]-delta[0]/2, centre[1]-delta[1]/2,
          centre[0]+delta[0]/2, centre[1]+delta[1]/2]
region = 'box [ [ {}pix , {}pix] , [{}pix, {}pix ] ]'.format(box_mask[0], box_mask[1], box_mask[2], box_mask[3])
spectrum_basename= maser + '-' + freq_string
get_spectrum(spectrum_basename, region)


maser = "G331.442-0.186"
maskcenter = [3403,5337]
phasecenter = "J2000 16h12m12.41 -51d35m09.5"
print("\n")
print("Processing {}, in box {}: {}".format(maser, maskcenter, phasecenter))
cube_namebase = maser + '-' + freq_string
delta = np.array([80,80])
centre = np.array(maskcenter)
box_mask=[centre[0]-delta[0]/2, centre[1]-delta[1]/2,
          centre[0]+delta[0]/2, centre[1]+delta[1]/2]
region = 'box [ [ {}pix , {}pix] , [{}pix, {}pix ] ]'.format(box_mask[0], box_mask[1], box_mask[2], box_mask[3])
spectrum_basename= maser + '-' + freq_string
get_spectrum(spectrum_basename, region)


plt.show()


# -fin-
