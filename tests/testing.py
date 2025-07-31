from start import read_config_file
import numpy as np
import pytest
from start import validate_parameters
from psf_functions import gaussian_psf, laguerre_gaussian_donut, effective_psf
from resolution_functions import fwhm, diffraction_limit



def test_read_config_file__types():
    """
    Test that read_config_file() returns parameters of correct types.
    
    Parameters:
    # lambda_exc: Excitation wavelength in nm (400–700)
    # lambda_sted: STED wavelength in nm (must be > λ_exc, typically 710–850)
    # NA: Numerical aperture (0.5–1.49)
    # I_s: Saturation intensity (normalized) (0.1–5.0)
    # I0_sted: STED beam peak intensity (normalized) (0–100)
    # grid_size: Simulation grid resolution (256–1000)
    # extent_nm: Physical extent of the field in nm (500–2000)
    """

    params = read_config_file()
    assert isinstance(params, dict), "Expected params to be a dictionary"

    # Check types of each parameter
    assert isinstance(params["lambda_exc"], float), "lambda_exc should be float"
    assert isinstance(params["lambda_sted"], float), "lambda_sted should be float"
    assert isinstance(params["NA"], float), "NA should be float"
    assert isinstance(params["I_s"], float), "I_s should be float"
    assert isinstance(params["I0_sted"], float), "I0_sted should be float"
    assert isinstance(params["grid_size"], int), "grid_size should be int"
    assert isinstance(params["extent_nm"], int), "extent_nm should be int"
#-----------------------------------------------------------------------------
# TESTING INVALID PARAMETERS
#-----------------------------------------------------------------------------
# Utility function with correct parameters to avoid repetition
def valid_params():
    return {
        "lambda_exc": 650,
        "lambda_sted": 750,
        "NA": 1.3,
        "I_s": 2,
        "I0_sted": 25,
        "grid_size": 500,
        "extent_nm": 1000,
    }

def test_invalid_lambda_exc():
    """ 
    Test for invalid Excitation wavelength (lanbda_exc) value 
    (valid values are within the range of 400 nm – 700 nm)
    """
    params_too_low = {**valid_params(), "lambda_exc": 1}  # Too low
    params_too_high = {**valid_params(), "lambda_exc": 2000}  # Above limit
    
    with pytest.raises(ValueError, match="Invalid lambda_exc value"): 
        validate_parameters(params_too_low)
    with pytest.raises(ValueError, match="Invalid lambda_exc value"):
        validate_parameters(params_too_high)

def test_invalid_NA():
    """ 
    Test for invalid Numerical aperture (NA) value 
    (valid values are within the range of 0.5 – 1.49)
    """
    params_too_low = {**valid_params(), "NA": 0.4}  # Too low
    params_too_high = {**valid_params(), "NA": 1.6}  # Too high

    with pytest.raises(ValueError, match="Invalid NA value"):
        validate_parameters(params_too_low)
    with pytest.raises(ValueError, match="Invalid NA value"):
        validate_parameters(params_too_high)

def test_invalid_I_s():
    """ 
    Test for invalid Saturation intensity (normalized) (I_s) value 
    (valid values are within the range of 0.1 – 5.0)
    """
    params_too_low = {**valid_params(), "I_s": 0.05}  # Too low
    params_too_high = {**valid_params(), "I_s": 10}   # Too high

    with pytest.raises(ValueError, match="Invalid I_s value"):
        validate_parameters(params_too_low)
    with pytest.raises(ValueError, match="Invalid I_s value"):
        validate_parameters(params_too_high)

def test_invalid_I0():
    """ 
    Test for invalid STED beam peak intensity (normalized) (I0) value 
    (valid values are within the range of 0 – 100)
    """
    params_too_low = {**valid_params(), "I0_sted": -5} # Too low
    params_too_high = {**valid_params(), "I0_sted": 120} # Too high

    with pytest.raises(ValueError, match="Invalid I0_sted value"):
        validate_parameters(params_too_low)
    with pytest.raises(ValueError, match="Invalid I0_sted value"):
        validate_parameters(params_too_high)

def test_invalid_grid_size():
    """ 
    Test for invalid Simulation grid resolution (grid_size) value 
    (valid values are within the range of 256–1000)
    """
    params_too_low = {**valid_params(), "grid_size": 100} # Too low
    params_too_high = {**valid_params(), "grid_size": 1200} # Too high

    with pytest.raises(ValueError, match="Invalid grid_size value"):
        validate_parameters(params_too_low)
    with pytest.raises(ValueError, match="Invalid grid_size value"):
        validate_parameters(params_too_high)

def test_invalid_extent_nm():
    """ 
    Test for invalid Physical extent of the field in nm (extent_nm) value 
    (valid values are within the range of 500–2000)
    """
    params_too_low = {**valid_params(), "extent_nm": 200} # Too low
    params_too_high = {**valid_params(), "extent_nm": 3000} # Too high

    with pytest.raises(ValueError, match="Invalid extent_nm value"):
        validate_parameters(params_too_low)
    with pytest.raises(ValueError, match="Invalid extent_nm value"):
        validate_parameters(params_too_high)    
    
