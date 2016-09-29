from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from roteamento import criaRotas
from grafo import Grafo
from dadosGrafo import grafo,defs
import sys
from mininet.link import TCLink



if __name__ == "__main__":

    topologia = Grafo(grafo,defs)
    net = Mininet(topologia,link=TCLink)
    print "vai startar"
    net.start()
    print "criando rotas"
    criaRotas(net,grafo,topologia,defs)
    print "terminou de criar rotas"

    print "ativando monitoramento"
    diretorio = sys.argv[1]+"/dados"
    print (net.hosts[0].intfs[0].ip)
    ipsHostsProvedores = [i.intfs[0].ip for i in net.hosts if i.name[:2] == "CP" and "H" in i.name]
    print "ips dos hosts provedores = ",ipsHostsProvedores
    for host in net.hosts: #routers tambem sao hosts
        interfaces = [i.name for i in host.intfs.values()]
        #print "./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces))
        if host.name[:3] == "ISP":
            print host.cmd("./simulaHostConsumidor.sh '%s'&"%(" ".join(ipsHostsProvedores)))
        elif host.name[:2] == "CP":
            print host.cmd("./webfsd -p80")
        host.cmd("./monitoraDentroDoHost.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces)))
	#print host.cmd("python -m SimpleHTTPServer 80 &")
    print "monitoramento ativado em todos os hosts"

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "tudo ok"
    net.interact()
    net.stop()
