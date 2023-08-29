import pandas as pd
import numpy as np

def apodization(fid_df: pd.DataFrame , LB: float = 1, apodization_type: str = 'gaussian') -> pd.DataFrame:
    """
    Applies an apodization function to the rows of a DataFrame.
    
    Parameters:
    - fid_df (pd.DataFrame): A DataFrame where columns represent time and rows represent FID values.
    - LB (float, optional): Line broadening parameter. Defaults to 1.
    - apodization_type (str, optional): Type of apodization function. Can be 'gaussian' or 'exponential'. Defaults to 'gaussian'.
    
    Returns:
    - pd.DataFrame: A DataFrame with the same shape as fid_df but with apodized values.
    """
    
    # Assertive lines
    assert isinstance(fid_df, pd.DataFrame), "fid_df should be a pandas DataFrame."
    assert LB >= 0, "LB should be non-negative."
    assert apodization_type in ['gaussian', 'exponential'], "apodization_type should be either 'gaussian' or 'exponential'."
    
    time = fid_df.columns.astype(float)
    
    if apodization_type == 'gaussian':
        apod_func = np.exp(-0.5 * (LB * time)**2)
    else:  # Since there are only two options for apodization_type, no need for another elif check.
        apod_func = np.exp(-LB * time)
    
    # Vectorized operation
    apodized_df = fid_df.multiply(apod_func, axis=1)
    
    return apodized_df