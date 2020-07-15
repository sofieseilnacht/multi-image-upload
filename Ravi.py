#!/usr/bin/env python
"""
Python 3.8
Attempt to detect SN in discovery images that have been 
processed with Astrometry.net into FITS files with WCS solutions
"""
from __future__ import division, print_function
from __future__ import absolute_import
import numpy as np
import os, sys
from astropy.table import Table, join
from astropy.io import fits
from astropy.wcs import WCS
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm, LogNorm
from matplotlib.patches import Ellipse
import sep
import argparse
import csv
from IPython import embed
from six.moves import range
plt.rc('font', family='serif')

############################### PARSE ARGUMENTS ###############################
parser = argparse.ArgumentParser(formatter_class=
                                 argparse.ArgumentDefaultsHelpFormatter,
    description='Detect SN in discovery image with SEP')
parser.add_argument('--SN', help='Supernova name')
parser.add_argument('--SNlogs', help='Directory where log files and job files are stored')
parser.add_argument('--SNdir', help='Directory where results files are stored')
parser.add_argument('--SNcoord', nargs=2, type=float,
                    help='Current SN RA DEC (space-sep.) in decimal degrees')
parser.add_argument('--jobid', help='Astrometry.net Job ID number')

args = parser.parse_args()
################################## FUNCTIONS ##################################

def nmad(x):
    """
    Compute normalized median absolute deviation of x
    """
    k = 1.4826 # normalization
    nmad = k * np.nanmedian(np.absolute(x - np.nanmedian(x)))
    return nmad

def get_dist(x, y, x0, y0):
    """
    Compute 2-D Pythagorean distance between 2 points
    """
    return np.sqrt(np.square(x - x0) + np.square(y - y0))

def sep_extract_stars(d, thresh, err, deblend_cont, w, SNcoords):
    """
    Run SEP extraction for stars with the given input parameters.
    Compute RA, Dec, etc. and output catalog sorted by distance from SN.
    SNcoords is current SN coordinates (SkyCoord object).
    """
    print('\tUsing deblend_cont={}'.format(deblend_cont))
    objex = sep.extract(d, thresh=thresh, err=err, deblend_cont=deblend_cont)
    obj = Table([objex['x'],objex['y'],objex['a'],objex['b'],objex['theta'],
                 objex['flag'],objex['flux'],objex['xpeak'],objex['ypeak']],
                names=['x','y','a','b','theta','flag','flux','xpeak','ypeak'])
    str_det = '\tSEP detected {} objects above threshold of {} times NMAD of {}'
    print(str_det.format(len(obj), thresh, err))
    # Add RA, Dec, arbitrary ID
    obj['RA'], obj['DEC'] = w.all_pix2world(obj['x'], obj['y'], 0)
    obj['peakRA'], obj['peakDEC'] = w.all_pix2world(obj['xpeak'], obj['ypeak'], 0)
    obj['SEPID'] = np.arange(len(obj)) + 1
    # Compute catalog object distance from SN in arcsec
    obj['dist_arcsec'] = SNcoords.separation(
        SkyCoord(obj['RA'],obj['DEC'], unit=u.deg)).to('arcsec')
    obj.sort('dist_arcsec')
    return obj

def writeOutputCsv(csvResultDict) :
    headers = sorted(csvResultDict.keys())
    dir = args.SNlogs
    if dir.endswith("/"):
        dir = dir[:-1]
    with open("{}/{}-{}newfits-results.csv".format(dir,args.jobid,args.jobid),"w") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=headers)
        writer.writeheader()
        writer.writerow(csvResultDict)

csvResultDict={}
###############################################################################
# Read in discovery image in FITS format with WCS solution from Astrometry.net
data, wcshead = fits.getdata(os.path.join(args.SNdir, '{}-{}new.fits'.format(
    args.jobid, args.jobid)), header=True)
# Convert int array into float array for SEP to read properly
data = np.array(data[0], dtype=np.float32)
print('\nShape of data array = ', data.shape)
csvResultDict['shape']=data.shape

# No need to do endian byte order swap for Astrometry.net output FITS files
try:
    #print(wcshead)
    w = WCS(wcshead, naxis=2)
