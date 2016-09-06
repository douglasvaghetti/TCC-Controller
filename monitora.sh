#!/bin/bash
arquivo="$1/$2.py"
touch $arquivo
chmod 777 $arquivo

echo "host['$2'] = {}" >> $arquivo
for i in $3 #3 eh a lista com os nomes das interfaces do host
do
	echo "host['$2']['$i'] = []" >> $arquivo
done

while true
do
	lista=$(bwm-ng -o csv -c1 | cut -d';' -f 1-4 --output-delimiter=' ' | egrep -v 'lo|total' | awk '{print($2 "\"].append((" $3 "," $4 "," $1 "))")}')
	for linha in $lista
	do
		echo "host['$2'][\"$linha" >> $arquivo
	done
done
