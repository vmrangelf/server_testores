import json
from catalogo import *
from operadores import *


def recorrido(arbol,pila):
	if "expr" in arbol.keys():
		pila=conc(arbol["expr"],pila);op=arbol["val"]
		if op == 'P':
			obj=operadores(recorrido(pila[0],[]),[[],[]])
			aplica_operador(obj,op,pila[1]["val"])
		else:
			obj=operadores(recorrido(pila[0],pila[1:]),recorrido(pila[1],[]))
			aplica_operador(obj,op)
		return [obj.matriz,obj.ttm]
	else:
		return [dic[arbol["val"]]["mat"], dic[arbol["val"]]["tt"]]

def aplica_operador(obj,op,n=None):
	if op == 'T':
		obj.theta()
	elif op == 'P':
		obj.phi(n)
	elif op == 'G':
		obj.gamma()
	else:
		print("error")

def conc(lista1,lista2):
	l1=lista1[:];l2=lista2[:]
	l1.reverse()
	for el in l1:
		l2.insert(0,el)
	return l2

if __name__ == '__main__':
	dic=read_csv_file("datos.csv")
	data = json.load(open('data4.json'))
	r=recorrido(data,[])
	print(r)