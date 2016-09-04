from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()
gateway = {}
RedesPublicasPorAS = {}
class Grafo(Topo):
    def build(self,grafo,defs):
        grafoAciclico = self.tiraAmbiguidades(grafo)
        nodosReais = {}

        #cria os nodos no mininet
        for nodo in grafoAciclico:
            #print "processando nodo ",nodo
            if nodo[:2] == "AS":
                nodosReais[nodo] = self.makeAS(defs[nodo][0],defs[nodo][1])
            elif nodo[:3] == "PTT":
                nodosReais[nodo] = self.makePTT(defs[nodo])
            else:
                raise "tem algo errado no grafo! :"+nodo
        # print "nodos reais = ",nodosReais
        # print "hosts = ",self.hosts()
        # print "switches = ",self.switches()

        global gateway
        global RedesPublicasPorAS
        # #cria os links com PTTs
        contadorRedes = 1
        for PTT,ASsAdjacentes in filter(lambda x: x[0][:3] == "PTT", grafo.items()):
            for i,ASAdjacente in enumerate(ASsAdjacentes):
                IPPublicoASNaRede = "172.16.%d.%d/24"%(contadorRedes,i+1)

                #print "adicionou link entre %s e %s"%(PTT,ASAdjacente)
                self.addLink(nodosReais[PTT],nodosReais[ASAdjacente],params2={'ip':IPPublicoASNaRede,'pudim':'10.0.%s.1'%ASAdjacente})
                for outroAS in ASsAdjacentes:
                    gateway[(ASAdjacente,outroAS)] = IPPublicoASNaRede[:-3] #o gateway dos outros ASs no PTT para este AS eh seu IP no PTT

                redePublica = "172.16.%d.0/24"%contadorRedes
                if ASAdjacente not in IPPublicoASNaRede:
                    RedesPublicasPorAS[ASAdjacente] = [redePublica]
                else:
                    RedesPublicasPorAS[ASAdjacente].append(redePublica)

            contadorRedes+=1

        for AS,ASsAdjacentes in filter(lambda x: x[0][:2] == "AS", grafoAciclico.items()):
            for ASAdjacente in filter(lambda x: x[:2]=="AS",ASsAdjacentes):
                IPPublicoASNaRede1 = "172.16.%d.1/24"%(contadorRedes)
                IPPublicoASNaRede2 = "172.16.%d.2/24"%(contadorRedes)

                #print "adicionou link entre %s e %s usando a rede 172.16.%d.X"%(AS,ASAdjacente,contadorRedes)
                self.addLink(nodosReais[AS],nodosReais[ASAdjacente],params1={'ip':IPPublicoASNaRede1},params2={'ip':IPPublicoASNaRede2})
                gateway[(ASAdjacente,AS)] = IPPublicoASNaRede2[:-3] # o gateway para ASadjancente a partir do AS eh o ip dele na sua ligacao
                gateway[(AS,ASAdjacente)] = IPPublicoASNaRede1[:-3] # e o contrario tambem

                redePublica = "172.16.%d.0/24"%contadorRedes
                if AS not in RedesPublicasPorAS:
                    RedesPublicasPorAS[AS] = [redePublica]
                else:
                    RedesPublicasPorAS[AS].append(redePublica)

                if ASAdjacente not in RedesPublicasPorAS:
                    RedesPublicasPorAS[ASAdjacente] = [redePublica]
                else:
                    RedesPublicasPorAS[ASAdjacente].append(redePublica)

                contadorRedes+=1
        #print "fim do build"

    def tiraAmbiguidades(self,grafo):
        semAmbiguidade = {}
        jaLinkou = set()
        for origem,destinos in grafo.items():
            semAmbiguidade[origem] = []
            for destino in destinos:
                if (origem,destino) in jaLinkou or (destino,origem) in jaLinkou:
                    pass
                else:
                    jaLinkou.add((origem,destino))
                    semAmbiguidade[origem].append(destino)
        return semAmbiguidade

    def makePTT(self,prefixo):
        return self.addSwitch("PTT%d"%prefixo)

    def makeAS(self,prefixo,tamanho):
        prefixo = prefixo
        ipRouter = "10.0.%d.1/24"%prefixo

        router = self.addHost("AS%d"%prefixo,cls=LinuxRouter,ip=ipRouter)
        switch = self.addSwitch("AS%dsw"%prefixo)
        self.addLink(switch,router)

        for i in range(tamanho):
            ipHost = "10.0.%d.%d/24"%(prefixo,i+2) #pula o zero e o router
            host = self.addHost("AS%dH%d"%(prefixo,i),ip=ipHost,defaultRoute="via 10.0.%d.1"%prefixo)
            #print "ligando host ",host,"com switch",switch," ip = ",ipHost
            link = self.addLink(switch,host)
        #print "terminou makeAS de %d"%prefixo
        return router

