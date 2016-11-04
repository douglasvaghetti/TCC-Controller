import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# t = np.arange(0.0, 2.0, 0.01)
# s = np.sin(2*np.pi*t)
# plt.plot(t, s)

# plt.xlabel('time (s)')
# plt.ylabel('voltage (mV)')
plt.grid(True)


host = {}
import os
arquivos = [f for f in os.listdir('.') if os.path.isfile(f) and f != "host.py" and f[-3:]==".py"]
for arquivo in arquivos:
	#print arquivo
	execfile(arquivo)

somatorioLegitimo = {}
somatorioMalicioso = {}

for listaLeituras in host.values():
	for leitura in listaLeituras:
		print "leitura= ",leitura
		finalDoIP1 = int(leitura[0].split(".")[-1])
		finalDoIP2 = int(leitura[1].split(".")[-1])
		print finalDoIP1
		print finalDoIP2
		banda1 = float(leitura[2])
		banda2 = float(leitura[3])
		timestamp = leitura[-1]
		if finalDoIP1 >= 100:
			if timestamp in somatorioMalicioso:
				somatorioMalicioso[timestamp]+=banda1
			else:
				somatorioMalicioso[timestamp] = banda1
		else:
			if timestamp in somatorioLegitimo:
				somatorioLegitimo[timestamp]+=banda1
			else:
				somatorioLegitimo[timestamp] = banda1

		if finalDoIP2 >= 100:
			if timestamp in somatorioMalicioso:
				somatorioMalicioso[timestamp]+=banda2
			else:
				somatorioMalicioso[timestamp] = banda2
		else:
			if timestamp in somatorioLegitimo:
				somatorioLegitimo[timestamp]+=banda2
			else:
				somatorioLegitimo[timestamp] = banda2


# for h in host.values():
# 	for interface in h.values():
# 		print "interface = ",interface
# 		tempo = range(len(interface))
# 		down = [i[0] for i in interface]
# 		up = [i[1] for i in interface]
# 		plt.plot(tempo,down)
# 		plt.plot(tempo,up)

pares = sorted(somatorioLegitimo.items())
tempo = [i[0] for i in pares]
trafegoLegitimo = [i[1] for i in pares]
plt.plot(tempo,trafegoLegitimo,color="blue")


paresMalicioso = sorted(somatorioMalicioso.items())
tempoMalicioso = [i[0] for i in pares]
trafegoMalicioso = [i[1] for i in pares]
plt.plot(tempo,trafegoMalicioso,color="red")



plt.savefig("test.png")
#print host
