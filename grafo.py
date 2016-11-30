from mininet.link import TCLink#,TCIntf
from mininet.node import OVSSwitch,Controller
from mininet.net import Mininet




class Grafo():
    def __init__(self,grafo,defs):
        self.net = Mininet(build=False, topo=None,link = TCLink)
        self.SWsQueImplementamBloqueio = set()
        nodosReais = {}
        #cria os nodos no mininet
        for nodo in grafo:
            #print "processando nodo ",nodo
            if nodo[:3] == "ISP":
                nodosReais[nodo] = self.makeISP(prefixo=defs[nodo][0],tamanho=defs[nodo][1],n_agressores=defs[nodo][2],nome=nodo)
            elif nodo[:2] == "CP":
                nodosReais[nodo] = self.makeCP(prefixo=defs[nodo][0],tamanho=defs[nodo][1],n_vitimas=defs[nodo][2],nome=nodo)
            elif nodo[:2] == "TP":
                nodosReais[nodo] = self.makeTP(prefixo=defs[nodo][0],nome=nodo)
            elif nodo[:3] == "PTT":
                 nodosReais[nodo] = self.makePTT(prefixo=defs[nodo][0],implementaBloqueio=defs[nodo][1],nome=nodo)
            else:
                raise "tem algo errado no grafo! :"+nodo
            
            for vizinho in grafo[nodo]:
                if vizinho in nodosReais:
                    print "linkou ", nodo,"e",vizinho
                    self.net.addLink(nodosReais[nodo],nodosReais[vizinho])

    def makePTT(self,prefixo,implementaBloqueio,nome):
        if implementaBloqueio:
            self.SWsQueImplementamBloqueio.add(nome)
        return self.net.addSwitch(nome)

    def makeISP(self,prefixo,tamanho,n_agressores,nome):
        switch = self.net.addSwitch(nome+"sw")

        for i in range(tamanho):

            if i < n_agressores:
                ipHost = "10.0.%d.%d/16"%(prefixo,i+100) #pula o zero e o router
                host = self.net.addHost(nome+"A%d"%i,ip=ipHost)
            else:
                ipHost = "10.0.%d.%d/16"%(prefixo,i+2) #pula o zero e o router
                host = self.net.addHost(nome+"H%d"%i,ip=ipHost)
            #print "ligando host ",host,"com switch",switch," ip = ",ipHost
            linkopts = dict(bw=10)
            self.net.addLink(switch,host,**linkopts) #1 mga de banda por host

        #print "terminou makeAS de %d"%prefixo
        return switch

    def makeTP(self,prefixo,nome):
        switch = self.net.addSwitch(nome+"sw")

        return switch

    def makeCP(self,prefixo,tamanho,n_vitimas,nome):
        switch = self.net.addSwitch(nome+"sw")

        for i in range(tamanho):
            ipHost = "10.0.%d.%d/16"%(prefixo,i+2) #pula o zero e o router
            if i < n_vitimas:
                host = self.net.addHost(nome+"V%d"%i,ip=ipHost)
            else:
                host = self.net.addHost(nome+"H%d"%i,ip=ipHost)
            #print "ligando host ",host,"com switch",switch," ip = ",ipHost

            link = self.net.addLink(switch,host)

        #print "terminou makeAS de %d"%prefixo
        return switch