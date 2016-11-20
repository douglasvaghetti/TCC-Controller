#!/bin/sh
mn -c
pkill webfsd
pkill wget
ps -ax | grep pox | egrep -v 'color=auto' | awk {'print $1'} | xargs -L1 -I% kill -9 %
ps -ax | grep sflowrt.jar | egrep -v 'color=auto' | awk {'print $1'} | xargs -L1 -I% kill -9 %
pgrep python | xargs -L1 -I% kill -9 %
mn -c
pgrep python | xargs -L1 -I% kill -9 %
