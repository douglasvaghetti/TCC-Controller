import requests
from time import sleep
import sys, os

if len(sys.argv) != 2 :
	print 'Numero de parametros incorreto'
	os._exit()

nomeArquivo = sys.argv[1]

f = open(nomeArquivo,'w')
f.write('dados = {}\n')
f.write('dados["malicioso"] = []\n')
f.write('dados["legitimo"] = []\n')
f.close()
sleep(5)

while True :
	r = requests.get("http://127.0.0.1:8008/app/dashboard-example/scripts/metrics.js/metric/json")
	try:	
		icmp = r.json()['top-5-protocols']['eth.ip.icmp']
	except:
		icmp = 0
	try:
		tcp = r.json()['top-5-protocols']['eth.ip.tcp']
	except:
		tcp = 0
	f = open(nomeArquivo,'a')
	f.write('dados["malicioso"].append('+str(icmp)+')\n')
	f.write('dados["legitimo"].append('+str(tcp)+')\n')
	f.close()
	sleep(1)
