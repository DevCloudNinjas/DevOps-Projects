#!/bin/bash
# This is a bash script with the purpose to probe functionality for DevOps resource CRUD operations for the DevOps Api

# Creates a new DevOps resource using a POST request
if [[ $1 == "post" ]];then
  # creates new DevOps resource
	curl http://localhost:8080/devops \
    		--include \
    		--header "Content-Type: application/json" \
    		--request "POST" \
        --data '{"ops": [], "dev": []}'
  exit
# Deletes a DevOps resource using DELETE request
# Arguments: 1: delete, 2: DevOps Id as query
elif [[ $1 == "delete" ]]; then
	curl http://localhost:8080/devops/${2} \
        	--include \
         	--header "Content-Type: application/json" \
         	--request "DELETE"
  exit
# Gets all DevOps resources or a specific DevOps resource by Id using GET request
# Arguments to get all DevOps resources: 1: get
# Arguments to get a specific DevOps resource: 1: get, 2: id
elif [[ $1 == "get" ]]; then
  if [[ $# == 1 ]]; then
	  curl http://localhost:8080/devops
  elif [[ $# == 2 ]]; then
    curl http://localhost:8080/devops/${2}
  fi
  exit
fi

echo Help Command DevOps Resource
echo
echo Here are all the commands used for the devops script:
echo
echo post "<-" creates new DevOps resource
echo 
echo delete [devops id] "<-" deletes DevOps resource
echo 
echo get "<-" gets all DevOps resources
echo 
echo get [devops id] "<-" gets specific DevOps resource from id
echo -e '   ' - [devops id] enter the id of the devops resource.
echo

