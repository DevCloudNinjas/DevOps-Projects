 echo "Which Process do you want to terminate ? "

 # shellcheck disable=SC2034
 # shellcheck disable=SC2034
 read processID

 sudo kill -9 $processID
