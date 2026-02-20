#!/bin/bash
# This is a bash script with the purpose to probe functionality for Dev resource CRUD operations for the DevOps Api

# Creates new Dev resources using POST request
# Arguments: 1: post
if [[ $1 == "post" ]];then
	# creates a new Dev resource named dev_ferrets
	curl http://localhost:8080/dev \
    		--include \
    		--header "Content-Type: application/json" \
    		--request "POST" \
    		--data '{"name": "dev_ferrets"}'
	# creates a new Dev resource named dev_bengal
	curl http://localhost:8080/dev \
      		--include \
      		--header "Content-Type: application/json" \
      		--request "POST" \
      		--data '{"name": "dev_bengal"}'
  exit
# Update a Dev resource using a PUT request
# Arguments: 1: put, 2: Dev Id as query
elif [[ $1 == "put" ]]; then
	curl http://localhost:8080/dev/${2} \
        	--include \
        	--header "Content-Type: application/json" \
        	--request "PUT" \
        	--data '{"name":"'"$3"'"}'
  exit
# Deletes a Dev resource using DELETE request
# Arguments: 1: delete, resource 2: Engineer Id as query
elif [[ $1 == "delete" ]]; then
	curl http://localhost:8080/dev/${2} \
        	 --include \
         	--header "Content-Type: application/json" \
         	--request "DELETE"
  exit
# Adds a Dev Resource to a DevOps resource's Dev list using POST request.
# Arguments: 1: devops, 2: Dev Id sent as json data, 3: DevOps Id sent as query 
elif [[ $1 == "devops" ]]; then
	curl http://localhost:8080/devops/dev/${3} \
          	--include \
          	--header "Content-Type: application/json" \
          	--request "POST" \
          	--data '{"id":"'"$2"'"}'
  exit
# Gets all Dev resources or a specific Dev resource by Id, Name using GET request
# Arguments to get all Engineers: 1: get
# Arguments to get a specific Dev resource: 1: get, 2: type -> id, name, 3: actual id, or name
elif [[ $1 == "get" ]]; then
	if [[ $# == 1 ]]; then
		curl http://localhost:8080/dev
  elif [[ $# == 3 ]]; then
    curl http://localhost:8080/dev/${2}/${3}
	fi
  exit
fi


echo Help Command Dev Resource
echo
echo Here are all the commands used for the dev script:
echo
echo post "<-" creates new Dev resources
echo
echo put [dev id] "<-" updates Dev resource
echo
echo delete [dev id] "<-" deletes Dev resource
echo
echo devops [dev id] [devops id] "<-" adds Dev resource to DevOps resource Dev list
echo
echo get "<-" gets all Dev resources
echo
echo get [type: id, or name] [dev id, or name] "<-" gets specific Dev resource from id or name
echo -e '   '  - [type: id, name] should be the word "id", or "name".
echo -e '   '  - [dev id, name] enter the id, or name of the dev resource.
echo
