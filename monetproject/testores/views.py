# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from testores.utils.catalogo import read_csv_file
from testores.utils.operadores import operadores
from testores.utils.rec_ops import solve
from testores.utils.validacion import validar
from testores.utils.main import convertirMatriz
import json
from django.http import JsonResponse
import ast
# Create your views here.
catalogo = read_csv_file('testores/utils/datos.csv')

def index (request):
	template = loader.get_template('testores/index.html')
	#catalogo = read_csv_file('testores/utils/datos.csv')
	context = {'id_list': catalogo.keys(),}
	return HttpResponse(template.render(context, request))

def obtenerMatriz(request):
	selectedValue = request.GET.get('selectedValue', None)
	#catalogo = read_csv_file('testores/utils/datos.csv')
	data = catalogo.get(selectedValue)
	return JsonResponse(json.dumps(data), safe=False)

def obtenerHipergrafoCatalogo(request):
	selectedValue = request.GET.get('selectedValue')
	centro = ast.literal_eval(request.GET.get('centro'))
	repeticion = ast.literal_eval(request.GET.get('repeticion'))
	#print(selectedValue) 
	#print(type(centro)) 
	#print(repeticion)
	data = catalogo.get(selectedValue)
	matHyp = {"matriz": data.get('mat'),}
	matHypergrafo = convertirMatriz(matHyp, centro, repeticion)
	#print(matHypergrafo)
	#response = {'prueba': 'json',}
	return JsonResponse(json.dumps(matHypergrafo), safe=False)

def obtenerHipergrafoResultante(request):
	matrizBasica = request.GET.get('matrizBasica')
	body = ast.literal_eval(matrizBasica)
	matHyp = {"matriz": body['data'],}
	centro = ast.literal_eval(request.GET.get('centro'))
	repeticion = ast.literal_eval(request.GET.get('repeticion'))
	matHypergrafo = convertirMatriz(matHyp, centro, repeticion)
	return JsonResponse(json.dumps(matHypergrafo), safe=False)

def operacionPhi(request):
	selectedValue = request.GET.get('selectedValue', None)
	exp = int(request.GET.get('exp', None))
	#catalogo = read_csv_file('testores/utils/datos.csv')
	data = catalogo.get(selectedValue)
	ops = operadores(data.get('mat'), data.get('tt'))
	ops.fi(data.get('mat'), exp)
	response = {'matrizBasica': ops.matriz,
			    'testoresTipicos': ops.ttm,}
	return JsonResponse(json.dumps(response), safe=False)
	
def calcularMB(request):	
	jsonReq = request.GET.get('content')
	body = ast.literal_eval(jsonReq)
	if(validar(body, catalogo)):
		response = solve(body, catalogo)
	else:
		response = {'Error': 'true'}
	#print("Resp")
	#print(response)
	return JsonResponse(json.dumps(response), safe=False)
	

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
	
