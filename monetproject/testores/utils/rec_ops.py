# -*- coding: utf-8 -*-
from catalogo import read_csv_file
from operadores import operadores


def recorrido(arbol, pila, dic):
        if "expr" in arbol.keys():
                pila = conc(arbol["expr"], pila)
                op = arbol["val"].lower()
                if op == 'p':
                        obj = operadores(recorrido(pila[0], [], dic), [[], []])
                        aplica_operador(obj, op, pila[1]["val"])
                else:
                        obj = operadores(recorrido(pila[0], pila[1:], dic),
                                         recorrido(pila[1], [], dic))
                        aplica_operador(obj, op)
                return [obj.matriz, obj.ttm]
        else:
                return [dic[arbol["val"].lower()]["mat"],
                        dic[arbol["val"].lower()]["tt"]]


def aplica_operador(obj, op, n=None):
        if op == 't':
                obj.theta()
        elif op == 'p':
                obj.phi(n)
        elif op == 'g':
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
               "ref": "Matriz resultante"}
        return dic


def solve(var, catalogo):
        #dic = read_csv_file("datos.csv")
        r = recorrido(var, [], catalogo)
        return to_dic(r)


if __name__ == '__main__':
        d = {"val": "G", "tipo": "Op",
             "expr": [{"val": "minima", "tipo": "Mat"},
                      {"val": "P", "tipo": "op",
                       "expr": [{"val": "aurora", "tipo": "Mat"},
                                {"val": 2, "tipo": "Int"}]}]}
        print(solve(d))
