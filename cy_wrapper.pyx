cimport cython
cimport numpy as np
import numpy as np
from libc.math cimport log, exp, round, abs

cdef extern from "math.h" nogil:
  double exp(double)
  double sqrt(double)
  double pow(double, double)
  double log(double)
  double erf(double)


@cython.cdivision(True)
cdef double std_norm_cdf(double x):
  return .5*(1+erf(x/sqrt(2.0)))


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cpdef double cprice_func(float s_var, float k0, float t_var, float sig, double cp):

  cdef double d1_var, d2_var, n_d1, n_d2, val
  cdef double r = .02

  d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
  d2_var = d1_var - sig * t_var**.5

  val = (cp * s_var * std_norm_cdf(cp*d1_var) - cp*k0*exp(-r*t_var) * std_norm_cdf(cp*d2_var))

  return val


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cpdef double gamma_func(float s_var, float k0, float t_var, float sig, float r):
    
  cdef double pi = 3.1415926535897

  cdef double d1_var, n_pdf, c_gamma

  d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
  n_pdf = exp(-d1_var**2/2)/(2*pi)**.5

  gamma = n_pdf/(s_var*(sig * t_var**.5))

  return gamma

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double vega_func(float s_var, float k0, float t_var, float sig):
    
  cdef double d1_var, vega
  cdef double pi = 3.1415926535897
  cdef double r = .02
    
  d1_var = (log(s_var/k0) + (r + .5 * sig**2)*t_var) / (sig * (t_var**.5))
  n_pdf = exp(-d1_var**2/2)/(2*pi)**.5
  vega = s_var * n_pdf * (t_var**.5) / 100 

  return vega

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cpdef cy_wrapper_iv(np.ndarray[dtype = DTYPE_t, ndim=2] main, int cp):

  cdef double [:,:] main_view = main
  cdef int I = main_view.shape[0]
  cdef double [:] return_view = np.zeros((I), np.float64)
  

  cdef double e = .01
  cdef double x0
  cdef double max_iter 
  cdef int i
  cdef double delta, s_var, k0, t_var, market
  cdef int max_range


  for i in range(0,I):

    x0 = .1
    max_iter = 0

    if k0 - s_var > market:

      max_range = 100

    else:

      max_range = 1000

    s_var = main_view[i,0]
    k0 = main_view[i,1]
    t_var = main_view[i,2]
    market = main_view[i,3]

    delta = cprice_func(s_var, k0, t_var, x0, cp) - market

    while abs(delta) > e and max_iter <= max_range:

      vega = vega_func(s_var,k0,t_var,x0)
    
      if delta > 0:
        if delta > vega: 
          x0 -= .01
        else:
          x0 -= .0001

        delta = cprice_func(s_var, k0, t_var, x0, cp) - market

      else:
        if -1 *delta > vega: 
          x0 += .01
        else:
          x0 += .0001

        delta = cprice_func(s_var, k0, t_var, x0, cp) - market

      max_iter += 1
      
    return_view[i] = x0

  return return_view

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
def cy_wrapper_gamma(np.ndarray[dtype = DTYPE_t, ndim=2] main):

  cdef double [:,:] main_view = main
  cdef int I = main_view.shape[0]
  cdef double [:] return_view = np.zeros((I), np.float64)

  for i in range(0,I):

    s_var = main_view[i,0]
    k0 = main_view[i,1]
    t_var = main_view[i,2]
    iv = main_view[i,4]

    g = gamma_func(s_var, k0, t_var, iv, .02)
    return_view[i] = g

  return return_view
