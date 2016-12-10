import requests
from time import sleep
import sys, os
import subprocess
from os import listdir
import time

execfile("../dadosGrafo" + sys.argv[1] + ".py")

listaPTTs = [x for x in grafo.keys() if x[:3] == "PTT"]

f = open("acumulado.py", 'w')
f.write('dados = {}\n')
f.write('dados["malicioso"] = []\n')
f.write('dados["legitimo"] = []\n')
f.write('dados["regras"] = []\n')
f.write('dados["chegouMalicioso"] = []\n')
f.write('dados["chegouLegitimo"] = []\n')
f.write('dados["bloqueio"] = []\n')
f.close()
sleep(5)

while True:
    timestamp = int(time.time())

    r = requests.get(
        "http://127.0.0.1:8008/app/dashboard-example/scripts/metrics.js/metric/json"
    )
    try:
        icmp = r.json()['top-5-protocols']['eth.ip'] / 1024**2
    except:
        icmp = 0
    try:
        tcp = r.json()['top-5-protocols']['eth.ip.tcp'] / 1024**2
    except:
        tcp = 0

    NRegras = {}
    for ptt in listaPTTs:
        proc = subprocess.Popen(
            ["ovs-ofctl dump-flows %s | wc -l" % ptt],
            stdout=subprocess.PIPE,
            shell=True)
        (out, err) = proc.communicate()
        #print "erro:",err
        NRegras[ptt] = int(out)
    r = requests.get("http://127.0.0.1:8008/app/mininet-dashboard/scripts/metrics.js/metric/json")
    try:
        maliciosoNaVitima = 0 
        legitimoNaVitima = 0 
        todasInterfaces = r.json()["top-5-flows"]
        #print "todasInterfaces = ",todasInterfaces
        for chave in [i for i in todasInterfaces.keys() if i[:len("CP1sw")] == "CP1sw" and (i[-3:] == "udp" or i[-2:] == "ip" or i[-3:] == "http" or i[-3:] == "tcp")]:
            if chave[-3:] == "udp" or chave[-2:] == "ip" :
                maliciosoNaVitima += r.json()["top-5-flows"][chave] / 1024**2
            else :
                legitimoNaVitima += r.json()["top-5-flows"][chave] / 1024**2
        #print "calculou chegouNaVitima = ",chegouNaVitima
    except:
        maliciosoNaVitima = 0 
        legitimoNaVitima = 0 

    icmp = str(icmp)
    tcp = str(tcp)
    #NRegras = str(NRegras)
    maliciosoNaVitima = str(maliciosoNaVitima)
    legitimoNaVitima = str(legitimoNaVitima)

    f = open("acumulado.py", 'a')
    f.write('dados["malicioso"].append((%s,%d))\n'%(icmp,timestamp))
    f.write('dados["legitimo"].append((%s,%d))\n'%(tcp,timestamp))
    for ptt in NRegras:
        f.write('dados["regras"].append((%s,"%s",%d))\n'%(NRegras[ptt],ptt,timestamp))
    f.write('dados["chegouMalicioso"].append((%s,%d))\n'%(maliciosoNaVitima,timestamp))
    f.write('dados["chegouLegitimo"].append((%s,%d))\n'%(legitimoNaVitima,timestamp))
    #print "icmp = ",icmp,"tcp=",tcp,"NRegras=",NRegras
    f.close()
    sleep(1)
