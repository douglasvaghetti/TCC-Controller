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

def makeAS(topo,prefixo,NHosts):
    prefixo = prefixo
    redeRouter = "10.0.%d.0/24"%prefixo
    ipRouter = "10.0.%d.1/24"%prefixo
    hostNameRouter = 'r%d'%prefixo
    router = topo.addHost(hostNameRouter,ip = ipRouter,cls=LinuxRouter)
    print "ip do router "+ipRouter
    switch = topo.addSwitch('s%d'%prefixo)
    topo.addLink(switch,router,params2={'ip':ipRouter})

    for h in range(2,NHosts+2):
        hostName = "h%d%d"%(prefixo,h)
        ipHost = "10.0.%d.%d/24"%(prefixo,h)
        rotaDefault = "via 10.0.%d.1"%prefixo
        host = topo.addHost(hostName,ip=ipHost,defaultRoute=rotaDefault)
        topo.addLink(host,switch,params1={'ip':ipHost})

    return (router,redeRouter)

class ASSimples(Topo):
    def build(self,listaPrefixos,tamanhoPorAS):
        PTT = self.addSwitch('s100')
        for prefixo,tamanho in zip(listaPrefixos,tamanhoPorAS):
            router,redeRouter = makeAS(self,prefixo,tamanho)
            IPPublico = "10.0.240.%d/24"%prefixo
            self.addLink(router,PTT,params1 = {'ip':IPPublico})


def simpleTest():
    "Create and test a simple network"
    prefixos = [1,2]
    tamanhosAS = [2,2]
    topo = ASSimples(prefixos,tamanhosAS)
    net = Mininet(topo)
    net.start()

    routers = filter(lambda x: x.name[0]=='r',net.hosts)

    for i,router in enumerate(routers):
        print """############################\ncriando bridge do router %d\n#############################"""%i
        print router.cmd("""
                      brctl addbr br0 &&
                      brctl addif br0 r%d-eth0 r%d-eth1 &&
                      ip link set dev br0 up"""%tuple([i+1]*2r1 ip ))
        for outroRouter in routers:
            if outroRouter != router:
                outraRede = outroRouter.intfList()[0].IP()[:outroRouter.intfList()[0].IP().rfind(".")]+".0/24"
                gateway = outroRouter.intfList()[1].IP()
                print "#####adicionando nova rota: ip route add %s via %s dev br0"%(outraRede,gateway)
                print router.cmd("ip route add %s via %s dev br0"%(outraRede,outroRouter.IP()))
                #router.setHostRoute(outraRede,'eth1')
                print "adicionou nova rota em "+router.name+" para "+outraRede
    #return
    #h1 = net.get('h2')
    #result = h1.cmd('ifconfig')
    #print result
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"

    #net.pingAll()
    net.interact()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
