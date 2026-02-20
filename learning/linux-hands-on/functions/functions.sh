#!/bin/bash

Goodbye(){
    echo "Goodbye from Linux Lessons $1 $2 $3"
}
Goodbye Latif Yakup Rahim

Welcome () {
    echo "welcome to linux lessons $1 $2 $3"
    return 3 #normalde $? 0 gelmesi gerekirken 3 geldi asagida
}

Welcome Joe Math Eric
echo $?