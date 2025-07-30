import matplotlib.pyplot as plt
import os

def plot_results(exc_psf, sted_donut, eff_psf, lambda_exc, lambda_sted, fwhm_exc, fwhm_eff, extent_nm):
    """
    Function that generates and displays plots for the PSFs (Excitation, 
    STED Donut, and Effective PSF) and the resolution comparison between the 
    classic confocal and STED methods.

    Input parameters:
        - exc_psf : numpy.ndarray
            The excitation PSF (normalized).
        - sted_donut: numpy.ndarray 
            The STED donut beam PSF (normalized).
        - eff_psf : numpy.ndarray
            The effective PSF (normalized) after STED depletion.
        - lambda_exc: float 
            The excitation wavelength (nm).
        - lambda_sted: float 
            The STED wavelength (nm).
        - fwhm_exc : float 
            The Full Width at Half Maximum (FWHM) of the excitation PSF (nm).
        - fwhm_eff : float 
            The Full Width at Half Maximum (FWHM) of the effective PSF (nm).
        - extent_nm : float 
            The extent of the grid in nm (used for axis scaling of the plots).

    Output:
        - Displays multiple plots:
          1. Three subplots showing the Excitation PSF, STED Donut Beam, 
              and Effective PSF.
          2. A plot comparing the FWHM values of the classic confocal 
             method vs. STED.
    """
    # Plot the PSFs
    fig, axes = plt.subplots(1, 3, figsize=(12, 3)) # defining subplot
    extent = [-extent_nm / 2, extent_nm / 2, -extent_nm / 2, extent_nm / 2]
    
    output_dir = os.path.join(os.path.dirname(__file__), "Output")
    os.makedirs(output_dir, exist_ok=True)  # Safe in case main didn't run
    
    # Plot Excitation PSF
    axes[0].imshow(exc_psf, extent=extent, cmap='viridis')
    axes[0].set_title(f"Excitation PSF ({lambda_exc} nm)")
    axes[0].set_xlabel("nm")
    axes[0].set_ylabel("nm")

    # Plot STED Donut Beam
    axes[1].imshow(sted_donut, extent=extent, cmap='inferno')
    axes[1].set_title(f"STED Donut Beam ({lambda_sted} nm)")
    axes[1].set_xlabel("nm")
    axes[1].set_ylabel("nm")

    # Plot Effective PSF (STED Applied)
    axes[2].imshow(eff_psf, extent=extent, cmap='viridis')
    axes[2].set_title("Effective PSF (STED Applied)")
    axes[2].set_xlabel("nm")
    axes[2].set_ylabel("nm")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "PSF_comparison.png"), dpi=300)
    plt.close()

    # Plot FWHM comparison
    fig, ax = plt.subplots(figsize=(6, 4))

    # Plot resolution comparison between confocal and STED
    ax.plot(['Classic confocal', 'After STED'], [fwhm_exc, fwhm_eff], 'bo-', 
            label='Resolution Comparison')

    # Set labels and title
    ax.set_title("FWHM Comparison: Confocal vs STED")
    ax.set_xlabel("Method")
    ax.set_ylabel("FWHM (nm)")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "FWHM_comparison.png"), dpi=300)
    plt.close()
