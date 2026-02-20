#!/bin/bash
#FILE=/home/bekir/projects/Project-101/First_Part/result.txt
#if [ -f "$FILE" ]; then
#echo "$FILE exists."
#else    
grep "^serdar*" event_history.csv |  grep -i "terminate*"  | egrep -o 'i-[[:xdigit:]]+' |sort | uniq > result.txt 
#fi