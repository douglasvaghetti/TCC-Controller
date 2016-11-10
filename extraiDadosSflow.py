import requests
from time import sleep
import sys, os
import subprocess
from os import listdir

execfile("../dadosGrafo.py")

listaPTTs = [x for x in grafo.keys() if x[:3] == "PTT"]

f = open("acumulado.py", 'w')
f.write('dados = {}\n')
f.write('dados["malicioso"] = []\n')
f.write('dados["legitimo"] = []\n')
f.write('dados["regras"] = []\n')
f.close()
sleep(5)

while True:
    r = requests.get(
        "http://127.0.0.1:8008/app/dashboard-example/scripts/metrics.js/metric/json"
    )
    try:
        icmp = r.json()['top-5-protocols']['eth.ip.icmp'] / 1024**2
    except:
        icmp = 0
    try:
        tcp = r.json()['top-5-protocols']['eth.ip.tcp'] / 1024**2
    except:
        tcp = 0

    NRegras = 0
    for ptt in listaPTTs:
        proc = subprocess.Popen(
            ["ovs-ofctl dump-flows %s | wc -l" % ptt],
            stdout=subprocess.PIPE,
            shell=True)
        (out, err) = proc.communicate()
        #print "erro:",err
        NRegras += int(out)

    f = open("acumulado.py", 'a')
    f.write('dados["malicioso"].append(' + str(icmp) + ')\n')
    f.write('dados["legitimo"].append(' + str(tcp) + ')\n')
    f.write('dados["regras"].append(' + str(NRegras) + ")\n")
    #print "icmp = ",icmp,"tcp=",tcp,"NRegras=",NRegras
    f.close()
    sleep(1)
