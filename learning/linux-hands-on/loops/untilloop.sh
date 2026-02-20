#!/bin/bash
number=1
until [[ $number -ge 10 ]]
do    
    echo $number
    ((number++))    
done
echo "Now number is $number"

number=1
until [[ $number -ge 11 ]]
do
    ((number++))
    if (( $number%2 == 0 ))
    then
        echo "$number cift sayi"
    else
        echo "$number tek sayi"
    fi 
    
done
