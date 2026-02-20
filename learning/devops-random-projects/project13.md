# INTRODUCING ANSIBLE DYNAMIC ASSIGNMENTS(INCLUDE) AND COMMUNITY ROLES

## INTRODUCTION

In continuation with [project 12](./Project12.md), dynamic assignment is introduced by making use of include modules. By dynamic, it means that all statements are processed only during execution of the playbook which is the opposite of the import modules.

The following steps outlines how include module is used for running dynamic environment variable:

## STEP 1: Introducing Dynamic Assignment Into The Project

- Checking out to a new branch in the same ansible-config-mgt repository and naming it ‘dynamic-assignments’

![](./img/project13/git%20checkout%20dynamic-assignment.png)

- Creating a new folder in the root directory of the repository and naming it ‘dynamic-assignments’

![](./img/project13/creating%20dynamic-assignment%20folder.png)

- Creating an environment variable file in the dynamic-assignments directory and naming it ‘env_vars.yml’

![](./img/project13/creating%20env-vars%20file.png)

- Creating a folder that holds the environmental variable and naming it ‘env-var’
- Creating the following files under it: dev.yml, uat.yml, prod.yml and stage.yml
- The structure of the ansible-config-mgt folder will be as displayed below:

![](./img/project13/ansible-config-mgt%20folder%20structure.png)

- Entering the following codes in the env_vars.yml file:
```
---
- name: looping through list of available files
  include_vars: "{{ item }}"
  with_first_found:
    - files:
        - stage.yml
        - dev.yml
        - prod.yml
        - uat.yml
      paths:
        - "../env-vars"
  tags:
    - always
```
![](./img/project13/env_vars.yml%20file.png)

- Updating site.yml file to work with dynamic-assignments:

![](./img/project13/updating%20site.yml%20file.png)

## STEP 2: Implementing Community Roles

In order to preserve my github state whenever I install a new role in the ansible-config-mgt project on the the bastion server, I made use of git commands so I can easily commit the changes made and pushing it to the ansible-config-mgt repository directly from the bastion server

- Installing git packages: `$ sudo apt install git`
- Initializing the ansible-artifact-config directory: `$ git init`

![](./img/project13/git%20init.png)

- Pulling the ansible-config-mgt repository: `$ git pull https://github.com/apotitech/ansible-config-mgt.git`

![](./img/project13/git%20pull.png)

- Registering the repo: `$ git remote add origin https://github.com/apotitech/ansible-config-mgt.git`
- Creating a new branch 'roles-feature': `$ git branch roles-feature`
- Switching to the new branch: `$ git switch roles-feature`

![](./img/project13/creating%20branch%20and%20switching%20to%20it.png)

- Making use of community roles by installing a MySQL role already configured from ansible-galaxy by geerlingguy in the role directory: `$ ansible-galaxy install geerlingguy.mysql`

![](./img/project13/ansible-galaxy%20for%20mysql.png)

- Renaming the role folder to mysql: `$ mv geerlingguy.mysql/ mysql`

![](./img/project13/changing%20the%20folder%20name%20to%20mysql.png)

- Updating the ansible-config-mgt repository

**git add .**

![](./img/project13/2-git%20add.png)

**git commit -m "Commit new role files into GitHub"**

![](./img/project13/2-git%20commit.png)

**git push --set-upstream origin roles-feature**

![](./img/project13/3-git%20push%20upstream.png)

- Creating a pull request

![](./img/project13/4-pull%20request%20created.png)

- Merging the request

![](./img/project13/5-pull%20request%20merged.png)

## STEP 3: Implementing Load Balancer(Apache & Nginx) Roles

Two load balancer roles are setup which are Nginx and Apache roles, but because a web server can only make use of one load balancer, the playbook is configured with the use of conditionals- when statement, to ensure that only the desired load balancer role tasks gets to run on the webserver 
- Setting up apache role in the role directory: `$ sudo ansible-galaxy init apache`

**The folder structure of Apache role:**

![](./img/project13/apache%20role%20folder%20structure.png)

- Setting up nginx role in the role directory: `$ sudo ansible-galaxy init nginx`

**The folder structure of Nginx role:**

![](./img/project13/nginx%20role%20folder%20structure.png)

- Entering the following code task in **apache/tasks/main.py** file:
```
---
- name: install apache
  become: true
  apt:
    name: apache2
    state: present

- name: Start service apache, if not started
  become: true
  service:
    name: apache2
    state: started

```
![](./img/project13/apache%20task%20file.png)

- Entering the following code in **nginx/tasks/main.py** file:
```
- name: install ngnix
  become: true
  apt:
    name: nginx
    state: present

- name: Start nginx service, if not started
  become: true
  service:
    name: nginx
    state: started

```
![](./img/project13/nginx%20task%20file.png)

- Declaring the following variable in the 'defaults/main.py' file of both apache and nginx roles file which makes ansible to skip the roles during execution.

**For apache/defaults/main.py**
```
---
enable_apache_lb: false
load_balancer_is_required: false

```
![](./img/project13/apache%20defaults%20file.png)

**For nginx/defaults/main.py**
```
---
enable_apache_lb: false
load_balancer_is_required: false
```
![](./img/project13/nginx%20defaults%20filt.png)

- Creating a file in the static-assignment folder and naming it ‘loadbalancers.yml’ and entering the following codes:
```
- hosts: lb
  roles:
    - { role: nginx, when: enable_nginx_lb and load_balancer_is_required }
    - { role: apache, when: enable_apache_lb and load_balancer_is_required }

```
![](./img/project13/loadbalancers.yml%20file.png)

- Updating the site.yml file:
```
---
- name: Loadbalancers assignment
  hosts: lb
- import_playbook: ../static-assignments/loadbalancers.yml
  when: load_balancer_is_required 

```
![](./img/project13/updating%20site.yml-2.png)

- To define which load balancer to use, the files in the env-var folder is used to override the default settings of any of the load balancer roles. In this case the env-var/dev.yml file is used to make ansible to only run nginx load balancer task in the target server:

**env-var/dev.yml file**
```
enable_nginx_lb: true
load_balancer_is_required: true

```
![](./img/project13/env-var%20for%20dev.yml.png)

- Running the playbook: `$ sudo ansible-playbook -i /home/ubuntu/ansible-config-artifact/inventory/dev.yml /home/ubuntu/ansible-config-artifact/playbooks/site.yml`

![](./img/project13/running%20the%20playbook.png)

