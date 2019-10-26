import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport log, exp, round
from math import *
from libc.stdlib cimport malloc, free
import pandas as pd

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double cprice_func(float s_var, float k0, float t_var, float sig, float r):

	cdef double d1_var, d2_var, n_d1, n_d2, c_val

	d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
	d2_var = d1_var - sig * t_var**.5
	
	n_d1 = (1.0 + erf(d1_var / (2.0)**.5)) / 2.0
	n_d2 = (1.0 + erf(d2_var / (2.0)**.5)) / 2.0
	c_val = (s_var * n_d1 - k0 * exp(-r*t_var) * n_d2)

	return c_val

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double pprice_func(float s_var, float k0, float t_var, float sig, float r):

	cdef double d1_var, d2_var, n_d1, n_d2, p_val

	d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
	d2_var = d1_var - sig * t_var**.5
	
	n_d1 = (1.0 + erf(-d1_var / (2.0)**.5)) / 2.0
	n_d2 = (1.0 + erf(-d2_var / (2.0)**.5)) / 2.0
	p_val = ((k0 * exp(-r*t_var)) * n_d2) - (s_var * n_d1)

	return p_val

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double cdelta_func(float s_var, float k0, float t_var, float sig, float r):
	
	cdef double d1_var, c_delta
	
	d1_var = (log(s_var/k0) + (r + .5 * sig**2)*t_var) / (sig * (t_var**.5))
	c_delta = ((1.0 + erf(d1_var / (2.0)**.5)) / 2.0)

	return c_delta

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double pdelta_func(float s_var, float k0, float t_var, float sig, float r):
	
	cdef double d1_var, p_delta
	
	d1_var = (log(s_var/k0) + (r + .5 * sig**2)*t_var) / (sig * (t_var**.5))
	p_delta = -1*((1.0 + erf(-1*d1_var / (2.0)**.5)) / 2.0)

	return p_delta

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double cvega_func(float s_var, float k0, float t_var, float sig, float r):
	
	cdef double d1_var, c_vega
	
	d1_var = (log(s_var/k0) + (r + .5 * sig**2)*t_var) / (sig * (t_var**.5))
	n_pdf = exp(-d1_var**2/2)/(2*pi)**.5
	c_vega = s_var * n_pdf * (t_var**.5) / 100 

	return c_vega

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double ctheta_func(float s_var, float k0, float t_var, float sig, float r):
	
	cdef double d1_var, d2_var, b, n_d2, n_pdf, c_theta

	d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
	d2_var = d1_var - sig * t_var**.5
	b = exp(-r*t_var)

	n_pdf = exp(-d1_var**2/2)/(2*pi)**.5
	n_d2 = (1.0 + erf(d2_var / (2.0)**.5)) / 2.0

	c_theta = ((-1 * s_var * n_pdf * sig) / (2*t_var**.5)) - r*(k0*b*n_d2)

	return c_theta/365

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cdef double ptheta_func(float s_var, float k0, float t_var, float sig, float r):
	
	cdef double d1_var, d2_var, b, n_d2, n_pdf, p_theta

	d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
	d2_var = d1_var - sig * t_var**.5
	b = exp(-r*t_var)

	n_pdf = exp(-d1_var**2/2)/(2*pi)**.5
	n_d2 = (1.0 + erf(-1*d2_var / (2.0)**.5)) / 2.0

	p_theta = ((-1 * s_var * n_pdf * sig) / (2*t_var**.5)) + r*(k0*b*n_d2)

	return p_theta/365

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cpdef double cgamma_func(float s_var, float k0, float t_var, float sig, float r):
	
	cdef double d1_var, n_pdf, c_gamma

	d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
	n_pdf = exp(-d1_var**2/2)/(2*pi)**.5

	c_gamma = n_pdf/(s_var*(sig * t_var**.5))

	return c_gamma

cdef double cAR_func(float s_var, float k0, float t_var, float sig, float r):

	cdef double d1_var, d2_var, ar 

	d1_var = (log(s_var/k0) + (r + (sig**2)/2)*t_var) / (sig * (t_var**.5))
	d2_var = d1_var - sig * t_var**.5

	ar = (1.0 + erf(d2_var / (2.0)**.5)) / 2.0

	return ar



