#!/bin/bash
# This is a bash script with the purpose to probe functionality for Engineer resource CRUD operations for the DevOps Api

# Creates new Engineer resources using POST request
# Arguments: 1: post
if [[ $1 == "post" ]];then
	# creates a new Engineer resource named ryan
	curl http://localhost:8080/engineers \
    		--include \
    		--header "Content-Type: application/json" \
    		--request "POST" \
    		--data '{"name": "Ryan","email": "ryan@ferrets.com"}'
	# creates a new Engineer resource named zach
	curl http://localhost:8080/engineers \
      		--include \
      		--header "Content-Type: application/json" \
      		--request "POST" \
      		--data '{"name": "zach", "email": "zach@bengal.com"}'
  # creates a new Engineer resource named bob
  curl http://localhost:8080/engineers \
      		--include \
      		--header "Content-Type: application/json" \
      		--request "POST" \
      		--data '{"name": "bob", "email": "bob@bob.com"}'
  exit
# Updates an Engineer Resource using a PUT request 
# Arguments: 1: put, 2: Engineer Id as query 
elif [[ $1 == "put" ]]; then
	curl http://localhost:8080/engineers/${2} \
        	--include \
        	--header "Content-Type: application/json" \
        	--request "PUT" \
        	--data '{"name":"'"$3"'"}'
  exit
# Deletes an engineer using a DELETE request
# Arguments: 1: delete, resource 2: Engineer Id as query 
elif [[ $1 == "delete" ]]; then
	curl http://localhost:8080/engineers/${2} \
        	 --include \
         	--header "Content-Type: application/json" \
         	--request "DELETE"
  exit
# Adds an Engineer Resource to a Developer resource's Engineer list using POST request.
# Arguments: 1: dev, 2: Engineer Id sent as json data, 3: Dev Id sent as query 
elif [[ $1 == "dev" ]]; then
	curl http://localhost:8080/dev/${3} \
          	--include \
          	--header "Content-Type: application/json" \
          	--request "POST" \
          	--data '{"id":"'"$2"'"}'
  exit
# Adds an Engineer Resource to a Operation resource's Engineer list using POST request.
# Arguments: 1: ops, 2: Engineer Id sent as json data, 3: Ops Id sent as query 
elif [[ $1 == "ops" ]]; then
	curl http://localhost:8080/op/${3} \
          	--include \
          	--header "Content-Type: application/json" \
          	--request "POST" \
          	--data '{"id":"'"$2"'"}'
  exit
# Gets all Engineer resources or a specific Engineer resource by Id, Name, or Email using GET request  
# Arguments to get all Engineers: 1: get
# Arguments to get a specigic Engineer: 1: get, 2: type -> id, name, or email 3: actual id, name or email
elif [[ $1 == "get" ]]; then
  if [[ $# == 1 ]]; then
     curl http://localhost:8080/engineers
  elif [[ $# == 3 ]]; then   
    curl http://localhost:8080/engineers/${2}/${3}
  fi
  exit
fi

echo Help Command Engineer Resource
echo
echo Here are all the commands used for the engineer script:
echo
echo post "<-" creates new Engineer resources 
echo
echo put [engineer id] "<-" updates Engineer resource
echo
echo delete [engineer id] "<-" deletes Engineer resource
echo
echo dev [engineer id] [dev id] "<-" adds Engineer resource to Dev resource Engineer list
echo
echo ops [engineer id] [ops id] "<-" adds Engineer resource to Ops resource Engineer list
echo 
echo get "<-" gets all Engineer resources
echo 
echo get [type: id, name, email] [engineer id, name, or email] "<-" gets specific Engineer resource from id or name
echo -e '   '  - [type: id, name, email] should be the word "id", "name", or "email".
echo -e '   '  - [engineer id, name, email] enter the id, name, or email of the engineer resource.
echo
