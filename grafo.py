from mininet.topo import Topo
from linuxRouter import LinuxRouter
from mininet.link import TCLink,TCIntf
from mininet.node import CPULimitedHost



class Grafo(Topo):
    def build(self,grafo,defs):
        grafoAciclico = self.tiraAmbiguidades(grafo)
        nodosReais = {}
        self.gateway = {}
        self.RedesPublicasPorAS = {}

        #cria os nodos no mininet
        for nodo in grafoAciclico:
            #print "processando nodo ",nodo
            if nodo[:3] == "ISP":
                nodosReais[nodo] = self.makeISP(prefixo=defs[nodo][0],tamanho=defs[nodo][1],n_agressores=defs[nodo][2],nome=nodo)
            elif nodo[:2] == "CP":
                nodosReais[nodo] = self.makeCP(prefixo=defs[nodo][0],tamanho=defs[nodo][1],n_vitimas=defs[nodo][2],nome=nodo)
            elif nodo[:2] == "TP":
                nodosReais[nodo] = self.makeTP(prefixo=defs[nodo][0],nome=nodo)
            elif nodo[:3] == "PTT":
                nodosReais[nodo] = self.makePTT(prefixo=defs[nodo][0],nome=nodo)
            else:
                raise "tem algo errado no grafo! :"+nodo
        # print "nodos reais = ",nodosReais
        # print "hosts = ",self.hosts()
        # print "switches = ",self.switches()


        self.ipsNaMao = {}
        for AS in grafoAciclico:
            self.ipsNaMao[AS] = {}

        # #cria os links com PTTs
        contadorRedes = 1
        for PTT,ASsAdjacentes in filter(lambda x: x[0][:3] == "PTT", grafo.items()):
            for i,ASAdjacente in enumerate(ASsAdjacentes):
                IPPublicoASNaRede = "172.16.%d.%d/24"%(contadorRedes,i+1)

                #print "adicionou link entre %s e %s"%(PTT,ASAdjacente)
                self.addLink(nodosReais[PTT],nodosReais[ASAdjacente])

                porta2 = self.linkInfo(PTT,ASAdjacente)['port2']
                self.ipsNaMao[ASAdjacente][porta2] = IPPublicoASNaRede


                #print "link = ",link
                for outroAS in ASsAdjacentes:
                    self.gateway[(ASAdjacente,outroAS)] = IPPublicoASNaRede[:-3] #o gateway dos outros ASs no PTT para este AS eh seu IP no PTT

                redePublica = "172.16.%d.0/24"%contadorRedes
                if ASAdjacente not in IPPublicoASNaRede:
                    self.RedesPublicasPorAS[ASAdjacente] = [redePublica]
                else:
                    self.RedesPublicasPorAS[ASAdjacente].append(redePublica)

            contadorRedes+=1



        for AS,ASsAdjacentes in filter(lambda x: x[0][:3] != "PTT", grafoAciclico.items()):
            for ASAdjacente in filter(lambda x: x[:3] != "PTT",ASsAdjacentes):
                IPPublicoASNaRede1 = "172.16.%d.1/24"%(contadorRedes)
                IPPublicoASNaRede2 = "172.16.%d.2/24"%(contadorRedes)

                #print "adicionou link entre %s e %s usando a rede 172.16.%d.X"%(AS,ASAdjacente,contadorRedes)
                self.addLink(nodosReais[AS],nodosReais[ASAdjacente])
                #print "criou link = ",link
                porta1,porta2 = self.linkInfo(AS,ASAdjacente)['port1'],self.linkInfo(AS,ASAdjacente)['port2']
                self.ipsNaMao[AS][porta1] = IPPublicoASNaRede1
                self.ipsNaMao[ASAdjacente][porta2] = IPPublicoASNaRede2





                self.gateway[(ASAdjacente,AS)] = IPPublicoASNaRede2[:-3] # o gateway para ASadjancente a partir do AS eh o ip dele na sua ligacao
                self.gateway[(AS,ASAdjacente)] = IPPublicoASNaRede1[:-3] # e o contrario tambem

                redePublica = "172.16.%d.0/24"%contadorRedes
                if AS not in self.RedesPublicasPorAS:
                    self.RedesPublicasPorAS[AS] = [redePublica]
                else:
                    self.RedesPublicasPorAS[AS].append(redePublica)

                if ASAdjacente not in self.RedesPublicasPorAS:
                    self.RedesPublicasPorAS[ASAdjacente] = [redePublica]
                else:
                    self.RedesPublicasPorAS[ASAdjacente].append(redePublica)

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

    def makePTT(self,prefixo,nome,rodaMatadorDePassarinho=False):
        return self.addSwitch(nome)

    # def makeAS(self,prefixo,tamanho):
    #     prefixo = prefixo
    #     ipRouter = "10.0.%d.1/24"%prefixo

    #     router = self.addHost("AS%d"%prefixo,cls=LinuxRouter,ip=ipRouter)
    #     switch = self.addSwitch("AS%dsw"%prefixo)
    #     self.addLink(switch,router)

    #     for i in range(tamanho):
    #         ipHost = "10.0.%d.%d/24"%(prefixo,i+2) #pula o zero e o router
    #         host = self.addHost("AS%dH%d"%(prefixo,i),ip=ipHost,defaultRoute="via 10.0.%d.1"%prefixo)
    #         #print "ligando host ",host,"com switch",switch," ip = ",ipHost
    #         link = self.addLink(switch,host)
    #     #print "terminou makeAS de %d"%prefixo
    #     return router

    def makeISP(self,prefixo,tamanho,n_agressores,nome):
        prefixo = prefixo
        ipRouter = "10.0.%d.1/24"%prefixo

        router = self.addHost(nome,cls=LinuxRouter,ip=ipRouter)
        switch = self.addSwitch(nome+"sw")
        self.addLink(switch,router)

        for i in range(tamanho):
            ipHost = "10.0.%d.%d/24"%(prefixo,i+2) #pula o zero e o router
            if i < n_agressores:
                host = self.addHost(nome+"A%d"%i,ip=ipHost,defaultRoute="via 10.0.%d.1"%prefixo)
            else:
                host = self.addHost(nome+"H%d"%i,ip=ipHost,defaultRoute="via 10.0.%d.1"%prefixo)
            #print "ligando host ",host,"com switch",switch," ip = ",ipHost
            linkopts = dict(bw=1)
            self.addLink(switch,host,**linkopts) #1 mga de banda por host

        #print "terminou makeAS de %d"%prefixo
        return router

    def makeTP(self,prefixo,nome):
        prefixo = prefixo
        ipRouter = "10.0.%d.1/24"%prefixo
        router = self.addHost(nome,cls=LinuxRouter,ip=ipRouter)
        switch = self.addSwitch(nome+"sw")
        self.addLink(switch,router)

        return router

    def makeCP(self,prefixo,tamanho,n_vitimas,nome):
        prefixo = prefixo
        ipRouter = "10.0.%d.1/24"%prefixo

        router = self.addHost(nome,cls=LinuxRouter,ip=ipRouter)
        switch = self.addSwitch(nome+"sw")
        self.addLink(switch,router)

        for i in range(tamanho):
            ipHost = "10.0.%d.%d/24"%(prefixo,i+2) #pula o zero e o router
            if i < n_vitimas:
                host = self.addHost(nome+"V%d"%i,ip=ipHost,defaultRoute="via 10.0.%d.1"%prefixo)
            else:
                host = self.addHost(nome+"H%d"%i,ip=ipHost,defaultRoute="via 10.0.%d.1"%prefixo)
            #print "ligando host ",host,"com switch",switch," ip = ",ipHost

            link = self.addLink(switch,host)

        #print "terminou makeAS de %d"%prefixo
        return router

    def getGateway(self):
        return self.gateway

    def getRedesPublicasPorAS(self):
        return self.RedesPublicasPorAS
