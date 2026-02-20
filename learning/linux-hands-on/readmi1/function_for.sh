# #!/bin/bash

# #diese funktion schreibt die DevOps-Tools
# DevOps(){
#     devops_tools=("Kubernetes" "Docker" "Ansible")

#     for tool in ${devops_tools[@]}
#         do
#         echo " $tool "
#         done
# }

# DevOps

#!/bin/bash

# Welcome () {
#     echo "Welcome to Linux Lessons $1 $2 $3"
#     return 2
#     }

# Welcome Joe Matt Timothy
# echo $?

#!/bin/bash

function_one () {
   echo "This is from the first function"
   function_two
}

function_two () {
   echo "This is from the second function"
}

function_one