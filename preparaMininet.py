from mininet.net import Mininet
from mininet.util import dumpNodeConnections
#from mininet.node import Controller, RemoteController
from roteamento import criaRotas
from grafo import Grafo
from dadosGrafo import grafo,defs
import sys
from mininet.link import TCLink
import random
import os
import time



if __name__ == "__main__":

    print "instanciando topologia"
    topologia = Grafo(grafo,defs)
    net = topologia.net


    print "instanciando controladores para os PTTs"
    n = 0
    controladoresPorSW = {}
    #portas = range(6633,6633+len(topologia.SWsQueImplementamBloqueio))
    #SWs = list(topologia.SWsQueImplementamBloqueio)
    # os.system("/home/mininet/pox/pox.py log.level --DEBUG openflow.of_01 --port=%d --address=10.0.0.5 misc.matador_de_passarinho --webServerPort=%d &"%(56670,57670))
    # time.sleep(2)
    # controladorLiberado = net.addController('c%d'%n,controller=RemoteController,port=56670,ip='10.0.0.5')
    # print controladorLiberado

    #
    # for switch,porta in zip(SWs,portas):
    #     print "vai rodar /home/mininet/pox/pox.py log.level --DEBUG openflow.of_01 --port=%d misc.matador_de_passarinho --webServerPort=%d &"%(porta,porta+1000)
    #     os.system("/home/mininet/pox/pox.py log.level --DEBUG openflow.of_01 --port=%d --address=127.0.0.1 misc.matador_de_passarinho --webServerPort=%d &"%(porta,porta+1000))
    #     controlador = net.addController('c%d'%n,controller=RemoteController,port=porta,protocol='tcp',ip='127.0.0.1')
    #
    #     controladoresPorSW[switch] = controlador


    #print dir(teste),teste,type(teste)
    print "terminou instanciacao de controladores"

    print "vai dar net.build"
    net.build()
    print "fim do net.build"

    # print "inciando os controladores"
    # for controller in net.controllers:
    #     print ".",
    #     #controller.start()
    # print "iniciou os controladores"

    # print "inciando os switches"
    # for switch in net.switches:
    #     if switch.name in controladoresPorSW:
    #         switch.start([controladoresPorSW[switch.name]])
    #     else:
    #         print "switch ",switch.name,"liberado"
    #         switch.start([])
    # print "terminou de iniciar os switches"
    #time.sleep(5)



    # ipsNaMao = topologia.ipsNaMao
    # print "botando ips na mao"
    # for AS,IPsPorIntf in ipsNaMao.items():
    #     for intf,IP in IPsPorIntf.items():
    #         net.get(AS).intfs[intf].setIP(IP)


    print "criando rotas"
    criaRotas(net,grafo,topologia,defs)
    print "terminou de criar rotas"

    print "vai startar"
    net.start()

    #time.sleep(5)

    # print "ativando monitoramento"
    # diretorio = sys.argv[1]+"/dados"
    # ipsHostsProvedores = [i.intfs[0].ip for i in net.hosts if i.name[:2] == "CP" and "H" in i.name or "V" in i.name]
    # ipsHostsVitimas = [i.intfs[0].ip for i in net.hosts if i.name[:2] == "CP" and "V" in i.name]
    # #print "ips dos hosts provedores = ",ipsHostsProvedores
    # for host in net.hosts: #routers tambem sao hosts
    #     interfaces = [i.name for i in host.intfs.values()]
    #     #print "./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces))
    #     if host.name[:3] == "ISP":
    #         if "H" in host.name: #se eh host normal, ex: ISPXHY
    #             host.cmd("./simulaHostConsumidor.sh '%s' &"%(" ".join(ipsHostsProvedores)))
    #         elif "A" in host.name: # se eh host agressor, ex: ISPXAY
    #             host.cmd("ping -i 0.0005 -s 1000 %s > /dev/null &"%(random.choice(ipsHostsVitimas)))
    #     elif host.name[:2] == "CP":
    #         host.cmd("./webfsd -p80")
    #     host.cmd("./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces)))
    # print "monitoramento ativado em todos os hosts"

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "tudo ok"
    #net.pingAll(timeout=0.2)
    net.interact()
    net.stop()
