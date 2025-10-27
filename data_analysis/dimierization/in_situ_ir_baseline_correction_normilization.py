import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from pybaselines import Baseline

# === Configuration ===
apply_baseline = True  # Toggle baseline correction on/off
reference_wn = 1182     # Wavenumber for normalization
exclude_indices = []  # Indices of spectra to exclude (e.g. [0] or [0, -1, -2])

# === Load averaged, uncorrected spectra ===
df = pd.read_csv(r"experimental_data\dimierization\in_situ_ir_conc_dimension_1.csv")
wavenumbers = df["Wavenumbercm-1"].values
spectra = df.drop(columns="Wavenumbercm-1")

# === Extract concentrations from column names ===
concentrations = [float(col.split()[0]) for col in spectra.columns]

# === Apply baseline correction (optional) ===
if apply_baseline:
    print("Applying AsLS baseline correction...")
    lam = 1e5
    p = 0.01
    baseline_obj = Baseline()
    corrected_spectra = []
    baselines = []

    for col in spectra.columns:
        spectrum = spectra[col].values
        baseline, _ = baseline_obj.asls(spectrum, lam=lam, p=p)
        corrected = spectrum - baseline
        corrected_spectra.append(corrected)
        baselines.append(baseline)

    corrected_df = pd.DataFrame(np.array(corrected_spectra).T, columns=spectra.columns)
    baseline_df = pd.DataFrame(np.array(baselines).T, columns=spectra.columns)

    # Plot original, baseline, and corrected
    num_spectra = len(spectra.columns)
    cols = 4
    rows = int(np.ceil(num_spectra / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 3*rows), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, col in enumerate(spectra.columns):
        ax = axes[i]
        ax.plot(wavenumbers, spectra[col], label="Original")
        ax.plot(wavenumbers, baseline_df[col], label="Baseline", linestyle='--')
        ax.plot(wavenumbers, corrected_df[col], label="Corrected")
        ax.set_title(f"{col}")
        ax.grid(True)
        if i % cols == 0:
            ax.set_ylabel("Intensity")
        if i >= (rows - 1)*cols:
            ax.set_xlabel("Wavenumber (cm⁻¹)")
        ax.label_outer()

    for j in range(i+1, rows*cols):
        fig.delaxes(axes[j])

    fig.suptitle("AsLS Baseline Correction per Spectrum", fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.legend(["Original", "Baseline", "Corrected"], loc='upper right')
    plt.show()
else:
    print("Skipping baseline correction — using original spectra.")
    corrected_df = spectra.copy()

# === Handle excluded indices ===
# Convert negative indices to positive
exclude_indices = [(i if i >= 0 else len(concentrations) + i) for i in exclude_indices]
keep_indices = [i for i in range(len(concentrations)) if i not in exclude_indices]

# Subset corrected data and concentrations
corrected_subset = corrected_df.iloc[:, keep_indices]
concentrations_subset = [concentrations[i] for i in keep_indices]

# === Normalize spectra at reference wavenumber ===
ref_idx = np.argmin(np.abs(wavenumbers - reference_wn))
ref_values = corrected_subset.iloc[ref_idx, :]
normalized_spectra = corrected_subset.divide(ref_values, axis=1)

# === Plot normalized spectra ===
fig, ax = plt.subplots(figsize=(10, 6))

norm = mcolors.Normalize(vmin=min(concentrations_subset), vmax=max(concentrations_subset))
cmap = cm.viridis_r  # or other: 'plasma', 'turbo', etc.

for i in reversed(range(len(concentrations_subset))):
    conc = concentrations_subset[i]
    spectrum = normalized_spectra.iloc[:, i]
    color = cmap(norm(conc))
    ax.plot(wavenumbers, spectrum, color=color, label=f"{conc:.1e} M")

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label("Ru Concentration (M)")

ax.set_xlabel("Wavenumber (cm⁻¹)")
ax.set_ylabel("Normalized Intensity")
ax.set_title(f"{'Baseline-corrected ' if apply_baseline else ''}Spectra Normalized at {reference_wn} cm⁻¹\n(excluding indices: {exclude_indices})")
ax.grid(True)
plt.tight_layout()
plt.show()

# === Export normalized spectra ===
normalized_export = pd.concat([pd.Series(wavenumbers, name="Wavenumbercm-1"), normalized_spectra], axis=1)
out_file = r"experimental_data\dimierization\in_situ_ir_normalized_1.csv"
normalized_export.to_csv(out_file, index=False)
print(f"Saved normalized spectra to: {out_file}")
