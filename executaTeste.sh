#!/bin/sh
mn -c
pkill webfsd
pkill wget
ps -ax | grep pox | egrep -v 'color=auto' | awk {'print $1'} | xargs -L1 -I% kill -9 %
ps -ax | grep sflowrt.jar | egrep -v 'color=auto' | awk {'print $1'} | xargs -L1 -I% kill -9 %
/home/mininet/TCC-Controller/sflow-rt/start.sh &
data="$(date | awk '{print $3 "-"$2"-"$4}' | sed 's/:/-/g')"
diretorio="testes/$data"
clear
mkdir $diretorio
mkdir "$diretorio/dados"
cp host.py "$diretorio/dados"
cp dadosGrafo.py $diretorio
chmod 777 -R $diretorio
python preparaMininet.py $diretorio
python "$diretorio/dados/host.py"
