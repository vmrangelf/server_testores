'''
operadores.py

	Se definen 3 funciones principales las cuales
	aplican los operadores (fi,theta,gamma) a 
	dos matrices básica y regresan la matriz
	resultante. 

		phi(A,B)
		theta(A,B)
		gamma(A,B)

sep, 2017.
'''
import numpy as np
from itertools import combinations as cb


class operadores:
	"""Operadores"""
	def __init__(self, A,B):
		self.A=A[0]
		self.B=B[0]
		self.TTA=A[1]
		self.TTB=B[1]
		self.ttm=[]
		self.ttm_aux =[]
		self.matriz=[]
 
	def concatena(self,a,b):
		aux=a[:]
		for i in b:
			aux.append(i)
		return aux
 
	def phi_aux(self,mA,mO,exp,ind):
		"""Genera la matriz del operador fi."""
		m_aux=[]
		if exp == ind:
			self.matriz = mA
		else:
			for row,i in zip(mA,mO):
				fila = self.concatena(row,i)
				m_aux.insert(0,fila)
			m_aux.reverse()
			self.phi_aux(m_aux,mO,exp,ind+1)
 
	def obtenerClasesEqu(self, test, lA, exp):
		clases = []
		for x in range(1, exp):
			clases. insert(0, [i + (lA * x) for i in test])
		clases.reverse()
		return clases   
 
	def sustituir(self, testor, listPos, clasesEq, listTest):
		test = testor[:]
		if listPos == []:
			self.ttm_aux = listTest
		else:
			pos = listPos[0]
			for clase in clasesEq:
				test[pos] = clase[pos]
				if len(listPos) == 1:
					t = test[:]
					self.sustituir(test, [], clasesEq, listTest)
				else:
					lp=listPos[:]
					lp.pop(0)
					self.sustituir(test, lp, clasesEq, listTest)
			
			
	def obtenerPosiciones(self, tamTest):
		listPos = []
		test = list(range(tamTest))     
		for el in range(1, len(test) + 1) :
			aux = list(cb(test, el))
			listPos.extend(aux)
		return listPos
 
	def phiTT (self, mA, ttA, exp):
		"""Genera los testores típicos del operador fi."""
		tt_aux = []
		for tt in ttA:
			tt_aux.insert(0, tt)
			clasesEqui = self.obtenerClasesEqu(tt, len(mA[0]), exp)
			listaPos = self.obtenerPosiciones(len(tt))
			for lp in listaPos:
				lp_aux = list(lp)
				self.sustituir(tt, lp_aux, clasesEqui, [])
				tt_aux.extend(self.ttm_aux)
		self.ttm = tt_aux
 
	def phi(self, exp):
		"""Función principal del operador fi."""
		A=self.A
		self.phi_aux(A,A,exp,1)
		self.phiTT(A,self.TTA,exp)

	def theta(self):
		"""Genera la matriz del operador theta."""
		mA = self.A
		mB = self.B
		m_aux=[]
		for rowA in mA:
			for rowB in mB:
				fila=self.concatena(rowA,rowB)
				m_aux.insert(0,fila)
		m_aux.reverse()
		self.matriz=m_aux
		self.thetaTT(self.A,self.TTA,self.TTB)
		
	def thetaTT(self, mA, ttA, ttB):
		"""Genera los testores típicos del operador theta."""
		ttm_aux = ttA[:]
		lA=len(mA[0])
		for e in ttB:
			ttm_aux.insert(0, [x + lA for x in e])
		self.ttm = ttm_aux
 
	def gamma_aux(self,mA,mB,lA,lB):
		"""Genera la matriz del operador gamma."""
		m_aux=[]
		for rowA in mA:
			fila=self.concatena(rowA,lB)
			m_aux.insert(0,fila)
		for rowB in mB:
			fila=self.concatena(lA,rowB)
			m_aux.insert(0,fila)
		m_aux.reverse()
		self.matriz=m_aux
 
	def gamma(self):
		"""Función principal del operador gamma."""
		mA=self.A
		mB=self.B
		lA=[0]*len(mA[0])
		lB=[0]*len(mB[0])
		self.gamma_aux(mA,mB,lA,lB)
		self.gammaTT(mA,self.TTA,self.TTB)
		
	def gammaTT(self, mA, ttA, ttB):
		"""Genera los testores típicos del operador gamma."""
		tt_aux = []
		ttm_aux = []
		tt_sum = []
		lA = len(mA[0])
		for e in ttB:
			tt_sum = [x + lA for x in e]
			for e2 in ttA:
				tt_aux = e2[:]
				tt_aux.extend(tt_sum)
				ttm_aux.insert(0, tt_aux)
				ttm_aux.reverse()
		self.ttm = ttm_aux
	
if __name__ == '__main__':
	A=[
	[0,0,1,0,1,0],
	[1,1,0,0,0,0],
	[0,0,0,0,0,1],
	[1,0,0,0,1,0]]

	B=[
	[1,1,1,0],
	[0,1,1,1],
	[1,0,1,1]]

	TTA = [[1, 5, 6], [1, 3, 6], [2, 5, 6]]
	TTB = [[3], [1, 2], [1, 4], [2, 3]]

	ops=operadores([B,TTB],[[],[]])
	ops.phi(2)
	m=np.array(ops.matriz)
	ttm=np.array(ops.ttm)
	print("matriz:")
	print(m)
	print("TTm("+str(len(ttm))+"):")
	print(ttm)


