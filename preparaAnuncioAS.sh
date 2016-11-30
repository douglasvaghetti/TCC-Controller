#!/bin/sh

echo "----------------------------" >> teste.log
echo "Iniciando sleep" >> teste.log
sleep 60s
for i in $(cat "dadosGrafo$1.py" | awk '{print $1}' | grep PTT | grep grafo | sed 's/grafo\[\"PTT//g' | sed 's/\"\]//g'); do
        echo "Anunciou regra para o PTT $i" >> teste.log
	j=$((i-1))
	echo "cat mensagemTopo$1.json | netcat 10.0.0.5 667$j &" >> teste.log
	tempo=$(date +%s)
	echo "dados['bloqueio'].append(('IXP$i', $tempo))" >> "$2/dados/acumulado.py"
	echo "guardou log: em $2/dados/acumulado.py" >> teste.log
	echo "dados['bloqueio'].append(('IXP$i', $tempo))" >> teste.log
	cat "mensagemTopo$1.json" | netcat 10.0.0.5 "667$j" &
	sleep 20s
done
echo "Terminou o Bloqueio" >> teste.log