except KeyError:
    wcshead['CTYPE3'] = '' # needed so that WCS will work
    w = WCS(wcshead, naxis=2)

# Search for pixel scale in header comments
pixscale = None
for i in wcshead['COMMENT']:
    if 'scale:' in i:
        pixscale = np.float(i.split()[1])
print('\nPixel scale for image = ', pixscale)
csvResultDict['pixscale'] = pixscale

# Get SN coordinates in image x, y (for plotting only)
xy = w.all_world2pix(args.SNcoord[0], args.SNcoord[1], 0)
SNx, SNy = float(xy[0]), float(xy[1])
SNcoords = SkyCoord(ra=args.SNcoord[0], dec=args.SNcoord[1], unit=u.degree)

# Detect supernova/stars that might lie on top of extended galaxy
back_box_size = int(round(8/pixscale)) # ~8"
print('Background box size =', back_box_size)
csvResultDict['back_box_size']=back_box_size

back_filt_size = 3 # 3 pix is default
bkg = sep.Background(data, bw=back_box_size, bh=back_box_size,
                     fw=back_filt_size, fh=back_filt_size)
data_sub = data - bkg

deblend_cont = 0.05
thresh = 5
objex = sep_extract_stars(data_sub, thresh=thresh, err=nmad(data_sub), 
                          deblend_cont=deblend_cont, w=w, SNcoords=SNcoords)
objtab = Table(objex)
nearby = objtab['dist_arcsec'] < 30 # all objects within 30 arcsec
print(objtab['x','y','a','b','flag','flux','dist_arcsec'][nearby])
#csvResultDict['x']= objtab['x'][nearby]
objtab.write('{}/{}_SEP_newfits_cat.txt'.format(args.SNdir,args.SN),
             format='ascii.fixed_width', delimiter=None, overwrite=True)

# Plot
fig, ax = plt.subplots()
# origin='upper' needed to orient N up, E left for Astrometry.net FITS files
# norm adjusts the scaling of the image
ax.imshow(data, interpolation='none', cmap='gray', origin='upper',
          aspect='equal', norm=PowerNorm(0.036*nmad(data)+0.28)) 
for i in range(len(objtab)):
    color = 'magenta' if i==0 else 'dodgerblue'
    f = Ellipse(xy=(objtab['x'][i], objtab['y'][i]),
                width=2*3*(objtab['a'][i]), height=2*3*(objtab['b'][i]),
                angle=np.degrees(objtab['theta'][i]), lw=0.8,
                edgecolor=color, facecolor='none')
    ax.add_artist(f)
ax.plot(SNx, SNy, 's', color='lime', markersize=10, mfc='None')
ax.set_xlabel('x [pixels]')
ax.set_ylabel('y [pixels]')
fig.tight_layout()
#plt.show()
fig.savefig('{}/{}_SEP_newfits.pdf'.format(args.SNdir,args.SN))

print('\n\nExisting SN coordinates =\t', args.SNcoord[0], args.SNcoord[1])
csvResultDict['SN coord[0]']=args.SNcoord[0]
csvResultDict['SN coord[1]']=args.SNcoord[1]
print('Closest object coordinates =\t', objtab['RA'][0], objtab['DEC'][0])
csvResultDict['RA'] = objtab['RA'][0]
csvResultDict['DEC'] = objtab['DEC'][0]
print('Closest object peak coordinates =\t', objtab['peakRA'][0], objtab['peakDEC'][0])
csvResultDict['peakRA'] = objtab['peakRA'][0]
csvResultDict['peakDEC'] = objtab['peakDEC'][0]
print('Separation from barycenter (arcsec) =', objtab['dist_arcsec'][0])
csvResultDict['dist_arcsec'] = objtab['dist_arcsec'][0]
print('Separation from peak pixel (arcsec) =', SNcoords.separation(
    SkyCoord(objtab['peakRA'][0], objtab['peakDEC'][0], unit=u.deg)).to('arcsec'))
csvResultDict['arcsec'] = SNcoords.separation(
    SkyCoord(objtab['peakRA'][0], objtab['peakDEC'][0], unit=u.deg)).to('arcsec')
writeOutputCsv(csvResultDict)