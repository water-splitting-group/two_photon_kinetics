import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# --- Load baseline-corrected spectra ---
spectra_file = r"experimental_data\dimierization\in_situ_ir_cleaned_data_1.csv"
df = pd.read_csv(spectra_file)

wavenumbers = df["Wavenumbercm-1"]
spectra = df.drop(columns="Wavenumbercm-1")

# --- Load concentrations and repeat counts ---
conc_df = pd.read_csv(r"experimental_data\dimierization\in_situ_ir_ru_conc_1.csv")
concentrations = conc_df["concentration"].values
group_sizes = conc_df["repeats"].values

# --- Sanity check ---
total_traces = spectra.shape[1]
expected_traces = sum(group_sizes)
assert expected_traces == total_traces, (
    f"Mismatch: sum of repeats = {expected_traces} traces, "
    f"but spectra file contains {total_traces} traces."
)

# --- Average spectra per condition ---
averaged_spectra = []
start = 0
for size in group_sizes:
    group = spectra.iloc[:, start:start + size]
    averaged = group.mean(axis=1)
    averaged_spectra.append(averaged)
    start += size

# Convert to DataFrame
averaged_spectra_df = pd.DataFrame(averaged_spectra).T
averaged_spectra_df.columns = [f"{c:.2e} M" for c in concentrations]

# --- Save averaged spectra ---
result_df = pd.concat([wavenumbers, averaged_spectra_df], axis=1)
result_df.to_csv(r"experimental_data\dimierization\in_situ_ir_ru_conc_1.csv", index=False)

# --- Plot: intensity vs. concentration ---
fig, ax = plt.subplots(figsize=(10, 6))

# Normalize concentration values for colormap scaling
norm = mcolors.Normalize(vmin=min(concentrations), vmax=max(concentrations))
cmap = cm.plasma  # or 'viridis', 'turbo', etc.

for i, conc in enumerate(concentrations):
    color = cmap(norm(conc))
    spectrum = averaged_spectra_df.iloc[:, i]
    ax.plot(wavenumbers, spectrum, color=color, label=f"{conc:.1e} M")

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # required for colorbar
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label("Ru Concentration (mM)")

ax.set_xlabel("Wavenumber (cm⁻¹)")
ax.set_ylabel("Intensity")
ax.set_title("Averaged Spectra per Condition")
ax.grid(True)
plt.tight_layout()
plt.show()
