# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import pylab
from matplotlib.backends.backend_pdf import PdfPages
import os

plt.grid(True)
execfile("acumulado.py")
primeiro = dados['malicioso'][0][1]

################# Grafico da rede ##################

fig = plt.figure()
ax = fig.add_subplot(111)
p1 = PdfPages('rede.pdf')
plt.title(u"Tráfego na rede")
ax.set_ylim(0,1024)
ax.set_xlim(0,130)
ax.set_xlabel("Tempo (s)")
ax.set_ylabel(u"Tráfego (MB/s)")

ax.plot([i[1] - primeiro for i in dados['legitimo']][:130], [i[0] for i in dados['legitimo']][:130], linewidth=2, color="blue",label=u"Tráfego legítimo na rede", linestyle="dashed")
ax.plot([i[1] - primeiro for i in dados['malicioso']][:130], [i[0] for i in dados['malicioso']][:130], linewidth=2, color="red",label=u"Tráfego malicioso na rede", linestyle="solid")
for bloq in dados['bloqueio']:
    y = int([i for i in dados['malicioso'] if i[1]==bloq[1]][0][0])
    x = int(bloq[1]) - primeiro
    ax.annotate(bloq[0],xy=(x,y),xytext=(x+5,y+60),arrowprops=dict(facecolor='black', shrink=0.05,frac=0.3,width=1,headwidth=10))

pylab.legend()
p1.savefig(fig)
p1.close()

############# FIM Grafico da rede ##################

plt.clf()

################# Grafico de regras ################

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
p2 = PdfPages('regras.pdf')
plt.title(u"Número de regras OpenFlow nos IXPs")
ax2.set_ylim(0,100)
ax2.set_xlim(0,130)
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel(u"Número de regras instaladas")

cores = ['green', 'blue', 'purple']
linhas = ['dotted', 'dashed', 'solid']
ptts = set([i[1] for i in dados['regras']])
for count, ptt in enumerate(ptts):
    ax2.plot([i[2] - primeiro for i in dados['regras'] if i[1] == ptt][:130], [i[0] for i in dados['regras'] if i[1] == ptt][:130], linewidth=2, color=cores[count],label=u"Número de regras OpenFlow no IXP"+ptt[3:], linestyle = linhas[count])
    for bloq in dados['bloqueio']:
#       print "bloq ", bloq[0][3:], "ptt ", ptt[3:]
        if bloq[0][3:] == ptt[3:] :
            y = int([i[0] for i in dados['regras'] if i[2] == bloq[1] and i[1][3:] == ptt[3:]][0])
#           print " y = ",y
            x = int(bloq[1]) - primeiro
            ax2.annotate(bloq[0],xy=(x,y),xytext=(x-15,y+10),arrowprops=dict(facecolor='black', shrink=0.05,frac=0.3,width=1,headwidth=10))

pylab.legend()
p2.savefig(fig2)
p2.close()

############# FIM Grafico de regras ################

################# Grafico da vitima ################

plt.clf()

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
p3 = PdfPages('asVitima.pdf')
plt.title(u"Tráfego na vítima")
ax3.set_ylim(0,256)
ax3.set_xlim(0,130)
ax3.set_xlabel("Tempo (s)")
ax3.set_ylabel(u"Trafégo (MB/s)")

ax3.plot([i[1] - primeiro for i in dados['chegouMalicioso']][:130], [i[0] for i in dados['chegouMalicioso']][:130], linewidth=2, color="red",label=u"Tráfego malicioso no SA vítima", linestyle="solid")
ax3.plot([i[1] - primeiro for i in dados['chegouLegitimo']][:130], [i[0] for i in dados['chegouLegitimo']][:130], linewidth=2, color="blue",label=u"Tráfego legítimo no SA vítima", linestyle="dashed")
for bloq in dados['bloqueio']:
    y = int([i for i in dados['chegouMalicioso'] if i[1]==bloq[1]][0][0])
    x = int(bloq[1]) - primeiro
    ax3.annotate(bloq[0],xy=(x,y),xytext=(x+7,y+15),arrowprops=dict(facecolor='black', shrink=0.05,frac=0.3,width=1,headwidth=10))

pylab.legend()
p3.savefig(fig3)
p3.close()

