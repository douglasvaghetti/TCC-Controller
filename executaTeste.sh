#!/bin/sh

data="$(date | awk '{print $3 "-"$2"-"$4}' | sed 's/:/-/g')"
diretorio="testes/$data"
mn -c
mkdir $diretorio
mkdir "$diretorio/dados"
cp host.py "$diretorio/dados"
cp dadosGrafo.py $diretorio
chmod 777 -R $diretorio
python preparaMininet.py $diretorio
