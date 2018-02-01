
# Author: Jake VanderPlas
# License: BSD
#   The figure produced by this code is published in the textbook
#   "Statistics, Data Mining, and Machine Learning in Astronomy" (2013)
#   For more information, see http://astroML.github.com
#   To report a bug or issue, use the following forum:
#    https://groups.google.com/forum/#!forum/astroml-general
from time import time
import numpy as np
from matplotlib import pyplot as plt

#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=False)

#------------------------------------------------------------
# Compute the execution times as a function of array size

# time quick-sort of a numpy array
N_npy = 10 ** np.linspace(5, 7, 10)
time_npy = np.zeros_like(N_npy)

for i in range(len(N_npy)):
    x = np.random.random(int(N_npy[i]))
    t0 = time()
    x.sort(kind='quicksort')
    t1 = time()
    time_npy[i] = t1 - t0

# time built-in sort of python list
N_list = N_npy[:-3]
time_list = np.zeros_like(N_list)

for i in range(len(N_list)):
    x = list(np.random.random(int(N_list[i])))
    t0 = time()
    x.sort()
    t1 = time()
    time_list[i] = t1 - t0

#------------------------------------------------------------
# Plot the results
fig = plt.figure(figsize=(5, 3.75))
fig.subplots_adjust(bottom=0.15)
ax = plt.axes(xscale='log', yscale='log')
ax.grid()

# plot the observed times
ax.plot(N_list, time_list, 'sk', color='gray', ms=5, label='list sort')
ax.plot(N_npy, time_npy, 'ok', color='gray', ms=5, label='NumPy sort')

# plot the expected scalings
scale = np.linspace(N_npy[0] / 2, N_npy[-1] * 2, 100)
scaling_N = scale * time_npy[0] / N_npy[0]
scaling_NlogN = (scale * np.log2(scale) * time_npy[0]
                 / N_npy[0] / np.log2(N_npy[0]))

ax.plot(scale, scaling_NlogN, '--k', label=r'$\mathcal{O}[N \log N]$')
ax.plot(scale, scaling_N, ':k', label=r'$\mathcal{O}[N]$')

scaling_N = scale * time_list[0] / N_list[0]
scaling_NlogN = (scale * np.log2(scale) * time_list[0]
                 / N_list[0] / np.log2(N_list[0]))

ax.plot(scale, scaling_NlogN, '--k')
ax.plot(scale, scaling_N, ':k')

# Create titles and labels
ax.set_title("Scaling of Sort Algorithms")
ax.set_xlabel('Length of Array')
ax.set_ylabel('Relative sort time')
plt.legend(loc='upper left')

ax.set_xlim(scale[0], scale[-1])

plt.show()