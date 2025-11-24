import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

# Time points (shared for all yield curves)
time = np.array([0, 1, 4, 24, 48])

# Yield / hydride
y1 = np.array([0.0, 0.0, 2.5, 19.0, 23.0])
err1 = np.array([0.5, 0.5, 0.05, 1, 1])

# Yield / main side product
y2 = np.array([0.0, 0.0, 4.5, 39.0, 31.5])
err2 = np.array([0.5, 0.5, 1.5, 7, 1.5])

# Yield / reactant
y3 = np.array([98, 94.5, 71, 9.5, 0.0])
err3 = np.array([0.5, 1.5, 9, 1.5, 0.5])

plt.figure(figsize=(7, 5))

plt.errorbar(time, y1, color="darkblue", yerr=err1, fmt="o-", capsize=4, label="[Ru(CO)H(OH)(PNP)]")
plt.errorbar(time, y2, color="#ff7f0e", yerr=err2, fmt="s-", capsize=4, label="main side product")
plt.errorbar(time, y3, color="darkgreen", yerr=err3, fmt="^-", capsize=4, label="[Ru(CO)(OH)$_2$(PNP)]")

plt.xlabel("time / h")
plt.ylabel("yield / %")
plt.xlim(-0.5, 48.5)
plt.ylim(-2, 100.5)

plt.legend()

plt.tight_layout()
plt.show()
