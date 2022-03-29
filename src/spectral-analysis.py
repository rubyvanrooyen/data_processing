"""
    Recipe for CASA pipeline processing of MeerKAT maser zoom mode data
"""

import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

import numpy as np
import matplotlib.pylab as plt


## -- CARACal --
# Assume some preprocessing using CARACal has already been done.
# Calibration
# Inspection of calibration solutions
# Dynamic range estimation for calibrator selfcal images
# Apply calibration to target data
# Split out calibrated target visibilities
msfile='1625501782_sdp_l0-G330_89_0_36-corr.ms'
prefix='1625501782_sdp_l0-G330_89_0_36'
target='G330.89-0.36'
## -- CARACal --


## -- CASA --
# Flagging before imaging/analysis
# Run plotms on the data, run through different perspectives and make sure there aren't any crazy outliers or low-level RFI now showing up in the data. You will kick yourself if some RFI messes up your continuum subtraction. 

# Theoretical line and continuum point source sensitivity
def calc_pss(msfile,  # calibrated target visibilities
             T_eta=20.,  # [K]  MeerKAT Tsys/Eta @ 1.4GHz
             ):
    """Noise calculation using measured Tsys/Eta_ap from tipping curves"""

    k = 1.38e-23  # Boltzmann's constant
    Jy = 1e-26  # Jansky conversion factor

    tb.open(msfile+'/ANTENNA')
    N = len(tb.getcol('NAME')) 
    D = tb.getcol('DISH_DIAMETER')[0]
    A = np.pi*(D/2.)**2
    tb.close()

    tb.open(msfile+'/SPECTRAL_WINDOW')
    # channel increments or bandwidth can end up being negative after
    # conversion to velocity space with cvel
    dv = np.absolute(tb.getcol('TOTAL_BANDWIDTH')[0])
    Nchan = tb.getcol('NUM_CHAN')[0]
    dv_per_chan = np.absolute(tb.getcol('CHAN_WIDTH')[0])
    tb.close()

    # Total Integration Time
    tb.open(msfile)
    Nints = len(pl.unique(tb.getcol('TIME')))
    dt = tb.getcol('EXPOSURE')[0]
    T = Nints * dt
    tb.close()

    # RMS noise (sensitivity calculations)
    # pss_N = np.sqrt(2)*Tsys*k
    # pss_D = eff * A * np.sqrt(N*(N-1)*dv*T)
    pss_N = np.sqrt(2) * T_eta * k
    pss_D = A * np.sqrt(N*(N-1) * dv * T)
    pss = pss_N / pss_D
    # pss_D_per_chan = eff * A * np.sqrt(N*(N-1)*dv_per_chan*T)
    pss_D_per_chan = A * np.sqrt(N*(N-1) * dv_per_chan * T)
    pss_per_chan = pss_N / pss_D_per_chan

    print("\n")
    print("\n")
    print("Point Source Sensitivity Parameters")
    print("-----------------------------------")
    print("Total Integration Time [s] = "+str(T))
    print("Total Bandwidth [Hz] = "+str(dv))
    print("Number of Channels = "+str(Nchan))
    print("Number of Antennas = "+str(N))
    print("Approximate Dish Area [m^2] = "+str(A))
    print("User Input(Tsys/eta [K] = "+str(T_eta))
    print("\n")
    print("Point Source Sensitivity [Jy] = "+str(pss/Jy))
    print("Point Source Sensitivity per channel [Jy] = "+str(pss_per_chan[0]/Jy))

    return pps_per_chan[0]/Jy


