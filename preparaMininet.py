from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from roteamento import criaRotas
from grafo import Grafo
from dadosGrafo import grafo,defs
import sys
from mininet.link import TCLink
import random



if __name__ == "__main__":

    print "instanciando topologia"
    topologia = Grafo(grafo,defs)
    net = Mininet(topologia,link=TCLink)
    ipsNaMao = topologia.ipsNaMao
    print "botando ips na mao"
    for AS,IPsPorIntf in ipsNaMao.items():
        for intf,IP in IPsPorIntf.items():
            net.get(AS).intfs[intf].setIP(IP)

    print "vai startar"
    net.start()
    print "criando rotas"
    criaRotas(net,grafo,topologia,defs)
    print "terminou de criar rotas"

    print "ativando monitoramento"
    diretorio = sys.argv[1]+"/dados"
    ipsHostsProvedores = [i.intfs[0].ip for i in net.hosts if i.name[:2] == "CP" and "H" in i.name or "V" in i.name]
    ipsHostsVitimas = [i.intfs[0].ip for i in net.hosts if i.name[:2] == "CP" and "V" in i.name]
    #print "ips dos hosts provedores = ",ipsHostsProvedores
    for host in net.hosts: #routers tambem sao hosts
        interfaces = [i.name for i in host.intfs.values()]
        #print "./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces))
        if host.name[:3] == "ISP":
            if "H" in host.name: #se eh host normal, ex: ISPXHY
                host.cmd("./simulaHostConsumidor.sh '%s' &"%(" ".join(ipsHostsProvedores)))
            elif "A" in host.name: # se eh host agressor, ex: ISPXAY
                host.cmd("ping -i 0.005 -s 1000 %s > /dev/null &"%(random.choice(ipsHostsVitimas)))
        elif host.name[:2] == "CP":
            host.cmd("./webfsd -p80")
        host.cmd("./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces)))
    print "monitoramento ativado em todos os hosts"

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "tudo ok"
    net.interact()
    net.stop()
