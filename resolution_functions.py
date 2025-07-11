import numpy as np 
# ------------------------
# FULL WIDTH AT HALF MAXIMUM
# ------------------------
def fwhm(psf):
    """
    Function that calculates the FWHM of a Point Spread Function (PSF).

    Input parameters:
        psf : 2D NumPy array
            The PSF intensity distribution.

    Output:
        float
        FWHM along one axis (in pixels or spatial units, depending on the grid).

    """    
    psf_max = np.max(psf)
    half_max = psf_max / 2
    # Find where the PSF drops to half-max
    indices = np.where(psf >= half_max)
    fwhm = np.max(indices[0]) - np.min(indices[0])  # FWHM along one axis
    return fwhm

# ------------------------
# DIFFRACTION-LIMITED RESOLUTION (using wavelength)
# ------------------------

def diffraction_limit(wavelength, NA):
    """    
    Function to calculate the diffraction-limited resolution (beam waist) 
    based on the wavelength and numerical aperture (NA) of the system.

    The diffraction limit defines the smallest resolvable detail based on 
    the properties of the optical system, such as the wavelength of light 
    and the numerical aperture of the lens.

    Parameters:
        wavelength : float
            The wavelength of light used in the system (in nanometers, nm).
        NA : float
            The numerical aperture of the optical system 
            (dimensionless, typically between 0.5 and 1.49).

    Output:
        float
            The diffraction-limited resolution, in nanometers (nm).
    """
    return wavelength / (2 * NA)
