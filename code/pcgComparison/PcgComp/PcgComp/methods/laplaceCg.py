import numpy as np
from scipy.stats import norm
from PcgComp.methods.cg import Cg
import random

"""
Laplace approximation using conjugate gradient
Params:
    K - Covariance Matrix
    Y - Target labels
    init - Initial solution
    threshold - Termintion criteria for algorithm

"""
class LaplaceCg(object):

	def __init__(self, K, Y, init=None, threshold=1e-9):
		
		N = np.shape(K)[0]
		f = np.zeros((N,1))
		converged = False
		k = 0
		innerC = 0

		for i in xrange(N):
			pdfDiff = norm.logpdf(f) - norm.logcdf(Y*f)
			W = np.exp(2*pdfDiff) + Y*f*np.exp(pdfDiff)
			Wsqrt = np.sqrt(W)
			Wdiag= np.diag(Wsqrt.flatten())

			B = np.identity(N) + np.dot(Wdiag, np.dot(K, Wdiag))
			grad = Y*np.exp(pdfDiff)
			b = W*f + grad
			interim = np.dot(Wdiag, np.dot(K, b))

			cgRes = Cg(B, interim, threshold=threshold)
			s1 = cgRes.result
			innerC = innerC + cgRes.iterations
			a = b - Wsqrt*s1

			if(converged):
				break
			f_prev = f
			f = np.dot(K, a)
			diff = f - f_prev
			if (np.dot(diff.T,diff).flatten() < threshold*N or innerC>15000):
				converged = True
			k = k+1

		self.result = f
		self.iterations = k + innerC
