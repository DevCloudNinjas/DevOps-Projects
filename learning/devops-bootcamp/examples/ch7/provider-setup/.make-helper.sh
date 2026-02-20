#!/bin/bash

function ac () {
  local err1=$(terraform -chdir=examples/allCombined init -plugin-dir=../../.plugin-cache | grep "Error")
  if [ "$err1" != "" ]; then
    printf "$err1\r\n"
    return 1
  else
    printf "|#######################      |\r"
  fi


  local err2=$(terraform -chdir=examples/allCombined plan | grep "Error")
  if [ "$err2" != "" ]; then
    printf "$err2\r\n"
    return 2
  else
    printf "|#############################| "
    echo "Finished Successfully"
  fi;
}

printf "|##########                   |\r"
if [ "$1" = "ac" ]; then
  ac;
fi
