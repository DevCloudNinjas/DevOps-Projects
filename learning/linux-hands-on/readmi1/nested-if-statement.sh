#!/bin/bash

read -p "Input a number: " number

if [[ $number -gt 10 ]]
then
  echo "Number is bigger than 10"

  if (( $number % 2 == 1 ))
  then
    echo "And is an odd number."
  else
    echo "And is an even number"
  fi
else 
  echo "It is not bigger than 10"
fi