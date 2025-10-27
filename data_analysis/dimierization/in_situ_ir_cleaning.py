import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

# --- Load data ---
df = pd.read_csv(r"experimental_data\dimierization\in_situ_ir_raw_data_1.csv")
wavenumbers = df["Wavenumbercm-1"]
spectra = df.drop(columns="Wavenumbercm-1")

# --- Exclude faulty traces (original indices 32 to 51) ---
exclude_range = list(range(32, 49))
kept_trace_names = [col for i, col in enumerate(spectra.columns) if i not in exclude_range]
filtered_spectra = spectra[kept_trace_names]

# --- Prepare colormaps ---
cmap = get_cmap("plasma")

n_traces_all = spectra.shape[1]
colors_all = [cmap(i / (n_traces_all - 1)) for i in range(n_traces_all)]

n_traces_clean = filtered_spectra.shape[1]
colors_clean = [cmap(i / (n_traces_clean - 1)) for i in range(n_traces_clean)]

# --- Create combined figure ---
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# --- Plot all raw spectra ---
for i, col in enumerate(spectra.columns):
    axes[0].plot(wavenumbers, spectra[col], color=colors_all[i], alpha=0.6)
sm1 = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=n_traces_all - 1))
cbar1 = plt.colorbar(sm1, ax=axes[0], orientation='vertical', label="Trace Index")
axes[0].set_title("All Raw Spectra")
axes[0].set_ylabel("Intensity")
axes[0].grid(True)

# --- Plot cleaned spectra ---
for i, col in enumerate(filtered_spectra.columns):
    axes[1].plot(wavenumbers, filtered_spectra[col], color=colors_clean[i], alpha=0.6)
sm2 = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=n_traces_clean - 1))
cbar2 = plt.colorbar(sm2, ax=axes[1], orientation='vertical', label="Trace Index (Cleaned)")
axes[1].set_title("Spectra After Removing Faulty Traces")
axes[1].set_xlabel("Wavenumber (cm⁻¹)")
axes[1].set_ylabel("Intensity")
axes[1].grid(True)

plt.tight_layout()
plt.show()

# --- Save subset with original index ≥ 49 (i.e. traces 50+) ---
subset_names = [col for i, col in enumerate(spectra.columns) if i not in exclude_range and i >= 49]
subset_df = pd.concat([wavenumbers, filtered_spectra[subset_names]], axis=1)
subset_df.columns = ["Wavenumbercm-1"] + subset_names
subset_df.to_csv(r"experimental_data\dimierization\in_situ_ir_cleaned_data_1.csv", index=False)
