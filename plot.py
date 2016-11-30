# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import pylab
from matplotlib.backends.backend_pdf import PdfPages

plt.grid(True)
p1 = PdfPages('rede.pdf')
p2 = PdfPages('regras.pdf')

host = {}
import os
execfile("acumulado.py")
eixoX = [i[1] for i in dados['malicioso']]
primeiro = eixoX[0]
eixoX = [i-primeiro for i in eixoX][:130]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(eixoX, [i[0] for i in dados['legitimo'][:130]], linewidth=2, color="blue",label=u"Tráfego legítimo na rede", linestyle="dotted")
ax.plot(eixoX, [i[0] for i in dados['malicioso'][:130]], linewidth=2, color="red",label=u"Tráfego malicioso na rede", linestyle="dashed")
ax.plot(eixoX, [i[0] for i in dados['chegou'][:130]], linewidth=2, color="purple",label=u"Tráfego no SA vítima", linestyle="solid")
plt.title(u"Tráfego de dados na rede")
ax.set_xlabel("Tempo(s)")
ax.set_ylabel(u"Tráfego (MB/s)")
ax.set_ylim(0,768)
ax.set_xlim(0,130)
pylab.legend()
for bloq in dados['bloqueio']:
    y = int([i for i in dados['malicioso'] if i[1]==bloq[1]][0][0])
    x = int(bloq[1]) - primeiro
    ax.annotate(bloq[0],xy=(x,y),xytext=(x+5,y+60),arrowprops=dict(facecolor='black', shrink=0.05,frac=0.3,width=1,headwidth=10))
    print "anotou"

p1.savefig(fig)
p1.close()
plt.clf()

fig2 = plt.figure()

ax2 = fig2.add_subplot(111)
ax2.set_ylim(0,128)
ax2.set_xlim(0,130)
plt.title("Regras OpenFlow nos PTTs")
ax2.plot(eixoX, [i[0] for i in dados['regras'][:130]], linewidth=2, color="green",label=u"Número de regras instaladas nos IXPs")
ax2.set_xlabel("Tempo(s)")
ax2.set_ylabel(u"Regras instaladas")
pylab.legend()
p2.savefig(fig2)
p2.close()
#print host
