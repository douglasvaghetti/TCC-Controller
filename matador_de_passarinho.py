from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
import socket
import threading
import SocketServer
import json

log = core.getLogger()

global controladores
controladores = {}
global chave

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self,*args,**kwargs):
        print "*************rodou init"
        global controladores
        print (args[2].socket.getsockname()[1])
        self.controller = controladores[args[2].socket.getsockname()]
        #print "controladores = ",controladores,"self.controlador = ",self.controller
        SocketServer.BaseRequestHandler.__init__(self,*args,**kwargs)
    
    def handle(self):
        #print "recebeu request"
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        response = response.split("\n")[-1]
        #print dir(json.loads(data)), json.loads(data)

        listaAgressores =  json.loads(data)['denuncia']['agressores']
        agredidos = json.loads(data)['denuncia']['vitima']
        #print listaAgressores
        #print "agredido",agredidos
        listaAgressores = set(listaAgressores)

        for agredido in agredidos:
            self.controller.listaBloqueios[agredido] = listaAgressores
            self.controller.cria_regra_vai_controller(str(agredido)+"/32")
        
        
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def startServer(controller):
    global webServerPorta
    HOST, PORT = "10.0.0.5",int(webServerPorta)
    print "Servidor aberto em ",HOST,PORT
    webServerPorta = int(webServerPorta) + 1
    controladores[(HOST,PORT)] = controller 
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler,controller)
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    #return server


class Tutorial (object):
    """
    A Tutorial object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """
    def __init__ (self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)
        self.listaBloqueios = {}
        # Use this table to keep track of which ethernet address is on
        # which switch port (keys are MACs, values are ports).
        log.debug("instanciou o controller")
        #global controladores
        #controladores.append(self)
        server = startServer(self)
        log.debug("iniciou o server")
        self.mac_to_port = {}

    def resend_packet (self, packet_in, out_port):
        """
        Instructs the switch to resend a packet that it had sent to us.
        "packet_in" is the ofp_packet_in object the switch had sent to the
        controller due to a table-miss.
        """
        msg = of.ofp_packet_out()
        msg.data = packet_in
        action = of.ofp_action_output(port = out_port)
        msg.actions.append(action)
        self.connection.send(msg)



    def act_like_switch (self, packet, packet_in):
        """
        Implement switch-like behavior.
        """

        self.mac_to_port[packet.src] = packet_in.in_port

        if packet.dst in self.mac_to_port:

            #print("Installing flow...")

            msg = of.ofp_flow_mod()
            msg.priority = 100
            msg.match.dl_dst=packet.dst

            action = of.ofp_action_output(port = self.mac_to_port[packet.dst])
            msg.actions.append(action)
            self.connection.send(msg)
            self.resend_packet(packet_in,self.mac_to_port[packet.dst])
        else:
            self.resend_packet(packet_in, of.OFPP_ALL)

    def cria_regra_drop(self,ipOrig,ipDest):
        msg = of.ofp_flow_mod()
        msg.priority = 200
        
        #msg.match = of.ofp_match.from_packet(packet)
        msg.match = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_dst=ipDest,nw_src=ipOrig)
        msg.idle_timeout = 25
        #sem acao nenhuma = DROP
        log.info("criou regra de drop de ",ipOrig," para ",ipDest)
        self.connection.send(msg)

    def cria_regra_pode_seguir(self,ipOrig,ipDest,porta):
        msg = of.ofp_flow_mod()
        msg.priority = 200
        msg.idle_timeout = 25
        msg.match = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_dst=ipDest,nw_src=ipOrig)
        action = of.ofp_action_output(port = porta)
        msg.actions.append(action)
        log.info("criou regra de pode seguir de ",ipOrig," para ",ipDest)
        self.connection.send(msg)

    def cria_regra_vai_controller(self,ipDest):
        msg = of.ofp_flow_mod()
        msg.priority = 150
        msg.match = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_dst=ipDest)
        action = of.ofp_action_output(port = of.OFPP_CONTROLLER)
        msg.actions.append(action)
        print "criou regra vai controller para",ipDest
        self.connection.send(msg)

    def processa(self, packet, packet_in):
        #print "packet tem",dir(packet)
        
        if packet.type == packet.IP_TYPE:
            ipOrig = packet.find('ipv4').srcip
            ipDest = packet.find('ipv4').dstip
            
            #print "pacote de",ipOrig,"para",ipDest
            #print self.listaBloqueios
            if str(ipDest) in self.listaBloqueios:
                #print "destinado a vitima"
                if str(ipOrig) in self.listaBloqueios[str(ipDest)]:
                    #print "estava na lista de agressores"
                    self.cria_regra_drop(ipOrig,ipDest)
                else:
                    self.cria_regra_pode_seguir(ipOrig,ipDest,self.mac_to_port[packet.dst])
                    self.resend_packet(packet_in,self.mac_to_port[packet.dst])
                    #print "nao estava na lista de agressores"
            else:
                #print "nada a ver com o DDoS"
                self.act_like_switch(packet,packet_in)
        else:
            #print "recebeu pacote nao ip",packet.type
            self.act_like_switch(packet, packet_in)

        #print "packet_in tem",dir(packet_in)

    def _handle_PacketIn (self, event):
        """
        Handles packet in messages from the switch.
        """
        packet = event.parsed # This is the parsed packet data.
        #print packet.getNameForType(packet.type)
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp # The actual ofp_packet_in message.
        self.processa(packet, packet_in)

class matador_de_passarinho(object):
    def __init__(self):
        core.openflow.addListeners(self)
    
    def _handle_ConnectionUp(self,event):
        log.debug("conexao matador de passarinho %s"%(event.connection,) )
        Tutorial(event.connection)


global webServerPorta
def launch (webServerPort=8000):
    """
    Starts the component
    """
    global webServerPorta
    webServerPorta = webServerPort
    core.registerNew(matador_de_passarinho)
