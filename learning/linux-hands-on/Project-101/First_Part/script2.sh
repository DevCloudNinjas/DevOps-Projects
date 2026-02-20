#!/bin/bash
grep -i serdar event_history.csv | grep -i TerminateInstances | grep -Eo "i-.{17}" | sort | uniq > result2.txt