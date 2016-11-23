# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import pylab

plt.grid(True)

host = {}
import os
execfile("acumulado.py")
eixoX = [i[1] for i in dados['malicioso']]
primeiro = eixoX[0]
eixoX = [i-primeiro for i in eixoX][:140]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(eixoX, [i[0] for i in dados['legitimo'][:140]], color="blue",label=u"Tráfego legítimo")
ax.plot(eixoX, [i[0] for i in dados['malicioso'][:140]], color="red",label=u"Tráfego malicioso")
ax.plot(eixoX, [i[0] for i in dados['chegou'][:140]],color="purple",label=u"Tráfego no SA vítima")
ax.set_xlabel("Tempo(s)")
ax.set_ylabel(u"Tráfego (MB/s)")
ax.set_ylim(0,1024)
ax.set_xlim(0,140)
pylab.legend()
for bloq in dados['bloqueio']:
    y = int([i for i in dados['malicioso'] if i[1]==bloq[1]][0][0])
    x = int(bloq[1]) - primeiro
    ax.annotate(bloq[0],xy=(x,y),xytext=(x+5,y+60),arrowprops=dict(facecolor='black', shrink=0.05,frac=0.3,width=1,headwidth=10))
    print "anotou"

plt.savefig("trafego.png")
plt.clf()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

ax2.plot(eixoX, [i[0] for i in dados['regras'][:140]], color="green")
ax2.set_xlabel("Tempo(s)")
ax2.set_ylabel(u"Regras instaladas")
plt.savefig("regras.png")

#print host
