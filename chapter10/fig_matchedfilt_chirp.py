"""
Matched Filter Chirp Search
---------------------------
Figure 10.26

A matched filter search for a chirp signal in time series data. A simulated
data set generated from a model of the form y = b0+Asin[omega t + beta t^2],
with homoscedastic Gaussian errors with sigma = 2, is shown in the top-right
panel. The posterior pdf for the four model parameters is determined using
MCMC and shown in the other panels.
"""
# Author: Jake VanderPlas
# License: BSD
#   The figure produced by this code is published in the textbook
#   "Statistics, Data Mining, and Machine Learning in Astronomy" (2013)
#   For more information, see http://astroML.github.com
#   To report a bug or issue, use the following forum:
#    https://groups.google.com/forum/#!forum/astroml-general
import numpy as np
from matplotlib import pyplot as plt

# Hack to fix import issue in older versions of pymc
import scipy
import scipy.misc
scipy.derivative = scipy.misc.derivative
import pymc

from astroML.plotting.mcmc import plot_mcmc
from astroML.decorators import pickle_results

#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=False)


#----------------------------------------------------------------------
# Set up toy dataset
def chirp(t, b0, beta, A, omega):
    return b0 + A * np.sin(omega * t + beta * t * t)

np.random.seed(0)

N = 100
b0_true = 10
A_true = 5
beta_true = 0.01
omega_true = 0.1
sigma = 2.0

t = 100 * np.random.random(N)

y_true = chirp(t, b0_true, beta_true, A_true, omega_true)
y_obs = np.random.normal(y_true, sigma)

t_fit = np.linspace(0, 100, 1000)
y_fit = chirp(t_fit, b0_true, beta_true, A_true, omega_true)

i = np.argsort(t)

#----------------------------------------------------------------------
# Set up MCMC sampling
b0 = pymc.Uniform('b0', 0, 50, value=50 * np.random.random())
A = pymc.Uniform('A', 0, 50, value=50 * np.random.random())
log_beta = pymc.Uniform('log_beta', -10, 10, value=-4.6)
log_omega = pymc.Uniform('log_omega', -10, 10, value=-2.3)


# uniform prior on log(beta)
@pymc.deterministic
def beta(log_beta=log_beta):
    return np.exp(log_beta)


# uniform prior on log(omega)
@pymc.deterministic
def omega(log_omega=log_omega):
    return np.exp(log_omega)


@pymc.deterministic
def y_model(t=t, b0=b0, A=A, beta=beta, omega=omega):
    return chirp(t, b0, beta, A, omega)

y = pymc.Normal('y', mu=y_model, tau=sigma ** -2, observed=True, value=y_obs)

model = dict(b0=b0, A=A,
             log_beta=log_beta, beta=beta,
             log_omega=log_omega, omega=omega,
             y_model=y_model, y=y)


#----------------------------------------------------------------------
# Run the MCMC sampling (saving results to a pickle)
@pickle_results('matchedfilt_chirp.pkl')
def compute_MCMC_results(niter=20000, burn=2000):
    S = pymc.MCMC(model)
    S.sample(iter=niter, burn=burn)
    traces = [S.trace(s)[:] for s in ['b0', 'A', 'omega', 'beta']]

    M = pymc.MAP(model)
    M.fit()
    fit_vals = (M.b0.value, M.beta.value, M.A.value, M.omega.value)

    return traces, fit_vals

traces, fit_vals = compute_MCMC_results()

labels = ['$b_0$', '$A$', r'$\omega$', r'$\beta$']
limits = [(9.5, 11.3), (3.6, 6.4), (0.065, 0.115), (0.00975, 0.01045)]
true = [b0_true, A_true, omega_true, beta_true]

#----------------------------------------------------------------------
# Find the Maximum a posteriori values
fig = plt.figure(figsize=(5, 5))

ax = plt.axes([0.5, 0.7, 0.45, 0.25])
t_fit = np.linspace(0, 100, 1001)
y_fit = chirp(t_fit, *fit_vals)
plt.scatter(t, y_obs, s=9, lw=0, c='k')
plt.plot(t_fit, y_fit, '-k')
plt.xlim(0, 100)
plt.xlabel('$t$')
plt.ylabel(r'$h_{\rm obs}$')

# This function plots multiple panels with the traces
plot_mcmc(traces, labels=labels, limits=limits, true_values=true, fig=fig,
          bins=30, bounds=[0.12, 0.08, 0.95, 0.91], colors='k')
plt.show()
