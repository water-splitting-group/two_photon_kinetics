import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

# Your data (example)
labels = ['365 nm', '470 nm', '365 nm and 470 nm']  # Labels for the bars
means = [13.5, 0, 18.5]          # Mean or central value
errors = [0.5, 0.1, 1.5]         # Error bar (e.g., half range or std dev)

x = np.arange(len(labels))

# Assign unique colors to each bar
colors = ['darkblue', '#ff7f0e', 'darkgreen']  # blue, orange, green

plt.bar(x, means, yerr=errors, capsize=5, color=colors, edgecolor='black')
plt.xlabel('irradiation wavelength')
plt.ylim(0, 22)  # Set y-axis limits
plt.xticks(x, labels)
plt.ylabel('yield([Ru(CO)H(OH)(PNP)]) / %')
plt.tight_layout()
plt.show()
