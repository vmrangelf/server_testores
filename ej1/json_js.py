#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json()
	result = ''
	#print(data)
	for item in data:
		#loop over every row
		print(item)
		result += str(item['make']) + '\n'

	return result
	#return 'ok'
	
@app.route('/obtDatos', methods = ['POST'])
def obtDatos():
	# read json + reply
	response = {'status' : 'ok', 'prueba' : '1'}
	return json.dumps(response)

if __name__ == '__main__':
	# run!
	app.run()