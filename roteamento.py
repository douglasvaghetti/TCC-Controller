from mininet.link import TCLink,TCIntf


visitados = None

def criaRotas(net,grafo,topologia,defs):
    routersASs = filter(lambda x: x.name[:3]!='PTT',net.hosts)
    routersReais = {}
    for nomeAS,defsAS in filter(lambda x: x[0][:3]!="PTT",defs.items()):
        routersReais[nomeAS] = net[nomeAS]
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
    gateway = topologia.getGateway()
    RedesPublicasPorAS = topologia.getRedesPublicasPorAS()
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
        #print "#### criando rotas de %s"%origem
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
