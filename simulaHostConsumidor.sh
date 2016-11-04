cd lixo
while true
do
    for i in $1
    do
        sleep $[ ( $RANDOM % 2 )  + 2 ]s
        wget $i/static/menes.png 2> /dev/null
        rm ../lixo/* 2>/dev/null
    done
done