#-----------------------------------------------------------------------------
# TESTING PSF AND RESOLUTION FUNCTIONS
#-----------------------------------------------------------------------------
def test_psf_functions_types():
    """
    Test whether the PSF functions return arrays with correct shape and type.
    """
    # Simulation parameters from config
    params = read_config_file()
    N = params["grid_size"]
    extent = params["extent_nm"]
    lambda_exc = params["lambda_exc"]
    lambda_sted = params["lambda_sted"]
    NA = params["NA"]
    I_s = params["I_s"]
    I0_sted = params["I0_sted"]

    # Generate simulation grid
    xy = np.linspace(-extent/2, extent/2, N)
    x, y = np.meshgrid(xy, xy)

    # Compute beam waists
    w_exc = diffraction_limit(lambda_exc, NA)
    w_sted = diffraction_limit(lambda_sted, NA)

    # Run PSF calculations
    exc_psf = gaussian_psf(x, y, w_exc)
    sted_psf = laguerre_gaussian_donut(x, y, w_sted)
    eff_psf = effective_psf(exc_psf, sted_psf, I_s, I0_sted)

    # Testing types
    assert isinstance(exc_psf, np.ndarray), "Excitation PSF must be a NumPy array"
    assert isinstance(sted_psf, np.ndarray), "STED PSF must be a NumPy array"
    assert isinstance(eff_psf, np.ndarray), "Effective PSF must be a NumPy array"

    # Testing shapes
    assert exc_psf.shape == (N, N), f"Expected shape {(N, N)}, got {exc_psf.shape}"
    assert sted_psf.shape == (N, N), f"Expected shape {(N, N)}, got {sted_psf.shape}"
    assert eff_psf.shape == (N, N), f"Expected shape {(N, N)}, got {eff_psf.shape}"
    
    
def test_diffraction_limit_return():
    """
    Tests whether diffraction_limit() returns a float within expected range.
    """
    params = read_config_file()
    wavelength = params["lambda_exc"]
    NA = params["NA"]

    result = diffraction_limit(wavelength, NA)
    assert isinstance(result, float), "diffraction_limit should return a float"
    assert result > 0, "diffraction_limit should return a positive value"


def test_fwhm_return():
    """
    Tests whether fwhm() returns a float and behaves reasonably on a Gaussian PSF.
    """
    params = read_config_file()
    N = params["grid_size"]
    extent = params["extent_nm"]
    lambda_exc = params["lambda_exc"]
    NA = params["NA"]

    # Create 2D Gaussian PSF
    xy = np.linspace(-extent/2, extent/2, N)
    x, y = np.meshgrid(xy, xy)
    w_exc = diffraction_limit(lambda_exc, NA)
    psf = gaussian_psf(x, y, w_exc)

    result = fwhm(psf)
    assert isinstance(result, (int, float, np.integer, np.floating)), "FWHM must be a number"
    assert result > 0, "FWHM must be positive"
    assert result < N, "FWHM should be smaller than grid size"
    
def test_gaussian_psf_peak_and_symmetry():
    """ 
    Test for cheking that the 2D Gaussian PSF peaks at the center and is symmetric across 
    the x-axis.
    """
    w0 = 100  # Beam waist in [nm]
    xy = np.linspace(-500, 500, 1001)
    x, y = np.meshgrid(xy, xy)
    psf = gaussian_psf(x, y, w0)

    center = psf[500, 500]
    left = psf[500, 400]
    right = psf[500, 600]

    #Check wether the peak is at the center
    assert np.isclose(center,1.0), #Peak should be 1 at the center
    #Check symmetry
    assert np.isclose(left,rigth, rtol=1e-3) #Should be symmetric in x

def test_laguerre_psf_peak():
    """ 
    Test for cheking that the Laguerre-Gaussian (donut) PSF has zero intensity at the center 
    (dark spot) and nonzero intensity in a surrounding ring, confirming correct donut shape.
    """
    w = 100  # Beam waist in [nm]
    xy = np.linspace(-500, 500, 1001)
    x, y = np.meshgrid(xy, xy)
    psf = gaussian_psf(x, y, w)

    center = psf[500, 500]
    ring = psf[500, 400] #Has to be more than 0

    #Check wether the peak is 0
    assert np.isclose(center,0, atol=1e-6), #Peak should be 0 at the center
    #Check that we have a ring with onzero intensity
    assert ring>0
    
def test_gaussian_psf_mathematical_behaviour():
    """ 
    Test for cheking that the Gaussian PSF drops by 1/e from its peak at a distance equal to the 
    beam waist w0, validating the analytical form of the Gaussian function.
    - Peak at 1.0 at the center (r = 0)
    - Drop to approximately 1/e (~0.3679) at a radial distance r = w0
    """
    w0 = 100  # Beam waist in [nm]
    #Creating a small grid centered around (0,0) going up to r=w0.
    x = np.array([[-w0,0,w0]])
    y = np.array([[0,0,0]])
    psf = gaussian_psf(x, y, w0)
    center_val = psf[0, 1]  # intensity at x=0
    edge_val = psf[0, 0]    # intensity at x=-w0

    assert np.isclose(center_val,1.0,atol=1e-6), #Center should be 1
    assert np.isclose(edge_val, 1/np.e, atol=1e-3), #At r=w0, intensity shoud be close to 1/e
