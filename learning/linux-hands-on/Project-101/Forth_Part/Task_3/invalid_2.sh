#!/bin/bash
grep -Eio "invalid user .+" auth.log | awk "{print $3}" | sort |uniq -c > result.txt