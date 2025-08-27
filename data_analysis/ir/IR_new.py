import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

# --- Parameters ---
input_file = r"experimental_data\Synthesis\ru_oh2_co_pnp\ir_raw_data.CSV"         # Input CSV file
output_file = r"experimental_data\Synthesis\ru_oh2_co_pnp\ir_peak_list.CSV"        # Output CSV file for peaks
save_plot = False                # Set to True if you want to save the plot as PNG
plot_file = "peaks_plot.png"     # Plot image filename (if saving)

# --- Peak detection parameters ---
prominence = 0.0075                 # Minimum prominence of peaks
height = 0.01                     # Minimum height of peaks

# --- Load data ---
df = pd.read_csv(input_file)
x = df.iloc[:, 0].values         # First column = x values
y = df.iloc[:, 1].values         # Second column = y values

# --- Find peaks ---
peaks, properties = find_peaks(y, prominence=prominence, height=height)

# --- Create peak list ---
peak_df = pd.DataFrame({
    "x": x[peaks],
    "y": y[peaks],
    "height": properties["peak_heights"],
    "prominence": properties["prominences"]
})

# --- Plot ---
plt.figure(figsize=(10, 6))
plt.plot(x, y)

# Kurze vertikale Linien für Peaks
line_height = 0.02  # Höhe der Linien (anpassbar)
for i, peak_idx in enumerate(peaks):
    # Kurze vertikale Linie vom Peak-Punkt nach oben
    plt.plot([x[peak_idx], x[peak_idx]], [y[peak_idx], y[peak_idx] + line_height], 
             'k-', linewidth=1.5)
    # Label mit x-Wert am oberen Ende der Linie
    plt.text(x[peak_idx], y[peak_idx] + line_height + 0.005, f'{x[peak_idx]:.1f}', 
             rotation=90, ha='left', va='bottom', fontsize=12, color='black')

plt.xlabel(r"wavenumber / cm$^{-1}$")
plt.ylabel("absorbance / - ")
plt.xlim(480, 4000)  # Common IR range
plt.ylim(0, y.max() * 1.25)  # From 0 to 110% of max signal
plt.gca().invert_xaxis()         # Invert x-axis
plt.tight_layout()

if save_plot:
    plt.savefig(plot_file, dpi=300)
plt.show()

# --- Export peak list ---
peak_df.to_csv(output_file, index=False)
print(f"Exported {len(peak_df)} peaks to '{output_file}'")