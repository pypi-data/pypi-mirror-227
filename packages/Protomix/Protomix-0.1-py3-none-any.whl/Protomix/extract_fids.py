import os
import numpy as np
import pandas as pd

def extract_fids(root_directory: str, acqus_df: pd.DataFrame) -> pd.DataFrame:
    # Check the type of root_directory
    assert isinstance(root_directory, str), "root_directory should be a string."
    
    # Check if root_directory exists and is a directory
    assert os.path.exists(root_directory) and os.path.isdir(root_directory), "root_directory should point to an existing directory."
    
    # Initialize lists to store fid data and sample names
    fid_files = []
    sample_names = []
    
    # Get paths of fid files using os.walk and list comprehension
    paths = [os.path.join(root, file) for root, _, files in os.walk(root_directory)
             for file in files if file == 'fid']
    
    # Check if paths list is not empty
    assert paths, "No 'fid' files found in the specified directory."
    
    for data_file in paths:
        sample_names.append(data_file.split(os.path.sep)[-3])
        
        # Read binary data directly into a numpy array
        binary_data = np.fromfile(data_file, dtype="int32")
        
        # Ensure that binary data is even-length
        assert len(binary_data) % 2 == 0, f"Unexpected data length in {data_file}."
        
        # Convert binary data to complex signal directly
        complex_signal = binary_data[::2] + 1j * binary_data[1::2]
        fid_files.append(complex_signal)

    # Calculate dwell time and time array once
    dwell_time = 1 / (float(acqus_df['$SW_h'][0]))
    number_of_points = len(fid_files[0])
    time = np.linspace(dwell_time, number_of_points * dwell_time, number_of_points)   

    # Create DataFrame with fid data and appropriate index and columns
    fid_df = pd.DataFrame(fid_files, index=sample_names, columns=time, dtype=np.complex128)
    
    return fid_df