# Regrid and set measurement frame
def split_vlsr(restfreq,  # Hz
               outframe='LSRK',
               ):
    # Set MS rest frequency
    freq_string=str(restfreq/1e6)+'MHz'
    split_outputvis = prefix + '-' + freq_string + '.ms'
    if os.access(split_outputvis, F_OK):
        os.system('rm -rf ' + split_outputvis)
    split(vis=msfile,
          outputvis=split_outputvis,
          datacolumn='all')

    tb.open(split_outputvis+'/SPECTRAL_WINDOW')
    orig_ref_freq = tb.getcol('REF_FREQUENCY')
    tb.close()
    tb.open(split_outputvis + '/SPECTRAL_WINDOW', nomodify=False)
    tb.putcell('REF_FREQUENCY', 0, restfreq)
    tb.close()
    tb.open(split_outputvis+'/SPECTRAL_WINDOW')
    set_ref_freq = tb.getcol('REF_FREQUENCY')
    tb.close()
    print(f'Set MS rest frequency from {orig_ref_freq} to {set_ref_freq}'

    # regrid to another measurement frame and Doppler correction
    cvel_outputvis = prefix + '-' + freq_string + '.cvel.ms'
    if os.access(cvel_outputvis, F_OK):
        os.system('rm -rf ' + cvel_outputvis)
    cvel(vis=split_outputvis,
         outputvis=cvel_outputvis,
         mode='velocity',
         interpolation='linear',
         outframe=outframe,
         restfreq=freq_string)
    # Flag with uv-clip
    flagdata(vis=cvel_outputvis, mode='clip', clipminmax=[1e-5, 1000.0])

    # remove intermediate dataset
    os.system('rm -rf ' + split_outputvis)

    return cvel_outputvis


# Continuum subtraction
def cont_sub(msfile,
             cont_window,
             imsize=8192,
             cellsize='1.5arcsec',
             mfs_namebase=None,
             ):
    # make a backup of the target MS before applying uvconstsub since it will do inline changes to the data
    os.system(f'tar -cvzf {msfile}.tgz {msfile}')

    # Make sure MS files that will be auto-generated are removed before cont subtraction
    cont_outputvis = msfile + '.cont'
    if os.access(cont_outputvis, F_OK):
        os.system('rm -rf ' + cont_outputvis)
    contsub_outputvis = msfile + '.contsub'
    if os.access(contsub_outputvis, F_OK):
        os.system('rm -rf ' + contsub_outputvis)

    # Do continuum subtraction
    uvcontsub(vis=msfile,
              fitspw=cont_window,
              fitorder=1,
              want_cont=True)

    if mfs_namebase is not None:
        # Make a dirty image of the selected line free channels and make sure it is noise like. Examining whether the continuum subtraction worked well or not.
        dirty_namebase = mfs_namebase + '.dirty.mfs.noise'
        os.system('rm -rf ' + dirty_namebase + '.*')
        clean(vis=msfile,
              imagename=dirty_namebase,
              spw=cont_window,
        #       outframe='LSRK',
        #       restfreq=freq_string,
              imsize=imsize,
              cell=cellsize,
              multiscale=[],
              mode='mfs',
              weighting='briggs',
              robust=0.,
              threshold='0.0Jy',
              gain=0.85,
              psfmode='clark',
              stokes='I',
              niter=0)

        # Make a clean image from continuum MS
        image_namebase = mfs_namebase + '.clean.cont.mfs'
        os.system('rm -rf ' + image_namebase + '.*')
        clean(vis=cont_outputvis,
              imagename=image_namebase,
        #       outframe='LSRK',
        #       restfreq=freq_string,
              mode='mfs',
              multiscale=[],
              negcomponent=1,
        #       mask=cont_mask,
        #       spw=cont_window,
              imsize=imsize,
              cell=cellsize,
              stokes='I',
              threshold='0.0Jy',
              niter=500,
              gain=0.85,
              psfmode='hogbom',
              interactive=False,
              weighting='briggs',
              robust=0.)

    return contsub_outputvis


# Create data cubes and make moment 0 map
def make_cubes(msfile,
               cube_namebase,
               restfreq,
               cont_window,
               imsize=8192,
               cellsize='1.5arcsec',
               outframe='LSRK',
               **kwargs):

    # Dirty cube of emission free channels to estimate the RMS noise.
    dirty_namebase = cube_namebase + '.dirty.contsub.noise'
    os.system('rm -rf ' + dirty_namebase + '.*')

    freq_str = str(restfreq/1e6)+'MHz',
    clean(vis=msfile,
          imagename=dirty_namebase,
          spw=cont_window,
          mode='channel',
          start=1,
          nchan=1,
          outframe=outframe,
          restfreq=freq_str,
          imsize=imsize,
          cell=cellsize,
          stokes='I',
          niter=0)

    noise_stat = imstat(imagename=dirty_namebase + '.image')
    rms = noise_stat['rms'][0]
    threshold = str(rms) + 'Jy'
    print(f'Making clean cube down to a threshold of {threshold}')
    # remove intermediate dataset
    os.system('rm -rf ' + dirty_namebase + '.*')

    # Make a clean cube to extract spectra
    clean_namebase = cube_namebase + '.clean.contsub.velocity'
    os.system('rm -rf ' + clean_namebase + '.*')

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
          threshold=threshold,
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
    os.system('rm -rf ' + mom0_file)

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


## -- Spectral line algo --
# Calculate expected thermal noise
# Note the theoretical RMS noise of this observation for the continuum assuming Tsys/Eta=21.5K, total integration time and bandwidth.
snr = calc_pss(target_ms, T_eta=21.5)  # Jy
# The threshold is set to three times the RMS noise in an emission free channel.
threshold = ' '.join([str(3*snr), 'Jy'])
print('Set clean threshold = {}'.format(threshold))

# OH maser lines – The full rest frequency as a floating point number
maser_lines = [1665.40184e6, 1667.35903e6]  # Hz
cont_windows = ['*:1655.64MHz~1664.06MHz;1668.75MHz~1674.56MHz', None]
masers = ["G330.878-0.367", "G330.954-0.182", "G331.132-0.244", "G331.278-0.188", "G331.442-0.186"]
masks = [[4100,4100], [4269,4549], [3856,4731], [3687,5067], [3403,5337]]
directions = ["J2000 16h10m20.01 -52d06m07.7", "J2000 16h09m52.60 -51d54m53.7", "J2000 16h10m59.72 -51d50m22.7", "J2000 16h11m26.57 -51d41m56.5", "J2000 16h12m12.41 -51d35m09.5"]

for restfreq, cont_window in zip(maser_lines, cont_windows):
    cvel_msfile = split_vlsr(rest_freq)  # Doppler corrected MS

    if cont_window is None:
        # Identify these channels and ranges using plotms to plot channel vs amplitude
        quit()  # exit pipeline and run rest manually once cont region is known
    # After identifying line free channels, subtract the continuum 
    mfs_namebase = target + '-' + freq_string
    contsub_msfile = cont_sub(cvel_msfile, cont_window, mfs_namebase=mfs_namebase)

    for maser, maskcenter, phasecenter in zip(masers, masks, directions):
        print("\n")
        print(f"Processing {maser}")

        cube_namebase = maser + '-' + freq_string
        delta = np.array([80,80])
        centre = np.array(maskcenter)
        box_mask=[centre[0]-delta[0]/2, centre[1]-delta[1]/2,
                  centre[0]+delta[0]/2, centre[1]+delta[1]/2]
        [cleancube_msfile,
         mom0_file] = make_cubes(contsub_msfile,
                                 cube_namebase,
                                 restfreq,
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
                     spectrum_basename,
                     )
        

## -- Spectral line algo --
## -- CASA --

# -fin-
