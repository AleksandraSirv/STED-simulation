import configparser
import os

def read_config_file():
    """
    Reads the configuration file using configparser and returns a 
    dictionary of parameters if they are within defined limits.
    Description of parameters:
    - lambda_exc: Excitation wavelength in nm (400–700)
    - lambda_sted: STED wavelength in nm (must be > λ_exc, typically 700–850)
    - NA: Numerical aperture (0.5–1.49)
    - I_s: Saturation intensity (normalized) (0.1–5.0)
    - I0_sted: STED beam peak intensity (normalized) (0–100)
    - grid_size: Simulation grid resolution (256–1000)
    - extent_nm: Physical extent of the field in nm (500–2000)
    """
    # Initialize configparser and read the file
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.txt'))
    # Extract the parameters from the config file
    params = {}
    try:
        params["lambda_exc"] = float(config.get('settings', 'lambda_exc'))
        params["lambda_sted"] = float(config.get('settings', 'lambda_sted'))
        params["NA"] = float(config.get('settings', 'NA'))
        params["I_s"] = float(config.get('settings', 'I_s'))
        params["I0_sted"] = float(config.get('settings', 'I0_sted'))
        params["grid_size"] = int(config.get('settings', 'grid_size'))
        params["extent_nm"] = int(config.get('settings', 'extent_nm'))
    except (configparser.NoOptionError, ValueError) as e:
        print(f"Error reading configuration: {e}")
        return None

    # Validate the parameters
    validate_parameters(params)

    return params

def validate_parameters(params):
    """
    Function validates the parameters read from config file by checking wether
    they are within the accepted limits.
    """
    if not (400 <= params["lambda_exc"] <= 700):
        raise ValueError(f"Invalid lambda_exc value: {params['lambda_exc']} (Expected: 400–700 nm)")
    if not (710 <= params["lambda_sted"] <= 850):
        raise ValueError(f"Invalid lambda_sted value: {params['lambda_sted']} (Expected: 710–850 nm)")
    if not (0.5 <= params["NA"] <= 1.49):
        raise ValueError(f"Invalid NA value: {params['NA']} (Expected: 0.5–1.49)")
    if not (0.1 <= params["I_s"] <= 5.0):
        raise ValueError(f"Invalid I_s value: {params['I_s']} (Expected: 0.1–5.0)")
    if not (0 <= params["I0_sted"] <= 100):
        raise ValueError(f"Invalid I0_sted value: {params['I0_sted']} (Expected: 0–100)")
    if not (256 <= params["grid_size"] <= 1000):
        raise ValueError(f"Invalid grid_size value: {params['grid_size']} (Expected: 256–1000)")
    if not (500 <= params["extent_nm"] <= 2000):
        raise ValueError(f"Invalid extent_nm value: {params['extent_nm']} (Expected: 500–2000)")

if __name__ == "__main__":
    # Load parameters from the config file and validate
    params = read_config_file()

    if params:
        print("Loaded parameters:")
        for key, value in params.items():
            print(f"{key}: {value}")