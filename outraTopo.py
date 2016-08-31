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
        print "rodei"
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()



class PTT(Topo):
    def build(self,prefixos,tamanhos):
        PTT = self.addSwitch('s100')
        routers = []
        for prefixo,tamanho in zip(prefixos,tamanhos):
            router = self.makeAS(prefixo,tamanho)
            IPPublico = "172.16.0.%d/24"%prefixo
            self.addLink(PTT,router,params2={'ip':IPPublico})
            routers.append(router)
        return routers

    def makeAS(self,prefixo,tamanho):
        prefixo = prefixo
        ipRouter = "10.0.%d.1/24"%prefixo
        hostNameRouter = 'r%d'%prefixo

        router = self.addHost("r%d"%prefixo,cls=LinuxRouter,ip=ipRouter)
        switch = self.addSwitch("s%d"%prefixo)
        self.addLink(switch,router)

        for i in range(tamanho):
            ipHost = "10.0.%d.%d/24"%(prefixo,i+2) #pula o zero e o router
            host = self.addHost("h%d%d"%(prefixo,i),ip=ipHost,defaultRoute="via 10.0.%d.1"%prefixo)
            self.addLink(switch,host)
        return router


def prepara(routers,prefixos):
    for router,prefixo in zip(routers,prefixos):
        print router.cmd("ip route | awk '{print $1}' | xargs -L1 -I@ ip route del @") #apaga todas rotas
        print router.cmd("ip route add 10.0.%d.0/24 dev r%d-eth0"%(prefixo,prefixo))
        print router.cmd("ip route add 172.16.0.0/24 dev r%d-eth1"%(prefixo))

    for i,router in enumerate(routers):
        for outroRouter in routers[i+1:]:
            #print "router = %s"%str(type(router))
            #print dir(net.host)
            IPPublicoA = router.intfList()[1].IP()
            redeA = router.intfList()[0].IP()
            redeA = redeA[:redeA.rfind(".")]+".0/24"
            print "routerA = %s redeA = %s IP publico A = %s"%(router,redeA,IPPublicoA)


            IPPublicoB = outroRouter.intfList()[1].IP()
            redeB = outroRouter.intfList()[0].IP()
            redeB = redeB[:redeA.rfind(".")]+".0/24"
            print "routerB = %s redeB = %s IP publico B = %s"%(outroRouter,redeB,IPPublicoB)

            print "#####adicionando rotas em %s"%router
            print router.cmd("route add -net %s gw %s"%(redeB,IPPublicoB))

            print "#####adicionando rotas em %s"%outroRouter
            print outroRouter.cmd("route add -net %s gw %s"%(redeA,IPPublicoA))


prefixos,tamanhos = [1,2,3,4,5],[10,20,30,40,4]
net = Mininet(PTT(prefixos,tamanhos))
net.start()
routers = filter(lambda x: x.name[0]=='r',net.hosts)
prepara(routers,prefixos)

print "Dumping host connections"
dumpNodeConnections(net.hosts)
net.interact()
net.stop()
