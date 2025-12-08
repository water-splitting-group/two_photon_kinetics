import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 12
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

def find_nearest(array, values):
    array_1d = array if array.ndim == 1 else array[:,0]
    values = np.atleast_1d(values)
    hits = []
    for value in values:
        idx = np.searchsorted(array_1d, value, side="left")
        if idx > 0 and (idx == len(array_1d) or abs(value - array_1d[idx-1]) < abs(value - array_1d[idx])):
            hits.append(idx-1)
        else:
            hits.append(idx)
    return hits

def read_uvvis_data(filepath):
    # Read metadata
    metadata = {}
    headers = None
    units = None
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                metadata['Info'] = line.strip()
            elif ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                metadata[key] = value
            elif 'Wave' in line:
                headers = [col.strip() for col in line.split(';')]
            elif '[nm]' in line:
                units = [unit.strip() for unit in line.split(';')]
                break
   
    # Create column headers
    combined_headers = [f"{header} {unit}" for header, unit in zip(headers, units)]
   
    # Read data with improved handling
    df = pd.read_csv(filepath, sep=';', decimal=',', skiprows=8,
                     skipinitialspace=True, encoding='utf-8', names=combined_headers)
   
    # Convert numeric columns to float, handling comma decimals
    for col in df.columns:
        if 'Wave' in col or 'Absorbance' in col or 'A.U' in col:
            # Convert to string first, then replace comma with dot, then convert to float
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
    
    # Remove any rows with NaN values
    df = df.dropna()
    
    return df, metadata

def plot_spectra(filepath, save=False, wavelength_range=[100, 1400], height=0.015, prominence=0.08):
    # Read data
    df, metadata = read_uvvis_data(filepath)
   
    print(f"Data types after reading:")
    print(df.dtypes)
    print(f"First few rows:")
    print(df.head())
    
    # Extract wavelength range
    idx = find_nearest(df['Wave [nm]'], wavelength_range)
    wave = df['Wave [nm]'][idx[0]:idx[1]]
    absorbance = df['Absorbance [A.U]'][idx[0]:idx[1]]
   
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(wave, absorbance, label=filepath)  # Using filepath as legend
   
    # Find peaks
    peaks, _ = find_peaks(absorbance, height=height, prominence=prominence)
   
    # Plot peaks
    if len(peaks) > 0:
        ax.plot(wave.iloc[peaks], absorbance.iloc[peaks], 'ro', markersize=5)
       
        # Label peaks with wavelengths
        for peak in peaks:
            ax.annotate(f'{wave.iloc[peak]:.1f}',
                        xy=(wave.iloc[peak], absorbance.iloc[peak]),
                        xytext=(5, 5),
                        textcoords='offset points',
                        fontsize=8)
   
    # Add labels and title
    ax.set_xlabel('wavelength / nm ')
    ax.set_ylabel('absorbance / - ')
   # ax.set_title(f'UV-Vis Spectrum of BFD2 with N-DMBI-H in DMSO (too high concentration).')
    #ax.legend()
   
    # Save if requested
    if save:
        # Save as PDF
        pdf_path = f"{filepath}_peaks.pdf"
        fig.savefig(pdf_path, format='pdf', dpi=300)
        print(f"Figure saved as {pdf_path}")
       
        # Save as PNG
        png_path = f"{filepath}_peaks.png"
        fig.savefig(png_path, format='png', dpi=300)
        print(f"Figure saved as {png_path}")
   
    plt.show()
   
    # Print peak information
    if len(peaks) > 0:
        print(f"Found {len(peaks)} peaks:")
        for i, peak in enumerate(peaks):
            print(f"Peak {i+1}: {wave.iloc[peak]:.2f} nm, absorbance: {absorbance.iloc[peak]:.4f}")
    else:
        print("No peaks found with the current parameters.")
   
    return df, peaks

if __name__ == "__main__":
    file_path = r'experimental_data\Synthesis\ru_oh2_co_pnp\other\uv_vis_AE-512_2.TXT'
    plot_spectra(
        file_path,
        save=True,
        wavelength_range=[200, 1400],
        height=10,    # Adjust this parameter to control minimum peak height
        prominence=0.015  # Adjust this parameter to control minimum peak prominence
    )