visitados = None

def prepara(net,grafo):
    routersASs = filter(lambda x: x.name[:2]=='AS',net.hosts)
    routersReais = {}
    for nomeAS,defsAS in filter(lambda x: x[0][:2]=="AS",defs.items()):
        routersReais[nomeAS] = net['AS%d'%(defsAS[0])]
    global visitados
    rotas = {}
    for nomeAS, router in routersReais.items():
        #print "determinando rotas de ",nomeAS
        visitados = set()
        for adjacencia in grafo[nomeAS]:
            #print "\n\ndeterminando rotas de ",nomeAS,"a partir de ",adjacencia

            visitados.add(nomeAS)
            if adjacencia[:3] == "PTT":
                visitados.add(adjacencia)
                for vizinhoDoPTT in grafo[adjacencia]:
                    if vizinhoDoPTT not in visitados:
                        rotas[(nomeAS,vizinhoDoPTT)] = listaAlcancaveis(grafo,vizinhoDoPTT)
            else:
                rotas[(nomeAS,adjacencia)] = listaAlcancaveis(grafo,adjacencia)
            #rotas[(origem,vizinho)] = ASs que podem ser alcancadas a partir de origem atravez de vizinho
    global gateway
    global RedesPublicasPorAS
    # print "limpando rotas originais do mininet"
    # print "#######\nrotas########gerson"
    # print rotas
    #
    # print "#######\ngateway########"
    # print gateway
    # print "#######\n redes publicas por AS########"

    #print RedesPublicasPorAS
    for origem,vizinho in rotas:
        router = routersReais[origem]
        gatewayVizinho = gateway[(vizinho,origem)]
        # print "#### criando rotas de %s"%origem
        for destinoPossivel in rotas[(origem,vizinho)]:
            prefixoDestinoPossivel = defs[destinoPossivel][0]
            #print "rodando ","route add -net 10.0.%d.0/24 gw %s"%(prefixoDestinoPossivel,gatewayVizinho)
            router.cmd("route add -net 10.0.%d.0/24 gw %s"%(prefixoDestinoPossivel,gatewayVizinho))
            for redePublica in RedesPublicasPorAS[destinoPossivel]:
                if destinoPossivel != vizinho:
                    #print "rodando chinelagem","route add -net %s gw %s"%(redePublica,gatewayVizinho)
                    router.cmd("route add -net %s gw %s"%(redePublica,gatewayVizinho))
            #adiciona uma rota para cada rede publica que o AS alvo se conecta (isso acaba criando rotas inuteis mas funciona)
            #tambem adiciona varias rotas iguais, ja que faz isso uma vez para cada host dentro de uma mesma rede
            #nao importa, funciona

def listaAlcancaveis(grafo,origem):
    global visitados
    visitados.add(origem)
    alcancados = set()
    alcancados.add(origem)
    #print "visitados = ",visitados
    #print "visitando ",origem
    for vizinho in grafo[origem]:
        #print "vizinho = ",vizinho
        if vizinho not in visitados:
            visitados.add(vizinho)
            if vizinho[:3] == "PTT":
                #print "####entrei no for do PTT"
                for vizinhoDoPTT in grafo[vizinho]:
                    if vizinhoDoPTT not in visitados:
                        alcancados = alcancados | listaAlcancaveis(grafo,vizinhoDoPTT)
                #print "####sai do for do PTT"
            else:
                alcancados = alcancados | listaAlcancaveis(grafo,vizinho)
            #adiciona a lista de alcancados todos que foram alcancados por este vizinho
    #print "listador retornando",alcancados,"da visita de ",origem
    return alcancados

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


    net = Mininet(Grafo(grafo,defs))
    print "vai startar"
    net.start()
    print "vai preparar"
    prepara(net,grafo)

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "tudo ok"
    net.interact()
    net.stop()
