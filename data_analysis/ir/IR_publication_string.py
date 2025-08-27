import pandas as pd

# --- Parameters ---
input_csv = r"experimental_data\Synthesis\ru_oh2_co_pnp\ir_peak_list.csv"  # Input CSV with peaks
output_csv = r"experimental_data\Synthesis\ru_oh2_co_pnp\ir_peak_list_publication.csv"  # Output file

# --- Load peak data ---
peaks_df = pd.read_csv(input_csv)

# --- Calculate normalized heights ---
max_height = peaks_df['y'].max()  # Find strongest signal
peaks_df['normalized_height'] = peaks_df['y'] / max_height  # Normalize to strongest peak

# --- Classify intensity ---
def classify_intensity(normalized_height):
    if normalized_height <= 0.33:
        return "weak"
    elif normalized_height <= 0.66:
        return "medium"
    else:
        return "strong"

peaks_df['intensity_class'] = peaks_df['normalized_height'].apply(classify_intensity)

# --- Create final output ---
result_df = pd.DataFrame({
    'wavenumber': peaks_df['x'],
    'normalized_height': peaks_df['normalized_height'].round(3),
    'intensity': peaks_df['intensity_class']
})

# --- Sort by wavenumber (descending for IR spectra) ---
result_df = result_df.sort_values('wavenumber', ascending=False)

# --- Export ---
result_df.to_csv(output_csv, index=False)

# --- Print summary ---
print(f"Peak analysis completed!")
print(f"Total peaks: {len(result_df)}")
print(f"Strong peaks (>66%): {len(result_df[result_df['intensity'] == 'strong'])}")
print(f"Medium peaks (33-66%): {len(result_df[result_df['intensity'] == 'medium'])}")
print(f"Weak peaks (<33%): {len(result_df[result_df['intensity'] == 'weak'])}")
print(f"Results saved to '{output_csv}'")

# --- Display first few entries ---
print("\nFirst 10 peaks:")
print(result_df.head(10).to_string(index=False))