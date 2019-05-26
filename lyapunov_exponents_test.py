import unittest

from numpy import *
import numpy as np
from lorenz_map import LorenzMap
from lyapunov_exponents import lyapunov_exponent, my_norm
from numpy.linalg import *
import time
def gprint(*args):
    '''green print'''
    print('\033[32;1m', end='') # GREEN
    print(*args, end='\033[0m\n')

TEST_TOLERANCE = 0.1

# LORENZ_MAP = LorenzMap(sigma=10, rho=28, beta=8/3)
# LORENZ_MAP = LorenzMap(sigma=100, rho=100, beta=10)
# LORENZ_MAP = LorenzMap(sigma=100, rho=100, beta=10)

# LORENZ_MAP_REFERENCE_SOLUTION = array([-14.57, 0, 0.90], dtype)
# LORENZ_MAP_INITIAL_CONDITION  = array([-5.76,  2.27,  32.82])
# LORENZ_MAP_INITIAL_CONDITION  = array([1, 0, 0])



# l = lyapunov_exponent(LORENZ_MAP, single_initial_condition=LORENZ_MAP_INITIAL_CONDITION, tol=TEST_TOLERANCE, max_it=10_000)
# l = lyapunov_exponent(LorenzMap(sigma=10.2, rho=24, beta=7) , array([1, 0, 0]), tol=TEST_TOLERANCE, max_it=500)
# l = lyapunov_exponent(LORENZ_MAP, single_initial_condition=LORENZ_MAP_INITIAL_CONDITION, tol=TEST_TOLERANCE, max_it=100)

sigma = 10
rho   = 28
beta  = 8/3

# sigma = 10
# rho   = 150
# beta  = 8/3

# sigma = 10
# rho   = 100
# beta  = 9
# max_it = 50
max_it = 500

t0 = time.time()
l = lyapunov_exponent(LorenzMap(sigma=sigma, rho=rho, beta=beta) , array([1, 0, 0]), tol=TEST_TOLERANCE, max_it=max_it)
# l = lyapunov_exponent(LorenzMap(sigma=10, rho=100, beta=6), array([1, 0, 0]), tol=TEST_TOLERANCE, max_it=500)
print(time.time() - t0, 'seconds')



print(l)
gprint(f'λ1 = {l[0]}')
gprint(f'λ2 = {l[1]}')
gprint(f'λ3 = {l[2]}')

a1 = sum(l)
a2 = -(sigma + beta + 1)
print()
gprint(f'λ1 + λ2 + λ3 = {a1}')
gprint(f' -(σ + ß +1) = {a2}')
gprint(f'ABSDIFF = {abs(a1 - a2)}')


# print(my_norm(LORENZ_MAP_REFERENCE_SOLUTION - l))
# print(TEST_TOLERANCE)

