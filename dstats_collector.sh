#!/usr/bin/sh
while `true`:
do
        docker stats -a --no-stream >> $1;
        sleep 1s;
        date >> $1;
done
