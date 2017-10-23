import csv
from ast import literal_eval


def read_csv_file(filename):
	dic={}
	data=[]
	f=open(filename)
	for row in csv.reader(f):
		data.insert(0,row)
	f.close()
	data.pop()
	dic=to_dict(data)
	return dic

def to_dict(data):
	dic={}
	for row in data:
		name=row.pop(0)
		dic[name]={"mat":0,"tt":0,"ref":0}
		parton=["mat","tt","ref"]
		for p,el in zip(parton,row):
			if p == "ref":
				dic[name][p]=el
			else:
				dic[name][p]=literal_eval(el)
	return dic

if __name__ == '__main__':
	dic=read_csv_file("datos.csv")
	rint(dic)