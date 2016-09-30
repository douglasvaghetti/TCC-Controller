#!/usr/bin/env python
import time
import sys
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
	if linha1 == "Terminated":
		break
	linha2 = raw_input()
	#print "leu",linha1,"\n",linha2
	ipOrig,ipDest = linha1.split()[1], linha2.split()[0]
	nomeDoHost = sys.argv[1]
	nomeDaInterface = sys.argv[2]

	n1,n2 = [x.split()[-1] for x in [linha1,linha2]]
	ipsIgnorados = set("255.255.255.255")
	if ipOrig not in ipsIgnorados and ipDest not in ipsIgnorados:
		print 'host["%s"].append( ("%s","%s",%.2f,%.2f,%d) )'%(nomeDoHost,ipOrig,ipDest,converte(n1),converte(n2),int(time.time()))
