import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from matplotlib import rcParams
import math as math

# Font settings
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 14

# Load data
data = np.genfromtxt(r'experimental_data\Synthesis\ru_oh2_co_pnp\AE-382-MS-ACN_2.xy')
x = data[:, 0]
y = data[:, 1]

# --- Define x-axis range for peak picking ---
x_min = 580
x_max = 595
range_mask = (x >= x_min) & (x <= x_max)

# --- Perform peak picking only in the selected range ---
peaks_in_range, properties = find_peaks(
    y[range_mask],
    height=100,         # minimum intensity (y-value) of a peak
    prominence=50       # how much a peak stands out from surroundings
)


# Convert local indices to global indices
global_peaks = np.where(range_mask)[0][peaks_in_range]
peak_positions = x[global_peaks]
peak_heights = y[global_peaks]

# --- Plot ---
plt.figure(figsize=(8, 5))
plt.plot(x, y, 'o-', markersize=1, label='Signal')
#plt.plot(peak_positions, peak_heights, 'rx', label='Peaks in range')
plt.xlabel('m/z / -')
plt.ylabel('Intensity / a.u.')
plt.legend()
plt.tight_layout()
plt.savefig("my_plot.pdf", bbox_inches="tight") 
plt.show()

# --- Save peak list ---
peak_list = np.column_stack((peak_positions, peak_heights))
np.savetxt('dihydroxo_MS_peaks.txt', peak_list, header='m/z    Intensity', fmt='%.6f', delimiter='    ')
