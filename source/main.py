#Including libraries
import numpy as np
import os
import logging
from start import read_config_file
from psf_functions import gaussian_psf, laguerre_gaussian_donut, effective_psf
from resolution_functions import fwhm, diffraction_limit
from visual import plot_results
#-----------------------------------------------------------------------------
#SETTING UP LOGGING
#-----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)] %(message)s",
    handlers=[
        logging.FileHandler("log.txt")
        logging.StreamHandler()
    ]
)
logger=logging.getLogger(__name__),
logger.info("Information message")
#-----------------------------------------------------------------------------
#INITIALIZATION OF PARAMETERS
#-----------------------------------------------------------------------------
"""
Description of parameters:
    - lambda_exc: Excitation wavelength in nm (400–700)
    - lambda_sted: STED wavelength in nm (must be > λ_exc, typically 700–850)
    - NA: Numerical aperture (0.5–1.49)
    - I_s: Saturation intensity (normalized) (0.1–5.0)
    - I0_sted: STED beam peak intensity (normalized) (0–100)
    - grid_size: Simulation grid resolution (256–1000)
    - extent_nm: Physical extent of the field in nm (500–2000)
"""
params = read_config_file()  #Reads the config.txt and returns parameters

if params is None:
    raise ValueError("Error: Parameters could not be loaded. Check the configuration file.")
else:
    #-------------------------------------------------------------------------
    #DEFINING PARAMETERS
    #-------------------------------------------------------------------------
    lambda_exc = params["lambda_exc"]
    lambda_sted = params["lambda_sted"]
    NA = params["NA"]
    I_s = params["I_s"]
    I0_sted = params["I0_sted"]
    grid_size = params["grid_size"]
    extent_nm = params["extent_nm"]
    
    # ------------------------------------------------------------------------
    # GRID and POINT SPREAD FUNCTION (PSF) CONSTRUCTION
    # ------------------------------------------------------------------------
    
    # Set up the grid
    xy = np.linspace(-extent_nm/2, extent_nm/2, grid_size)
    x, y = np.meshgrid(xy, xy)
    r2 = x**2 + y**2

    # Calculate BEAM WAISTS Based on Wavelengths
    w_exc = diffraction_limit(lambda_exc, NA)  # Excitation beam waist (nm)
    w_sted = diffraction_limit(lambda_sted, NA)  # STED beam waist (nm)

    logger.info(f"Excitation Beam Waist (w0) = {w_exc:.2f} nm")
    logger.info(f"STED Beam Waist (w0) = {w_sted:.2f} nm")

    # Generate PSFs
    exc_psf = gaussian_psf(x, y, w_exc)
    sted_donut = laguerre_gaussian_donut(x, y, w_sted)
    eff_psf = effective_psf(exc_psf, sted_donut, I_s, I0_sted)

    # Normalize for plotting
    exc_psf /= exc_psf.max()
    sted_donut /= sted_donut.max()
    eff_psf /= eff_psf.max()

    # ------------------------------------------------------------------------
    # DATA ANALYSIS
    # ------------------------------------------------------------------------

    # Calculate Abbe diffraction limit
    abbe_resolution = diffraction_limit(lambda_exc, NA)
    
    # Calculate the Full Width at Half Maximum (FWHM) for Comparison
    fwhm_exc = fwhm(exc_psf)  # FWHM of excitation PSF
    fwhm_eff = fwhm(eff_psf)  # FWHM of effective PSF (after STED)
    try:  os.makedirs("Output")
    except FileExistsError:
        # directory already exists
        pass
        
    logger.info(f"Abbe Diffraction Limit: {abbe_resolution:.2f} nm")
    logger.info(f"Excitation Beam FWHM: {fwhm_exc:.2f} nm")
    logger.info(f"Effective FWHM (after STED): {fwhm_eff:.2f} nm")

    # ------------------------------------------------------------------------
    # PLOTTING RESULTS
    # ------------------------------------------------------------------------
    plot_results(exc_psf, sted_donut, eff_psf, lambda_exc, lambda_sted, 
                 fwhm_exc, fwhm_eff, extent_nm)
