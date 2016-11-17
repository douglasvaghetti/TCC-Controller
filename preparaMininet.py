from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import Controller, RemoteController
from roteamento import criaRotas
from grafo import Grafo
from dadosGrafo import grafo, defs
import sys
from mininet.link import TCLink
import random
import os
import time
from mininet.cli import CLI
import sflow

if __name__ == "__main__":
    print "instanciando topologia"
    topologia = Grafo(grafo, defs)
    net = topologia.net

    print "instanciando controladores para os PTTs"
    n = 0
    controladoresPorSW = {}
    os.system(
        "/home/mininet/pox/pox.py log.level --ERROR openflow.of_01 --port=%d --address=10.0.0.5  forwarding.l2_learning  &"
        % (6634))
    os.system(
        "/home/mininet/pox/pox.py log.level --ERROR openflow.of_01 --port=%d --address=10.0.0.5 misc.matador_de_passarinho --webServerPort=%d &"
        % (6635, 6670))
    time.sleep(1)
    c1 = net.addController(
        'c1', port=6634, controller=RemoteController, ip="10.0.0.5")
    c2 = net.addController(
        'c2', port=6635, controller=RemoteController, ip="10.0.0.5")
    print "vai dar net.build"
    net.build()
    print "fim do net.build"

    c1.start()
    c2.start()
    #time.sleep(5)

    print "inciando os switches"
    for switch in net.switches:
        #print "iniciando ", switch.name
        if switch.name[:3] == "PTT":
            switch.start([c2])
            #print ">>>>>instanciando switch com matador de passarinho"
        else:
            #print ">>>>instanciando switch sem matador de passarinho"
            switch.start([c1])
        #time.sleep(1)
    print "terminou de iniciar os switches"

    print "criando rotas"
    criaRotas(net, grafo, topologia, defs)
    print "terminou de criar rotas"

    print "inicializando sflow"
    collector = '127.0.0.1'
    (ifname, agent) = sflow.getIfInfo(collector)
    sflow.configSFlow(net, collector, ifname)
    sflow.sendTopology(net, agent, collector)

    print "inicializou sflow"
    #time.sleep(5)

    print "ativando monitoramento"
    diretorio = sys.argv[1] + "/dados"
    ipsHostsProvedores = [
        i.intfs[0].ip for i in net.hosts
        if i.name[:2] == "CP" and "H" in i.name or "V" in i.name
    ]
    ipsHostsVitimas = [
        i.intfs[0].ip for i in net.hosts
        if i.name[:2] == "CP" and "V" in i.name
    ]
    #print "ips dos hosts provedores = ",ipsHostsProvedores
    for host in net.hosts:  #routers tambem sao hosts
        interfaces = [i.name for i in host.intfs.values()]
        #print "./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces))
        if host.name[:3] == "ISP":
            if "H" in host.name:  #se eh host normal, ex: ISPXHY
                host.cmd("./simulaHostConsumidor.sh '%s' &" %
                         (" ".join(ipsHostsProvedores)))
            elif "A" in host.name:  # se eh host agressor, ex: ISPXAY
                host.cmd("sleep 10s && sleep $[ ( $RANDOM %% 30 ) + 1 ]s && ./udp -h %s -ts 2ms > /dev/null &" %
                         (random.choice(ipsHostsVitimas)))
            elif len(host.name) == 4:
                pass
                #host.cmd("./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces)))
        elif host.name[:2] == "CP":
            if len(host.name) == 5:
                host.cmd("./webfsd -p80")
            elif len(host.name) == 3:
                pass
                #host.cmd("./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces)))
        elif host.name[:2] == "TP":
            pass
            #host.cmd("./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces)))

    print "monitoramento ativado em todos os hosts"

    #print "Dumping host connections"
    #dumpNodeConnections(net.hosts)
    #net.pingAll(timeout=0.1)
    print "tudo ok"
    #net.pingAll(timeout=0.2)
    CLI(net)
    #net.pingAll(timeout=0.1)
    print "fim"
    net.stop()
