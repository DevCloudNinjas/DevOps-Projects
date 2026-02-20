#!/bin/bash

echo "numbers: "
for number in 0 1 2 3 4 5
do
    echo $number
done

for number2 in {1..6..2}
do
    echo $number2
done

echo "Names: "
names=( Rahim "Latif" "Yakup" )
for name in ${names[@]}
do
    echo $name
done

echo "files in current folder:"

for file in `pwd`/* # or $(pwd)/*
do
    echo $file
done

for file in ls pwd date whoami
do
    echo
    echo "----$file----"
    $file
    
done

devops_tools=("terraform" "docker" "kubernetes")
for tool in ${devops_tools[@]}; 
do
echo $tool
done

