import numpy as np
cimport numpy as np

# to build the module on linux:
#cython exp_smoothing_conv.pyx
#gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.6 -o exp_smoothing_conv.so exp_smoothing_conv.c

dtype = np.float64
ctypedef np.float64_t dtype_t

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)

def pyx_exp_smoothed_value(np.ndarray[dtype_t, ndim=1] kernel, dtype_t alpha, np.ndarray[dtype_t, ndim=1] data, dtype_t previous):
	cdef Py_ssize_t N = data.shape[0]
	cdef Py_ssize_t Nk = kernel.shape[0]
	cdef Py_ssize_t i
	cdef dtype_t value, conv
	
	if N == 0:
		value = previous
	else:
		conv = 0.
		
		for i in range(0, N):
			conv = conv + kernel[Nk - N + i]*data[i]
		
		value = alpha * conv + previous*(1.-alpha)**N
	
	return value
