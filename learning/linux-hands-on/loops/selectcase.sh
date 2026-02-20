#!/bin/bash

read -p "Input first number: " first_number
read -p "Input second number: " second_number

PS3="Select the operation: "

select operation in addition subtraction multiplication division exit
do
    case $operation in
    addition)
        echo "result=$(($first_number + $second_number))"
    ;;
    subtraction)
        echo "result=$(($first_number - $second_number))"
    ;;
    multiplication)
        echo "result=$(($first_number * second_number))"
    ;;
    division)
        echo "result=$((first_number/second_number))"
    ;;
    exit)
        break
    ;;
    *)
    echo "wrong choice.."
    ;;
    esac
done
    
