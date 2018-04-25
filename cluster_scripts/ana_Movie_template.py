import matplotlib                                                                            
matplotlib.use('Agg')  

import sys,os
from sys import argv, stdout
from os.path import expanduser
from pathlib import Path

import numpy as np
from numpy import pi, e, cos, sin, sqrt
from numpy.random import randn
from os import path,walk
from scipy.optimize import leastsq
from scipy.signal import hilbert,cwt,ricker,lombscargle,welch,morlet,bartlett

from skimage import io 

#----------Import Wavelet Routines----------------
scriptpath = expanduser('~/WaveletMovies/cluster_scripts')
sys.path.append( scriptpath) # the sys.path!
from wavelet_ana_lib import *
#-------------------------------------------------

#---- to be overwritten by the prepare script----
dt = 10
Tmin = 100
Tmax = 220
nT = 100
#------------------------------------------------

wdir = os.getcwd()
print("Working in",wdir)

if len(sys.argv) < 2:
    print("No command line argument.. exiting")
    sys.exit(1)

p = Path(wdir)
movie_names = list( p.glob('input_*tif') )
if len(movie_names) == 0:
    print('Found no input movie.. exiting!')
    sys.exit(1)

print("Found {} input movies:".format(len(movie_names), wdir))
print(movie_names)

movie_name = movie_names[0].name # the roi movie file name

movie_path = os.path.join( wdir, movie_name )
print('Opening :', movie_name)
rm = io.imread(movie_path, plugin="tifffile")

#---------------------------------------------------------
periods = np.linspace(Tmin,Tmax,nT)
T_c = Tmax

NFrames, ydim, xdim = rm.shape
Npixels = ydim*xdim
# not working, Fiji can't read this :/
#wm = np.zeros( (*rm.shape,3),dtype = np.float32 ) # initialize empty array for output

period_movie = np.zeros( rm.shape,dtype = np.float32 ) # initialize empty array for output
phase_movie = np.zeros( rm.shape,dtype = np.float32 ) # initialize empty array for output
power_movie = np.zeros( rm.shape,dtype = np.float32 ) # initialize empty array for output

print( 'Computing the transforms for {} pixels'.format(Npixels) )
sys.stdout.flush()

# loop over pixel coordinates
for x in range(xdim):

    print("X:",x)
    sys.stdout.flush()

    for y in range(ydim):
        
        input_vec = rm[:,y,x] # the time_series at pixel (x,y)
        Nt = len(input_vec) # number of sample points
        dsignal = sinc_smooth(input_vec, T_c, dt, detrend = True)

        modulus, wlet = compute_spectrum(dsignal,dt , periods)
        ridge_y = get_maxRidge(modulus)

        # stdout format
        ridge_periods = periods[ridge_y]
        powers = modulus[ridge_y,np.arange(Nt)]
        phases = np.angle(wlet[ridge_y,np.arange(Nt)])

        phase_movie[:,y,x] = phases
        period_movie[:,y,x] = ridge_periods
        power_movie[:,y,x] = powers



        
print('done with the transformations')
# save phase movie
out_path1 = os.path.join(wdir, 'phase' + rm_name)
io.imsave(out_path1, phase_movie)
print('written',out_path1)

# save period movie
out_path2 = os.path.join(wdir, 'period' + rm_name)
io.imsave(out_path2, period_movie)
print('written',out_path2)

# save power movie
out_path3 = os.path.join(wdir, 'power' + rm_name)
io.imsave(out_path3, phase_movie)
print('written',out_path3)
