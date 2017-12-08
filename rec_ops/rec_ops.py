from catalogo import read_csv_file
from operadores import *


def recorrido(arbol, pila, dic):
        if "expr" in arbol.keys():
                pila = conc(arbol["expr"], pila)
                op = arbol["val"]
                if op == 'P':
                        obj = operadores(recorrido(pila[0], [], dic), [[], []])
                        aplica_operador(obj, op, pila[1]["val"])
                else:
                        obj = operadores(recorrido(pila[0], pila[1:], dic),
                                         recorrido(pila[1], [], dic))
                        aplica_operador(obj, op)
                return [obj.matriz, obj.ttm]
        else:
                return [dic[arbol["val"]]["mat"], dic[arbol["val"]]["tt"]]


def aplica_operador(obj, op, n=None):
        if op == 'T':
                obj.theta()
        elif op == 'P':
                obj.phi(n)
        elif op == 'G':
                obj.gamma()
        else:
                print("error")

def conc(lista1, lista2):
        l1 = lista1[:]
        l2 = lista2[:]
        l1.reverse()
        for el in l1:
                l2.insert(0, el)
        return l2

def to_dic(res):
        dic = {"mat": res[0], "tt": res[1],
               "ref": "Matriz resultente"}
        return dic


def solve(var):
        dic = read_csv_file("datos.csv")
        r = recorrido(var, [], dic)
        return to_dic(r)

if __name__ == '__main__':
        d = {"val": "G", "tipo": "Op",
             "expr": [{"val": "minima", "tipo": "Mat"},
                      {"val": "P", "tipo": "op", 
                      "expr": [{"val": "aurora", "tipo": "Mat"},{"val": 5, "tipo": "Int"}]}]}
        print(solve(d))
