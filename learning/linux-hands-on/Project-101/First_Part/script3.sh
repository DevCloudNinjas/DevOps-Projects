#!/bin/bash
grep -i '^serdar' event_history.csv | grep -i 'terminate*'| grep -Eo 'i-.{17}' | sort | uniq > result3.txt
line_count=$(wc -l < result3.txt)
echo $line_count >> result3.txt