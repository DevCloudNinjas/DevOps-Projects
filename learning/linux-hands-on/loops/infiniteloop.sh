#!/bin/bash
number=1
until [[ $number -lt 1 ]]
do    
    ((number++))

    tens=$(($number%10))

    if [[ $tens -eq 0 ]]
    then
        continue #10 20 30 40 görünce es gec
    fi

    echo $number

    if [[ $number -gt 40 ]]
    then
        break #40i gecince kir
    fi
done
echo "now number is $number"