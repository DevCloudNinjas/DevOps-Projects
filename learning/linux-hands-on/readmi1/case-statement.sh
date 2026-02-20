#!/bin/bash

read -p "Input first number: " first_number
read -p "Input second number: " second_number

read -p "choice
1- topla
2- cikar
" operation

case $operation in 
    "1")
    echo "result=$(( $first_number + $second_number ))"
    ;;
    "2")
    echo "result=$(( $first_number + $second_number ))"
    ;;
    *)
    echo "wrong choice"
    ;;
esac