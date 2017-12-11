# -*- coding: utf-8 -*-
from catalogo import read_csv_file


def recorrido(arbol, pila, dic):
    if "expr" in arbol.keys():
        pila = conc(arbol["expr"], pila)
        op = arbol["val"].lower()
        if op in ['p', 'g', 'g']:
            if op == 'p':
                return (recorrido(pila[0], [], dic) and
                        (type(pila[1]["val"]) == int))
            else:
                return (recorrido(pila[0], pila[1:], dic) and
                        recorrido(pila[1], [], dic))
        else:
            return False
    else:
        if arbol["val"].lower() in dic.keys():
            return True
        else:
            return False


def conc(lista1, lista2):
    l1 = lista1[:]
    l2 = lista2[:]
    l1.reverse()
    for el in l1:
        l2.insert(0, el)
    return l2


def validar(var):
    dic = read_csv_file("datos.csv")
    r = recorrido(var, [], dic)
    return r


if __name__ == '__main__':
    d = {"val": "g", "tipo": "Op",
         "expr": [{"val": "minIma", "tipo": "Mat"},
                  {"val": "p", "tipo": "op",
                   "expr": [{"val": "aurora", "tipo": "Mat"},
                            {"val": 2, "tipo": "Int"}]}]}
    print(validar(d))
