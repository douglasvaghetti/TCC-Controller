import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

plt.grid(True)

host = {}
import os
execfile("acumulado.py")

eixoX = range(len(dados["malicioso"]))
plt.plot(eixoX, dados['legitimo'], color="blue")
plt.plot(eixoX, dados['malicioso'], color="red")
plt.plot(eixoX, dados['regras'], color="green")

plt.savefig("test.png")
#print host
