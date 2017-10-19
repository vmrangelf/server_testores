import csv
from ast import literal_eval

data=[]
dic={}
def read_csv_file(filename):
	f=open(filename)
	for row in csv.reader(f):
		data.insert(0,row)
	f.close()
	data.pop()
	to_dict(data)

def to_dict(data):
	for row in data:
		name=row.pop(0)
		dic[name]={"mat":0,"tt":0,"ref":0}
		parton=["mat","tt","ref"]
		for p,el in zip(parton,row):
			if p == "ref":
				dic[name][p]=el
			else:
				dic[name][p]=literal_eval(el)

if __name__ == '__main__':
	read_csv_file("datos.csv")
	print(dic)