# -*- coding: utf-8 -*-
#!/usr/bin/python

# Desarrollador por: Silva Peña Guillermo
# Descripcion: Convertir matriz en json para archivo d3js

# -------------------------------------------------------------------------------------
# ---------------------------- Libraries ----------------------------------------------
# -------------------------------------------------------------------------------------

import os
import argparse
import json
from testores.utils.dibuja_hipergrafo import *

# -------------------------------------------------------------------------------------
# ---------------------------- Functions ----------------------------------------------
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# ---------------------------- Main Code ----------------------------------------------
# -------------------------------------------------------------------------------------

def convertirMatriz(matriz, centro, repeticion):
    matriz=matriz['matriz']
    vertices = ['v'+str(x+1) for x in range(len(matriz[0]))]
    dibuja = dibuja_hipergrafo("hipergrafo_Prueba",repeticion,centro)
    dibuja.dibujar_hipergrafo(vertices,matriz)
    return dibuja.hipergrafo

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--matriz',dest='matriz', nargs='+', help='Archivo con matriz binaria')
    parser.add_argument('--centro',dest='centro', help='Generar centro',action='store_true')
    parser.add_argument('--repeticion',dest='repeticion', help='Generar repetición en nodos',action='store_false')
    parser.set_defaults(centro=False,repeticion=True)
    args = parser.parse_args()

    if (args.matriz):
        with open(args.matriz[0],'r') as json_file:
            matriz = json.load(json_file)
    matriz=matriz['matriz']

    vertices = ['v'+str(x+1) for x in range(len(matriz[0]))]

    dibuja = dibuja_hipergrafo("hipergrafo_"+args.matriz[0].split(".")[0],args.repeticion,args.centro)
    dibuja.dibujar_hipergrafo(vertices,matriz)
    dibuja.guardar_dibujo()
    print("Listo!!!!")

