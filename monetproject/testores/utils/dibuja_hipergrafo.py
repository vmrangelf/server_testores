# -*- coding: utf-8 -*-
#!/usr/bin/python

#By Silva Peña Guillermo
#Descripcion: Generar el hipergrafo de manera grafica a través de la matriz de incidencia


# -------------------------------------------------------------------------------------
# ---------------------------- Librerias ----------------------------------------------
# -------------------------------------------------------------------------------------

import os
import random
import json
import types

# -------------------------------------------------------------------------------------
# ---------------------------- Definición Clase ---------------------------------------
# -------------------------------------------------------------------------------------

class dibuja_hipergrafo:
	def __init__(self, nombre,con_repeticiones=True,con_centro=False):
		self.con_repeticiones = con_repeticiones
		self.con_centro = con_centro
		self.nombre_archivo = nombre
		self.hipergrafo = {
		"hyperedges":[],
		"links":[],
		"nodes": {}
		}
		if(self.con_centro):
			self.hipergrafo["nodes"]["centro"] = {"level":1,"word":""}
		return

	def dibuja_nodo(self,nodo,hiperarista):

		if(not self.con_repeticiones):
			self.hipergrafo["nodes"][str(nodo)+hiperarista] = {"level":3,"word":str(nodo)}
			return
		self.hipergrafo["nodes"][str(nodo)] = {"level":3,"word":str(nodo)}
		return

	def dibuja_hiperarista(self,hiperarista):
		self.hipergrafo["hyperedges"].append(hiperarista)
		self.hipergrafo["nodes"][hiperarista] = {"level":2,"word":hiperarista}
		if(self.con_centro):
			self.hipergrafo["links"].append({'parent': "centro", 'child': hiperarista})
		return

	def dibuja_relacion(self,nodo,hiperarista):
		if(not self.con_repeticiones):
			self.hipergrafo["links"].append({'parent': hiperarista, 'child': str(nodo)+hiperarista})
			return
		self.hipergrafo["links"].append({'parent': hiperarista, 'child': str(nodo)})

	def dibujar_hipergrafo(self,nodos,matriz):
		dic_nodos = {}
		for i in range(0,len(nodos)):
			dic_nodos[i]=nodos[i]

		for x in range(0,len(matriz)):
			id_hiperarista = "E"+str(x+1)
			self.dibuja_hiperarista(id_hiperarista)
			nodos_hiperarista = [dic_nodos[y] for y in range(len(matriz[x])) if matriz[x][y] == 1]
			for nodo in nodos_hiperarista:
				self.dibuja_nodo(nodo,id_hiperarista)
				self.dibuja_relacion(nodo,id_hiperarista)
		return

	def guardar_dibujo(self):
		with open(self.nombre_archivo+".json", 'w') as f:
			json.dump(self.hipergrafo, f, ensure_ascii=False)
