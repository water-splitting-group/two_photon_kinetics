import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ==========================
# Plot appearance
# ==========================
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

# ==========================
# Configuration
# ==========================
FILE_PATH = r'experimental_data\irradiations\o2\blank_irrad.txt'  # your PyroScience file
START_TIME = 0                                # adjust as needed
T_START_LABEL = -2700                                  # x-axis starting label
OUTPUT_FILE = r'experimental_data\irradiations\o2\blank_plot.png'                # output image name

# ==========================
# Helper functions
# ==========================
def read_pyroscience_file(filepath):
    """Read PyroScience txt file, skipping header lines starting with #"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                lines = f.readlines()
            data_start = next(i for i, line in enumerate(lines) if not line.startswith('#'))
            df = pd.read_csv(filepath, sep='\t', skiprows=data_start, encoding=encoding)

            # Fix potential mojibake (e.g., “�mol” → “µmol”)
            df.columns = df.columns.str.replace('�', 'µ').str.strip()
            print(f"✅ Successfully read {filepath} using {encoding} encoding")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"⚠️ Error reading {filepath} with {encoding}: {e}")
    raise ValueError(f"❌ Could not read {filepath} with any of the attempted encodings: {encodings}")

def find_col(df, keyword):
    """Find the first column containing a keyword (case-insensitive)"""
    cols = [c for c in df.columns if keyword.lower() in c.lower()]
    return cols[0] if cols else None

# ==========================
# Read and prepare data
# ==========================
print("Reading file...")
df = read_pyroscience_file(FILE_PATH)

# Detect columns
time_col = find_col(df, 'dt') or find_col(df, 'time')
oxygen_col = find_col(df, 'Oxygen')
print(f"Detected columns: time='{time_col}', oxygen='{oxygen_col}'")

# Filter and standardize data
df_filtered = df[df[time_col] >= START_TIME].copy()
df_filtered['time_adj'] = df_filtered[time_col] - START_TIME
df_filtered.rename(columns={oxygen_col: 'oxygen'}, inplace=True)

# Clean NaNs
df_filtered.dropna(subset=['oxygen'], inplace=True)

# Prepare for plotting
df_filtered['time_plot'] = df_filtered['time_adj'] + T_START_LABEL

# ==========================
# Plotting
# ==========================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered['time_plot'], df_filtered['oxygen'],
        label='oxygen', marker='o', markersize=0, linestyle='-', color='black', linewidth=1)

ax.set_xlabel('Time / s')
ax.set_ylabel(r'$\mathrm{O_2}$ / $\mathrm{\mu mol\ L^{-1}}$')
ax.set_xlim(T_START_LABEL, T_START_LABEL + 2700 + 1440 + 1262)  # adjust if needed
ax.set_ylim(-0.15, 1.2)
ax.legend()


plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
print(f"\n✅ Plot saved as '{OUTPUT_FILE}'")
plt.show()

# ==========================
# Summary Statistics
# ==========================
print("\n--- Summary Statistics ---")
print(f"{len(df_filtered)} points | Time: {df_filtered['time_adj'].min():.2f}–{df_filtered['time_adj'].max():.2f} s")
