from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from roteamento import criaRotas
from grafo import Grafo
from dadosGrafo import grafo,defs
from monitoramento import ativaMonitoramento
import sys


if __name__ == "__main__":

    topologia = Grafo(grafo,defs)
    net = Mininet(topologia)
    print "vai startar"
    net.start()
    print "criando rotas"
    criaRotas(net,grafo,topologia,defs)
    print "terminou de criar rotas"

    print "ativando monitoramento"
    diretorio = sys.argv[1]+"/dados"
    for host in net.hosts: #routers tambem sao hosts
        interfaces = [i.name for i in host.intfs.values()]
        print "./monitora.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces))
        host.cmd("./monitora.sh %s %s '%s' &"%(diretorio,host.name," ".join(interfaces)))

    print "monitoramento ativado em todos os hosts"

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "tudo ok"
    net.interact()
    net.stop()