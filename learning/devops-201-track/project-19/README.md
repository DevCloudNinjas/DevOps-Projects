# Automate Infrastructure With IaC using Terraform – Terraform Cloud

### [Link to Code](https://github.com/Tonybesto/TCS-Packer-Terraform-Setup.git)
#


[In project 18 ](https://github.com/Tonybesto/DevOps_Projects/blob/main/project-18/project18.md), we refactored our terraform codes into modules and as a result the introduction of modules into our codebase helped save time and reduce costly errors by re-using configuration written either by yourself, other members of your team, or other Terraform practitioners who have published modules for you to use.

We require AMIs that are preconfigured with necessary packages for our applications to run on specific servers.

![](../project-15/Images/architecture%20diagram.PNG)

In this project, we will be introducing two new concepts 
- **Packer**
- **Terraform Cloud**
#
## What is Packer? 
#
Packer is an open source tool for creating identical machine images for multiple platforms from a single source configuration. Packer is lightweight, runs on every major operating system, and is highly performant, creating machine images for multiple platforms in parallel.
#

## Step 1. Creating Bastion, Nginx, Tooling and Wordpress AMIs 
#
We write packer code which helps us create AMIs for each of the following mentioned servers. A sample of the code can be found here: [packer code setup](https://github.com/Tonybesto/TCS-Packer-Terraform-Setup/tree/main/AMI)

For each of the following `.pkr.hcl` files, we run the following commands
```
- packer fmt <name>.pkr.hcl
- packer validate <name>.pkr.hcl
- packer build <name>.pkr.hcl
```

![](./Images/bastion%20AMI.PNG)
![](./Images/nginx%20AMI.PNG)
![](./Images/created%20AMI.PNG)
![](./img/4.all_amis.jpg)
#

## Step 2. Setting Up Infrastructures using Terraform Cloud
#
In this project, we changed the backend from S3 to a remote backend using Terraform Cloud. TF Cloud manages all state in our applications and carries out tf plan , tf validate and applies our infrastructures as required.

To do this, we setup an organization on terraform cloud and a workspace and link our workspace to our repository. On every commit, a webhook is triggered on terraform cloud and plans or applies our terrraform code based on need.


![](./Images/terraform%20cloud%20plan.PNG)
![](./Images/first%20apply.PNG)

## Step 3. Ansible Dynamic Inventory
#
A dynamic inventory is a script written in Python, PHP, or any other programming language. It comes in handy in cloud environments such as AWS where IP addresses change once a virtual server is stopped and started again.

We make use of dynamic inventory to get Ip address of our servers created based on their tag names and hence we are able to run the required role on each server.
![](./Images/ansible-graph.PNG)


#

##  Step 4. Checking Successful 
#
![](./Images/tooling%20site.PNG)
![](./Images/wordpress.PNG)
#

## Step 5. Destroying Resources
#
![](./Images/terraform%20destroy.PNG)
#