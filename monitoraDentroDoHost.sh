#!/bin/bash
arquivo="$1/$2.py"
touch $arquivo
chmod 777 $arquivo

echo "host['$2'] = []" >> $arquivo

while true
do

	for i in $3 #3 eh a lista com os nomes das interfaces do host
	do
		echo "rodando na interface $i"
		timeout 3s iftop -B -t -n -s 1 -i $i 2>/dev/null | egrep "<=|=>" | ./formatadorSaidaIFtop.py $2 $i >> $arquivo &
		#echo "rodou"
	done

	#echo "rodei $arquivo"
	 sleep $[ ( $RANDOM % 2 )  + 1 ]s
done
