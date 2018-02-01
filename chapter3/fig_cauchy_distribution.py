import numpy as np
from scipy.stats import cauchy
from matplotlib import pyplot as plt

#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=False)

#------------------------------------------------------------
# Define the distribution parameters to be plotted
gamma_values = [0.5, 1.0, 2.0]
linestyles = ['-', '--', ':']
mu = 0
x = np.linspace(-10, 10, 1000)

#------------------------------------------------------------
# plot the distributions
fig, ax = plt.subplots(figsize=(5, 3.75))

for gamma, ls in zip(gamma_values, linestyles):
    dist = cauchy(mu, gamma)

    plt.plot(x, dist.pdf(x), ls=ls, color='black',
             label=r'$\mu=%i,\ \gamma=%.1f$' % (mu, gamma))

plt.xlim(-4.5, 4.5)
plt.ylim(0, 0.65)

plt.xlabel('$x$')
plt.ylabel(r'$p(x|\mu,\gamma)$')
plt.title('Cauchy Distribution')

plt.legend()
plt.show()