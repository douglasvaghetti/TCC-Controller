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
	print arquivo
	execfile(arquivo)

for h in host.values():
	for interface in h.values():
		print "interface = ",interface
		tempo = range(len(interface))
		down = [i[0] for i in interface]
		up = [i[1] for i in interface]
		plt.plot(tempo,down)
		plt.plot(tempo,up)

plt.savefig("test.png")
print host