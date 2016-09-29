cd lixo
while true
do
    for i in $1
    do
        wget $i/static/menes.png 2> /dev/null
        sleep $[ ( $RANDOM % 6 )  + 3 ]s
        rm ../lixo/* 2>/dev/null
    done
done
