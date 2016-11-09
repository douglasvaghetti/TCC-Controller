#!/bin/sh
mn -c
pkill webfsd
pkill wget
ps -ax | grep pox | egrep -v 'color=auto' | awk {'print $1'} | xargs -L1 -I% kill -9 %
ps -ax | grep sflowrt.jar | egrep -v 'color=auto' | awk {'print $1'} | xargs -L1 -I% kill -9 %
pgrep python | xargs -L1 -I% kill -9 %
/home/mininet/TCC-Controller/sflow-rt/start.sh &
data="$(date | awk '{print $3 "-"$2"-"$4}' | sed 's/:/-/g')"
diretorio="testes/$data"
clear
mkdir $diretorio
mkdir "$diretorio/dados"
cp host.py "$diretorio/dados"
cp dadosGrafo.py $diretorio
chmod 777 -R $diretorio

cd "$diretorio/dados/"
python ../../../extraiDadosSflow.py &
cd "../../../"
python preparaMininet.py $diretorio
echo "encerrou o prepara mininet"
cd "$diretorio/dados/"
mn -c
pgrep python | xargs -L1 -I% kill -9 %
echo "rodou o matador de python"
python host.py 
echo "plotou o grafico"
