import numpy as np

def gaussian_psf(x, y, w0):
    """
    Function that generates a 2D Gaussian point spread function (PSF).

    Input parameters:
        x, y : 2D NumPy arrays
            Meshgrid coordinate arrays representing spatial coordinates (nm).
        w0 : float
            Beam waist (radius at which the intensity drops by 1/e).

    Output:
        2D NumPy array representing intensity distribution of the Gaussian PSF.
    """
    return np.exp(-(x**2 + y**2) / w0**2)

def laguerre_gaussian_donut(x, y, w, m=1):
    """
    Function that generates a 2D Laguerre-Gaussian donut-shaped PSF.

    Input parameters:
        x, y : 2D NumPy arrays
            Meshgrid coordinate arrays representing spatial coordinates (nm).
        w : float
            Beam waist (radius at which the intensity drops by 1/e).
        m : int, optional
            Azimuthal mode index (default is 1). 
            Higher values increase the size of the central dark region.

    Output:
        2D NumPy array 
        Intensity distribution of the 2D Laguerre-Gaussian donut-shaped PSF.
    """
    r2 = x**2 + y**2
    return (r2 / w**2)**m * np.exp(-r2 / w**2)

def effective_psf(exc_psf, sted_psf, I_s, I0_sted):
    """
    Function that calculates the effective PSF after STED depletion is applied 
    to the excitation PSF.

    Input parameters:
        exc_psf : 2D NumPy array
            Excitation PSF intensity distribution.
        sted_psf : 2D NumPy array
            STED beam intensity distribution (e.g., Laguerre-Gaussian donut).
        I_s : float
            Saturation intensity (normalized).
        I0_sted : float
            Peak STED intensity (normalized).

    Output:
        2D NumPy array 
        Effective PSF after applying STED depletion.
    """    
    return exc_psf * np.exp(-I0_sted * sted_psf / I_s)
