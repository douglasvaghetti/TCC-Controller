from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
import socket
import threading
import SocketServer
import json

log = core.getLogger()

listaBloqueios = {}
controller = None

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        response = response.split("\n")[-1]
        listaAgressores = json.loads(response)['denuncia']
        listaAgressores = listaAgressores['agressores']
        listaAgressores = [i['ip'] for i in listaAgressores]
        agredido = json.loads(response)['denuncia']['vitima'][0]['ip']
        print listaAgressores
        print "agredido",agredido
        listaBloqueios[agredido] = set(listaAgressores)
       	controller.cria_regra_vai_controller(str(agredido)+"/32")
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def startServer():
	global webServerPorta
    webServerPorta = int(webServerPorta)
	print "porta = ",webServerPorta
	HOST, PORT = "127.0.0.1",webServerPorta
    webServerPorta += 1

	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address
	print "ip,port",ip,port

	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()


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

		# Use this table to keep track of which ethernet address is on
		# which switch port (keys are MACs, values are ports).
		log.debug("instanciou o controller")
		#startServer()
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

			print("Installing flow...")

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
		#sem acao nenhuma = DROP
		print "criou regra de drop de ",ipOrig," para ",ipDest
		self.connection.send(msg)

	def cria_regra_pode_seguir(self,ipOrig,ipDest,porta):
		msg = of.ofp_flow_mod()
		msg.priority = 200
		msg.match = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_dst=ipDest,nw_src=ipOrig)
		action = of.ofp_action_output(port = porta)
		msg.actions.append(action)
		print "criou regra de pode seguir de ",ipOrig," para ",ipDest
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

			print "pacote de",ipOrig,"para",ipDest
			print listaBloqueios
			if str(ipDest) in listaBloqueios:
				print "destinado a vitima"
				if str(ipOrig) in listaBloqueios[str(ipDest)]:
					print "estava na lista de agressores"
					self.cria_regra_drop(ipOrig,ipDest)
				else:
					self.cria_regra_pode_seguir(ipOrig,ipDest,self.mac_to_port[packet.dst])
					self.resend_packet(packet_in,self.mac_to_port[packet.dst])
					print "nao estava na lista de agressores"
			else:
				print "nada a ver com o DDoS"
				self.act_like_switch(packet,packet_in)
		else:
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


global webServerPorta
def launch (webServerPort=8000):
	"""
	Starts the component
	"""
	global webServerPorta
	webServerPorta = webServerPort
	def start_switch (event):
		teste = event.connection
		#print dir(teste),teste,type(teste)
		log.debug("Controlling %s" % (event.connection,))
		global controller
		print "matador de passarinho rodando!"
		controller = Tutorial(event.connection)
	core.openflow.addListenerByName("ConnectionUp", start_switch)
