"""This example illustrates how to minimize an arbitrary Python function using the zfit minimizer.

This may has some overhead in the beginning and won't be instantly fast compared to other libraries if run once.

Copyright (c) 2021 zfit
"""

#  Copyright (c) 2021 zfit

import numpy as np

import zfit

# set everything to numpy mode
zfit.run.set_autograd_mode(False)
zfit.run.set_graph_mode(False)

# create our favorite minimizer
minimizer = zfit.minimize.IpyoptV1()


# minimizer = zfit.minimize.Minuit()
# minimizer = zfit.minimize.ScipyTrustKrylovV1()
# minimizer = zfit.minimize.NLoptLBFGSV1()


def func(x):
    x = np.array(x)  # make sure it's an array
    return np.sum((x - 0.1) ** 2 + x[1] ** 4)


# we can also use a more complicated function instead
# from scipy.optimize import rosen as func


# we need to set the errordef, the definition of "1 sigma"
func.errordef = 0.5

# initial parameters
params = [1, -3, 2, 1.4, 11]
# or for a more fine-grained control
# params = {
#     'value': [1, -3, 2, 1.4, 11],  # mandatory
#     'lower': [-2, -5, -5, -10, -15],  # lower bound, can be omitted
#     'upper': [2, 4, 5, 10, 15],  # upper bound, can be omitted
#     'step_size': [0.1] * 5,  # initial step size, can be omitted
# }

# minimize
result = minimizer.minimize(func, params)

# estimate errors
result.hesse()
result.errors()
print(result)