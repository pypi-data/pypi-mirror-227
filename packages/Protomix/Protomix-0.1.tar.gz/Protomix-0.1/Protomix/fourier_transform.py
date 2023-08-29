import numpy as np
import pandas as pd

def fourier_transform(fid_df: pd.DataFrame, acqus_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply Fourier Transform to FID (Free Induction Decay) signals in a DataFrame.

    Parameters:
    - df (pd.DataFrame): DataFrame containing FID signals in rows.
    - freq_nmr (float): NMR frequency in MHz (default: 600).
    - dwell_time (float): Time between data points in seconds (default: 1.0).
    - offset (float): Spectral offset in Hz (default: 0.0).

    Returns:
    - pd.DataFrame: DataFrame containing Fourier-transformed spectra with ppm as columns.

    The function takes a DataFrame containing rows of FID signals and applies the Fourier Transform
    to each row. It returns a DataFrame with Fourier-transformed spectra, where columns represent
    chemical shift values in ppm.
    """
    # Get the values from the DataFrame as a NumPy array
    fid_values = fid_df.values

    # Fourier transform the FIDs
    spectra = np.fft.fftshift(np.fft.fft(fid_values, axis=1), axes=1)

    # Create a frequency array corresponding to the Fourier transform
    num_points = fid_values.shape[1]
    dwell_time = 1 / (float(acqus_df['$SW_h'][0]))
    offset = float(acqus_df['$O1'][0])
    freq_nmr = float(acqus_df['$SFO1'][0])

    freq = np.fft.fftfreq(num_points, d=dwell_time)
    freq = np.fft.fftshift(freq + offset)

    # Convert the frequency to ppm using the NMR frequency
    ppm = freq / freq_nmr

    # Create a DataFrame from the spectra with ppm as the index
    result_df = pd.DataFrame(spectra, columns=ppm, index=fid_df.index)

    return result_df