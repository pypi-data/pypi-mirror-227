from typing import Optional, Any, Tuple
import numpy as np
from numpy.typing import DTypeLike
import pyparma

NDArray = np.ndarray[Any, Any]
DefaultScale: float = 10000

class Polytope:
	@classmethod
	def Empty(cls, dim: int, *, scale: Optional[float] = None, dtype: Optional[DTypeLike] = None) -> 'Polytope':
		return cls.FromGenerators(np.empty((0, dim), dtype = dtype), scale = scale)
	
	@classmethod
	def Universe(cls, dim: int, *, scale: Optional[float] = None, dtype: Optional[DTypeLike] = None) -> 'Polytope':
		return cls.FromHalfspaces(np.empty((0, dim), dtype = dtype), np.empty((0,), dtype = dtype), scale = scale)
	
	@classmethod
	def FromHalfspaces(cls, A: NDArray, b: NDArray, *, scale: Optional[float] = None) -> 'Polytope':
		if scale is None:
			scale = DefaultScale
		dtype = A.dtype
		
		# (Ax <= b) <=> (0 <= b + (-A)x)
		impl = pyparma.Constraint_System()
		A = _quantize(A, scale)
		b = _quantize(b, scale**2)
		for Ai, bi in zip(A, b):
			ex = pyparma.Linear_Expression(Ai, 0)
			impl.insert(ex <= bi)
		
		return cls(pyparma.C_Polyhedron(impl), scale = scale, dtype = dtype)
	
	@classmethod
	def FromGenerators(cls, V: Optional[NDArray] = None, R: Optional[NDArray] = None, *, scale: Optional[float] = None) -> 'Polytope':
		if scale is None:
			scale = DefaultScale
		
		M = (R if V is None else V)
		if M is None:
			raise ValueError("vertices and rays cannot both be omitted")
		dtype = M.dtype
		dim = M.shape[-1]
		
		if V is None:
			V = np.empty((0, dim), dtype = dtype)
		if R is None:
			R = np.empty((0, dim), dtype = dtype)
		
		impl = pyparma.Generator_System()
		V = _quantize(V, scale)
		R = _quantize(R, scale)
		for Vi in V:
			impl.insert(pyparma.point(pyparma.Linear_Expression(Vi, 0), 1))
		for Ri in R:
			impl.insert(pyparma.ray(pyparma.Linear_Expression(Ri, 0)))
		
		return cls(pyparma.C_Polyhedron(impl), scale = scale, dtype = dtype)
	
	def __init__(self, impl: pyparma.C_Polyhedron, *, scale: Optional[float] = None, dtype: Optional[DTypeLike] = None):
		if scale is None:
			scale = DefaultScale
		if scale <= 0:
			raise ValueError("scale must be positive", scale)
		if dtype is None:
			dtype = np.float64
		self.impl = impl
		self.dim = impl.space_dimension()
		self.dtype = dtype
		self.scale = scale
	
	def add_halfspace(self, A: NDArray, b: NDArray) -> None:
		if len(A.shape) == 1:
			A = A[None,:]
			b = np.broadcast_to(b, (1,))
		A = _quantize(A, self.scale)
		b = _quantize(b, self.scale**2)
		for Ai, bi in zip(A, b):
			self.impl.add_constraint(pyparma.Linear_Expression(Ai, 0) <= bi)
	
	def add_point(self, V: NDArray) -> None:
		if len(V.shape) == 1:
			V = V[None,:]
		V = _quantize(V, self.scale)
		for Vi in V:
			self.impl.add_generator(pyparma.point(pyparma.Linear_Expression(Vi, 0), 1))
	
	def add_ray(self, R: NDArray) -> None:
		if len(R.shape) == 1:
			R = R[None,:]
		R = _quantize(R, self.scale)
		for Ri in R:
			self.impl.add_generator(pyparma.ray(pyparma.Linear_Expression(Ri, 0)))
	
	def get_inequalities(self) -> Tuple[NDArray, NDArray]:
		A_list = []
		b_list = []
		for c in self.impl.minimized_constraints():
			coef = c.coefficients()
			inho = c.inhomogeneous_term() / self.scale
			A_list.append(coef)
			b_list.append(inho)
			if c.is_equality():
				A_list.append(-np.array(coef))
				b_list.append(-inho)
		
		if A_list:
			A = np.array(A_list, dtype = self.dtype)
			# PPL constraints are `coeffs @ x + b >= 0` so `A = -coeffs`
			np.negative(A, out = A)
			norms = np.linalg.norm(A, axis = 1)
			A /= norms[:,None]
			b = np.array(b_list, dtype = self.dtype)
			b /= norms
		else:
			A = np.empty((0, self.dim), dtype = self.dtype)
			b = np.empty((0,), dtype = self.dtype)
		
		return A, b
	
	def get_generators(self) -> Tuple[NDArray, NDArray]:
		V_list = []
		R_list = []
		for g in self.impl.minimized_generators():
			coef = np.array(g.coefficients(), dtype = self.dtype)
			if g.is_point():
				V_list.append(coef / g.divisor())
			else:
				R_list.append(coef)
		if V_list:
			V = np.array(V_list, dtype = self.dtype)
			V /= self.scale
		else:
			V = np.empty((0, self.dim), dtype = self.dtype)
		if R_list:
			R = np.array(R_list, dtype = self.dtype)
			R /= np.linalg.norm(R, axis = 1, keepdims = True)
		else:
			R = np.empty((0, self.dim), dtype = self.dtype)
		return V, R
	
	def copy(self) -> 'Polytope':
		return Polytope(pyparma.C_Polyhedron(self.impl), scale = self.scale, dtype = self.dtype)

def _quantize(m: NDArray, scale: float) -> NDArray:
	m = m * scale
	np.around(m, out = m)
	return m.astype(np.int64)
