# STED Microscopy PSF Simulation

This Python project simulates the point spread function (PSF) and resolution improvement in STimulated Emission Depletion (STED) microscopy. It allows the user to compare a conventional diffraction-limited excitation PSF to an effective PSF after applying a STED depletion beam, visualize the improvement, and compute approximate resolution metrics.

---

## Introduction: STED Microscopy

Conventional fluorescence microscopy is limited by the diffraction of light (Abbe Limit). STED microscopy overcomes this limit by using an additional doughnut-shaped depletion laser wavefield to selectively deplete fluorescence at the periphery of the excitation spot, effectively narrowing the point-spread function of the excitation to increase resolution beyond the diffraction limit.

In STED, a doughnut-shaped depletion beam forces excited fluorophores back to the ground state through stimulated emission, except at the very center. This produces a much smaller effective fluorescence spot and thus overcomes the diffraction limit. The final resolution depends on the STED beam intensity and fluorophore properties, reaching resolutions down to tens of nanometers and enabling detailed imaging of subcellular structures.

---

## Workflow

The simulation proceeds as follows:

1. **Parameter Setup**  
   The user defines simulation parameters in **_config.txt_** (excitation wavelength, STED wavelength, numerical aperture, intensities). These are loaded and validated using **_read_config_file()_** and **_validate_parameters()_** from **_start.py_**, ensuring only physically meaningful values are used.

2. **PSF Generation**  
   The excitation PSF is modeled as a Gaussian distribution using **_gaussian_psf()_**, representing a conventional diffraction-limited spot. The STED depletion beam is generated using **_laguerre_gaussian_donut()_**, which produces a central zero-intensity "doughnut" necessary for confinement.

3. **Effective PSF Calculation**  
   The effective PSF is calculated with **_effective_psf()_**, which combines the excitation and STED PSFs according to the principle of stimulated emission saturation. This step simulates how the STED beam constrains the final fluorescence region.

4. **Resolution Estimation and Visualization**  
   The simulation computes resolution metrics, such as the full width at half maximum (FWHM), using **_diffraction_limit()_** and **_fwhm()_** from **_resolution_functions.py_**. Finally, **_main.py_** visualizes the excitation PSF, the STED beam, and the resulting effective PSF side by side to clearly illustrate resolution improvement and compare the FWHM.

Through this workflow, the project provides an intuitive and quantitative way to understand the resolution enhancement achievable by STED microscopy.

---

## Project Structure

The project is divided into many parts:

- **_config.txt_**  
  Configuration file containing key simulation parameters. Users specify the excitation and STED wavelengths (in nm), numerical aperture (NA), saturation intensity (**I_s**), peak STED beam intensity (**I0_sted**), simulation grid size, and physical field extent (in nm). This allows for easy parameter tuning without modifying the code.

- **_start.py_**  
  Contains utility functions to read and validate simulation parameters from the config file.  
  - **_read_config_file()_** reads parameters and converts them into appropriate types.  
  - **_validate_parameters()_** checks that all parameters fall within physically meaningful and safe ranges, raising descriptive errors if invalid.

- **_resolution_functions.py_**  
  Provides functions related to optical resolution:  
  - **_diffraction_limit(wavelength, NA)_** calculates the theoretical diffraction-limited beam waist based on wavelength and numerical aperture.  
  - **_fwhm(psf)_** computes the full width at half maximum (FWHM) of a given point spread function array, used to estimate resolution numerically.

- **_psf_functions.py_**  
  Implements point spread function calculations:  
  - **_gaussian_psf(x, y, w0)_** models the excitation PSF as a Gaussian distribution.  
  - **_laguerre_gaussian_donut(x, y, w0)_** models the STED depletion beam as a Laguerre-Gaussian donut shape, which creates a zero-intensity center.  
  - **_effective_psf(exc_psf, sted_psf, I_s, I0_sted)_** combines the excitation and STED PSFs using saturation principles to simulate the effective fluorescence emission region after depletion.

