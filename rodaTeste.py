from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from roteamento import prepara
from grafo import Grafo

if __name__ == "__main__":

    defs = {}
    defs["PTT1"] = 1
    defs["PTT2"] = 2
    defs["AS1"] = (1,2) #prefixo 33, 10 hosts
    defs["AS2"] = (2,2)
    defs["AS3"] = (3,2)
    defs["AS4"] = (4,2)
    defs["AS5"] = (5,2)
    defs["AS6"] = (6,2)
    defs["AS7"] = (7,2)
    defs["AS8"] = (8,2)
    defs["AS9"] =(9,2)

    grafo = {}
    grafo["PTT1"] = ["AS1","AS6","AS2"]
    grafo["PTT2"] = ["AS3","AS7","AS2"]
    grafo["AS1"] = ["PTT1","AS8"]
    grafo["AS2"] = ["PTT1","PTT2","AS9"]
    grafo["AS3"] = ["AS4","AS5","PTT2"]
    grafo["AS4"] = ["AS3"]
    grafo["AS5"] = ["AS3"]
    grafo["AS6"] = ["PTT1"]
    grafo["AS7"] = ["PTT2"]
    grafo["AS8"] = ["AS1"]
    grafo["AS9"] = ["AS2"]

    # grafo = {}
    # grafo["PTT1"] = ["AS1","AS2"]
    # grafo["AS1"] = ["PTT1","AS3"]
    # grafo["AS2"] = ["PTT1"]
    # grafo["AS3"] = ["AS1"]
    #
    # defs = {}
    # defs["PTT1"] = 1
    # defs["AS1"] = (1,2) #prefixo 33, 10 hosts
    # defs["AS2"] = (2,2)
    # defs["AS3"] = (3,2)

    topologia = Grafo(grafo,defs)
    net = Mininet(topologia)
    print "vai startar"
    net.start()
    print "vai preparar"
    prepara(net,grafo,topologia,defs)

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "tudo ok"
    net.interact()
    net.stop()