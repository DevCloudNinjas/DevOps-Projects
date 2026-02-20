#!/bin/bash
# This is a bash script with the purpose to probe functionality for Ops resource CRUD operations for the DevOps Api

# Creates new Ops resources using POST request
# Arguments: 1: post
if [[ $1 == "post" ]];then
	# creates a new Ops resource named ops_ferrets
	curl http://localhost:8080/op \
    		--include \
    		--header "Content-Type: application/json" \
    		--request "POST" \
    		--data '{"name": "ops_ferrets"}'
	# creates a new Ops resource named ops_bengal
	curl http://localhost:8080/op \
      		--include \
      		--header "Content-Type: application/json" \
      		--request "POST" \
      		--data '{"name": "ops_bengal"}'
  exit
# Update a Ops resource using a PUT request
# Arguments: 1: put, 2: Ops Id as query
elif [[ $1 == "put" ]]; then
	curl http://localhost:8080/op/${2} \
        	--include \
        	--header "Content-Type: application/json" \
        	--request "PUT" \
        	--data '{"name":"'"$3"'"}'
  exit
# Deletes a Ops resource using DELETE request
# Arguments: 1: delete, resource 2: Ops Id as query
elif [[ $1 == "delete" ]]; then
	curl http://localhost:8080/op/${2} \
        	--include \
         	--header "Content-Type: application/json" \
         	--request "DELETE"
  exit
# Adds a Ops Resource to a DevOps resource's Ops list using POST request.
# Arguments: 1: devops, 2: Ops Id sent as json data, 3: DevOps Id sent as query 
elif [[ $1 == "devops" ]]; then
	curl http://localhost:8080/devops/op/${3} \
          	--include \
          	--header "Content-Type: application/json" \
          	--request "POST" \
          	--data '{"id":"'"$2"'"}'
  exit
# Gets all Ops resources or a specific Ops resource by Id, Name using GET request
# Arguments to get all Ops resources: 1: get
# Arguments to get a specific Ops resource: 1: get, 2: type -> id, name, 3: actual id, or name
elif [[ $1 == "get" ]]; then
	if [[ $# == 1 ]]; then
		curl http://localhost:8080/op
  elif [[ $# == 3 ]]; then
    curl http://localhost:8080/op/${2}/${3}
	fi
  exit
fi


echo Help Command Ops Resource
echo
echo Here are all the commands used for the ops script:
echo
echo post "<-" creates new Ops resources
echo
echo put [ops id] "<-" updates Ops resource
echo
echo delete [ops id] "<-" deletes Ops resource
echo
echo devops [ops id] [devops id] "<-" adds Ops resource to DevOps resource Ops list
echo
echo get "<-" gets all Ops resources
echo
echo get [type: id, name] [ops id, name] "<-" gets specific Ops resource from id or name
echo -e '   '  - [type: id, name] should be the word "id", or "name".
echo -e '   '  - [ops id, name] enter the id, or name of the ops resource.
echo