- **_testing.py_**  
  Contains comprehensive unit tests using pytest to ensure the correctness of parameter reading, validation, PSF generation, and resolution metrics:  
  - Tests for valid and invalid parameter ranges (wavelengths, NA, intensities).  
  - Tests for return types and shapes of PSFs.  
  - Tests for correct computation of diffraction limit and FWHM.

- **_main.py_**  
  Main entry point of the simulation:  
  - Reads and validates configuration parameters.  
  - Sets up a spatial grid based on user-defined extent and grid size.  
  - Calculates the excitation PSF, STED PSF, and final effective PSF.  
  - Computes resolution estimates (e.g., **_fwhm()_**).  
  - Generates visualizations comparing the excitation, STED, and effective PSFs side by side to illustrate resolution improvement.

---

## Usage

1. **Edit _config.txt_ carefully**

   - Open **_config.txt_** and provide your simulation parameters in the following format (one per line):

     ```
     lambda_exc = 650
     lambda_sted = 750
     NA = 1.3
     I_s = 2
     I0_sted = 25
     grid_size = 500
     extent_nm = 1000
     ```

   - **Important:** Make sure all parameter values stay within their valid physical ranges:
     - **lambda_exc**: 400 – 700 nm (Excitation wavelength).
     - **lambda_sted**: must be greater than **lambda_exc**, typically 710 – 850 nm.
     - **NA**: 0.5 – 1.49 (Numerical aperture of your objective lens).
     - **I_s**: 0.1 – 5.0 (Normalized saturation intensity).
     - **I0_sted**: 0 – 100 (Normalized STED beam peak intensity).
     - **grid_size**: 256 – 1000 (Number of pixels per dimension in the simulation grid).
     - **extent_nm**: 500 – 2000 nm (Physical size of the simulation field).

   - If any parameter falls outside these ranges, the program will raise a **_ValueError_** to prevent invalid or non-physical simulations.

2. **Run the main simulation**

   - Execute the main script to generate and visualize the PSFs:    **_python main.py_**
   - The script will read and validate your **_config.txt_**, compute the excitation PSF, STED depletion beam, and the resulting effective PSF, and display plots for visual comparison. It relies on functions like **_gaussian_psf()_**, **_laguerre_gaussian_donut()_**, and **_effective_psf()_** from **_psf_functions.py_**.



---

## Output

Output plots are created with the **_matplotlib_** library, and two functions are dedicated to producing visual results of the simulation.

Output files are saved automatically in the working directory as:

- **_PSF_comparison.png_** showing the excitation PSF, STED depletion beam, and effective PSF side by side.

- **_FWHM_comparison.png_**  displaying a FWHM comparison of the excitation and effective PSFs.

Moreover, the estimated effective PSF resolution calculated using **_fwhm()_** is printed to the console for quantitative evaluation.

**Note:** Running the simulation again will overwrite existing output images. To preserve previous results, rename or move them before re-running.  

---
## Example Output

Below are example images generated by the simulation:

### Excitation, STED, and Effective PSFs
<img width="3600" height="900" alt="PSF_comparison" src="https://github.com/user-attachments/assets/38d2fde6-f4b0-430a-8511-1769d840e0af" />


### FWHM Comparison
<img width="300" height="3000" alt="FWHM_comparison" src="https://github.com/user-attachments/assets/4e5ec489-6fbd-4ae3-8364-2c64e80aade0" />

---
## Requirements

- **Python 3.7 or higher**

- **_numpy_**  
  Used for numerical computations and array manipulations.

- **_matplotlib_**  
  Required for generating plots and visualizations of the PSFs.

- **_pytest_** (optional)  
  Needed to run the unit tests provided in the project.

---
## References
[1] S. P. Price and M. W. Davidson, STED Concept, Zeiss Campus Tutorials. Retrieved July 2025, from https://zeiss-campus.magnet.fsu.edu/tutorials/superresolution/stedconcept/indexflash.html

[2] T. Müller, C. Schumann, A. Kraegeloh, STED microscopy and its applications: new insights into cellular processes on the nanoscale, _ChemPhysChem_, 2012, **13**, 1986.
