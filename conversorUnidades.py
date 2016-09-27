#!/usr/bin/env python

def converte(numero):
	numeros = set([str(x) for x in range(10)])
	if numero[-2] not in numeros:
		unidade = numero[-2]
		#print "convertendo unidade",unidade
		if unidade == 'K':
			numero = float(numero[:-2])*1024
		elif unidade == 'M':
			numero = float(numero[:-2])*1024**2
		elif unidade == 'G':
			numero = float(numero[:-2])*1024**3
		return numero
	else:
		return float(numero[:-1])

while True:
	try:
		linha1 = raw_input()
	except:
		#print "deu break direto"
		break
	linha2 = raw_input()	
	#print "leu",linha1,"\n",linha2
	ipOrig,ipDest = linha1.split()[1], linha2.split()[0]
	n1,n2 = [x.split()[-1] for x in [linha1,linha2]]
	print ipOrig,ipDest,converte(n1),converte(n2)
		
	