@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)
cpdef cbsm(float scalar, float s0, float k0, float t, float sig, str param, s_view, t_view, c_type):

	cdef double [:,:] main_t = np.empty([s_view.shape[0], t_view.shape[0]])
	
	cdef float r = .02
	cdef double s_var, t_var
	cdef double c, c0

	cdef int i, j, I, J
	I = s_view.shape[0]
	J = t_view.shape[0]
	

	if param == 'Delta':
		if c_type == 0:
			for i in range(I):
				for j in range(J):

					s_var = s_view[i]
					t_var = (t_view[j]/365)

					c = cdelta_func(s_var, k0, t_var, sig, r) * scalar

					main_t[i,j] = c 

			return main_t, t_view, s_view

		else:
			for i in range(I):
				for j in range(J):

					s_var = s_view[i]
					t_var = (t_view[j]/365)

					c = pdelta_func(s_var, k0, t_var, sig, r) * scalar

					main_t[i,j] = c 

			return main_t, t_view, s_view


	if param == 'Gamma':
		for i in range(I):
			for j in range(J):

				s_var = s_view[i]
				t_var = (t_view[j]/365)

				c = cgamma_func(s_var, k0, t_var, sig, r) * scalar

				main_t[i,j] = c 

		return main_t, t_view, s_view

	if param == 'Theta':
		if c_type == 0:
			for i in range(I):
				for j in range(J):

					s_var = s_view[i]
					t_var = (t_view[j]/365)


					c = ctheta_func(s_var, k0, t_var, sig, r) * scalar

					main_t[i,j] = c 

			return main_t, t_view, s_view

		else:
			for i in range(I):
				for j in range(J):

					s_var = s_view[i]
					t_var = (t_view[j]/365)


					c = ptheta_func(s_var, k0, t_var, sig, r) * scalar

					main_t[i,j] = c 

			return main_t, t_view, s_view


	if param == 'Vega':
		for i in range(I):
			for j in range(J):

				s_var = s_view[i]
				t_var = (t_view[j]/365)


				c = cvega_func(s_var, k0, t_var, sig, r) * scalar

				main_t[i,j] = c 

		return main_t, t_view, s_view

	if param == 'Exercise Probability':
		for i in range(I):
			for j in range(J):

				s_var = s_view[i]
				t_var = (t_view[j]/365)


				c = cAR_func(s_var, k0, t_var, sig, r)

				main_t[i,j] = c 

		return main_t, t_view, s_view

	else:

		if c_type == 0:

			c0 = cprice_func(s0, k0, t/365, sig, r)

			for i in range(I):
				for j in range(J):

					s_var = s_view[i]
					t_var = (t_view[j]/365)


					c = (cprice_func(s_var, k0, t_var, sig, r) - c0) * scalar

					main_t[i,j] = c 

			return main_t, t_view, s_view

		else:

			c0 = pprice_func(s0, k0, t/365, sig, r)

			for i in range(I):
				for j in range(J):

					s_var = s_view[i]
					t_var = (t_view[j]/365)


					c = (pprice_func(s_var, k0, t_var, sig, r) - c0) * scalar

					main_t[i,j] = c 

			return main_t, t_view, s_view


DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

cpdef main_array(np.ndarray[dtype = DTYPE_t, ndim=2] main, str Z):

	cdef double [:,:] main_view = main
	cdef int I = main_view.shape[0]
	cdef int i, j, k

	cdef double s_w = main_view[0,6]
	cdef double s_s = main_view[0,7]
	cdef double t_s = main_view[0,8]
	cdef double s0 = main_view[0,2]
	cdef double t0 = main_view[0,4]
	cdef float s_max = s0+s_w*s0
	cdef float s_min = s0-s_w*s0

	cdef double [:] t_view = np.arange(1,t0, t_s)
	cdef double [:] s_view = np.arange(s_min,s_max, s_s*s0)
	cdef double [:,:] return_matrix = np.zeros((s_view.shape[0], t_view.shape[0]), np.float64)
	cdef double [:,:,:] matrix = np.zeros((s_view.shape[0],t_view.shape[0],I), np.float64)

	cdef double scalar, c_type, s_var, k0, t_var, sig
	cdef int x = s_view.shape[0]
	cdef int y = t_view.shape[0]
	for k in range(I):
		
		scalar = main_view[k,0]
		c_type = main_view[k,1]
		s_var = main_view[k,2]
		k0 = main_view[k,3]
		t_var = main_view[k,4]
		sig = main_view[k,5]

		array, array_x, array_y = cbsm(scalar, s_var, k0, t_var, sig, Z, s_view, t_view, c_type)
		
		for i in range(x):
			for j in range(y):
				matrix[i,j,k] = array[i,j]

	for k in range(I):
		for i in range(x):
			for j in range(y):
				return_matrix[i,j] += matrix[i,j,k]

	return_array = np.asanyarray(return_matrix)
	return_index = np.asanyarray(s_view)
	return_columns = np.asanyarray(t_view)

	df = pd.DataFrame(return_array)
	df.columns = return_columns
	df = df.set_index(return_index)


	return df
