#!/bin/bash
#curl stenin icerigini cekiyor

until curl -s -h www.google.com > /dev/null
do
    echo "website is unavailable"
    sleep 5
done

echo "it connected"

while true
do
    curl -s -h www.google.com > /dev/null
    if [[ $? -ne 0 ]]
    then
        echo "website is unavailable"
        sleep 5
    else
        echo "it connected"
    fi
done