# DEVOPS_JENKINS_101

In this project, I created an end-to-end Production like CI-CD pipeline  while keeping in mind Securities Best Practices,DevSecOps principles and used all these tools *Git, GitHub, Jenkins, Maven, JUnit, SonarQube, Jfrog Artifactory, Docker, Trivy, AWS S3, Docker Hub, GitHub CLI, EKS, ArgoCD, Prometheus, Grafana, Slack and Hashicorp Vault,*  to achieve the goal.

#### I used Jenkins for Continuous Integration and ArgoCD for Continuous Deployment.

## Project Architecture
![pipeline](./images/pipeline.png)

## Pipeline flow:
1. When an event (commit) will occur in the application code GitHub repo,  the GitHub webhook will push the code to Jenkins and Jenkins will start the build.

2. Maven will build the code, if the build fails, the whole pipeline will become a failure and Jenkins will notify the user using Slack, If build success then

3.  Junit will do unit testing, if the application passes test cases then will go to the next step otherwise the whole pipeline will become a failure Jenkins will notify the user that your build fails.

4.  SonarQube scanner will scan the code and will send the report to the SonarQube server, where the report will go through the quality gate and gives the output to the web Dashboard.

 5. In the quality gate, we define conditions or rules like how many bugs or vulnerabilities, or code smells should be present in the code. 
                    Also, we have to create a webhook to send the status of quality gate status to Jenkins.
 If the quality gate status becomes a failure, the whole pipeline will become a failure then Jenkins will notify the user that your build fails.

5. After the quality gate passes, Artifacts will be sent to Jfrog Artifactory. If artifacts send to the artifactory successfully then will go to the next stage otherwise the whole pipeline will become a failure Jenkins will notify the user that your build fails.

6. After successful artifacts push to Artifactory, Docker will build the docker image.
if the docker build fails when the whole pipeline will become a failure and Jenkins will notify the user that your build fails.

6. Trivy will scan the docker image, if it finds any Vulnerability then the whole pipeline will become a failure, and the generated report will be sent to s3 for future review and Jenkins will notify the user that your build fails.

7. After the Trivy scan docker images will be pushed to the docker hub, if the docker fails to push docker images to the docker hub then the pipeline will become a failure and Jenkins will notify the user that your build fails.

8. After the docker push, Jenkins will clone the Kubernetes manifest repo from the feature branch, if the repo is already present then it will only pull the changes. If Jenkins is unable to clone the repo then the whole pipeline will become a failure and Jenkins will notify the user that your build fails.

9. After Cloning the repo, Jenkins will update the image tag in the deployment manifest. If Jenkins is unable to update the image tag  then the whole pipeline will become a failure and Jenkins will notify the user that your build fails.

10. After updating the image tag, Jenkins will commit the change and push the code to the feature branch. If Jenkins is unable to push the changes to the feature branch  then the whole pipeline will become a failure and Jenkins will notify the user that your build fails.

11. After pushing changes to the feature branch, Jenkins will create a pull request against the main branch. If Jenkins is unable to create a pull request  then the whole pipeline will become a failure and Jenkins will notify the user that your build fails.

12. After the pull request creation, a senior person from the team will review and merge the pull request.

13. After merging the feature branch into the main branch, ArgoCD will pull the changes and deploy the application into Kubernetes.

### PreRequisites
1. JDK 
1. Git 
1. Github
1. GitHub CLI
1. Jenkins
1. Sonarqube
1. Jfrog Artifactory
1. Docker
1. Trivy
1. AWS account
1. AWS CLI
1. Docker Hub account
1. Terraform
1. EKS Cluster
1. kubectl
1. ArgoCD
1. Helm
1. Prometheus & Grafana
1. Hashicorp Vault
1. Slack

## Server Configuration ( I used )

1. 2 t2.medium ( ubuntu) EC2 Instances –  1. one for sonarqube and Hashicorp vault server  & 2. another for Jfrog Artifactory

3. 1 t2.large (ubuntu ) EC2 Instance -  For Jenkins, Docker, Trivy, AWS CLI, Github CLI, Terraform

4. EKS Cluster with t3.medium nodes


### Want to create this Project on your own  then *Follow these  project steps*

## Step: 1 Installation Part 

### Stage-01: Install JDK and Create a Java Springboot application
Push all the web application  code files into GitHub

![deeee](./images/Screenshot%20from%202023-06-23%2022-45-05.png)

### Stage-02: Install Jenkins, Docker, Trivy, AWS CLI, Github CLI, Terraform ( t2.large node1 -Jenkins-server)

#### Jenkins Installation Prerequisites  https://www.jenkins.io/doc/book/installing/linux/

1. Installation guide is available here  ./Jenkins_installation.md
2. After installation, install the suggested plugins
3. Open Jenkins Dashboard and install required plugins – SonarQube Scanner, Quality gates, Artifactory, Hashicorp Vault, Slack, Open Blue Ocean
4. go to manage Jenkins > manage plugins > search for plugins > Download now and install after restart

![deeee](./images/jenkins.png)

### Docker Installation

1. Install docker using this command 

```sh
sudo apt install docker.io
```

2. Add the current user and Jenkins user into the docker group

```sh
sudo usermod -aG docker $USER
sudo usermod -aG docker jenkins
```

### Trivy Installation

1. Install **Trivy** using these commands

```sh
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

### AWS CLI installation

1. install aws cli  using these commands

```sh 
sudo apt install unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Install GitHub CLI

1. install GitHub cli using these commands

```sh 
# Check if curl is installed, and install it if not
type -p curl >/dev/null || { sudo apt update && sudo apt install curl -y; }

# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```

### Install Terraform

1. install terraform using these commands

```sh 
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring \
	--keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
	--fingerprint
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt-get install terraform
```

### Stage-03 : Install SonarQube and Hashicorp Vault ( t2.medium node2 - SonarQube Server )

#### SonarQube installation

1. install docker on the sonarqube server

```sh
sudo apt update
sudo apt install docker.io
```

2. create a docker container to install SonarQube

```sh
sudo docker run -d -p 9000:9000 --name sonarqube sonarqube  
```

#### Install the Hashicorp Vault server 

HashiCorp Vault is a secret-management tool specifically designed to control access to sensitive credentials in a low-trust environment.

1. Installation vault using these commands

```sh
sudo curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt update
sudo apt install vault -y
```

### Stage-04: Install Jfrog Artifactory ( t2.medium node3 - Jforg-artifactory server)

1. install the docker

```sh
sudo apt update
sudo apt install docker.io
```

1. Install Jfrog Artifactory

```sh
sudo docker pull docker.bintray.io/jfrog/artifactory-oss:latest
sudo mkdir -p /jfrog/artifactory
sudo chown -R 1030 /jfrog/
sudo docker run --name artifactory -d -p 8081:8081 -p 8082:8082 \
	-v /jfrog/artifactory:/var/opt/jfrog/artifactory \
	docker.bintray.io/jfrog/artifactory-oss:latest
```

### Stage-05 : Install Slack ( on your local system or login in google chrome)

Slack is a workplace communication tool, “a single place for messaging, tools and files." Install Slack from the official website of Slack https://slack.com/intl/en-in/downloads/linux

### Stage-06: EKS Cluster Creation using Terraform 

To create EKS Cluster using Terraform, I have put the Terraform code here - https://github.com/DevOpsCloudNinjas/medicure-project/tree/master/eks_module

`Suggestion – create eks cluster after successful configuration of jenkins server. When jenkins is able to create pull request in the manifest repo.`

> Note: I have installed the terraform in the jenkins server and configured aws cli to create eks cluster. But you can use your local system to create eks cluster . for this, you have to install Terraform and aws cli on your local system.

Run this command after eks cluster creation to update or configure `.kube/config` file

```sh
aws eks --region your-region-name update-kubeconfig --name cluster-name
```

### Stage-07: Install ArgoCD in EKS 

I am assuming that you have already Kubernetes cluster running
1. use these commands to install argocd

```sh
kubectl create namespace argocd 
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

2. edit the argocd-server service to NodePort to access argocd ui

```sh
kubectl -n argocd edit svc argocd-server
```

### Stage-08: Install helm ( on the system from where you are creating eks cluster)

1. use these commands to install the helm

```sh
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### Stage-09: Install Prometheus and Grafana ( from where you have installed helm)

1. use helm to install Prometheus and grafana

```sh
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm search repo prometheus-community
kubectl create namespace prometheus
helm install stable prometheus-community/kube-prometheus-stack -n prometheus
kubectl get pods -n prometheus
kubectl get svc -n prometheus
#in order to make Prometheus and grafana available outside the cluster, use LoadBalancer or NodePort instead of ClusterIP.
#Edit Prometheus Service
kubectl edit svc stable-kube-prometheus-sta-prometheus -n prometheus
#Edit Grafana Service
kubectl edit svc stable-grafana -n prometheus
kubectl get svc -n prometheus

#Access Grafana UI in the browser using load balancer or nodeport

UserName: admin 
Password: prom-operator
```

> Done with Installation, Now will we Configure each the tools

## Step: 2 Configure Individual tool

### Stage-01 : Jenkins Configuration

1. go to Manage Jenkins > configure tools > go to maven> give some name and click on install automatically

2. go to Manage Jenkins > configure tools > go to sonarqube scanner > give some name and click on install automatically

### Stage-02: Hashicorp Vault Configuration

I am assuming that your Vault server is installed and  running 
* open the ` /etc/vault.d/vault.hcl` file with vi or nano
* replace all the content of this file with this

```
storage "raft" {
  path    = "/opt/vault/data"
  node_id = "raft_node_1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true
```

```sh
sudo systemctl stop vault
sudo systemctl start vault
```

#### Commands to run to configure Vault and create AppRole

```sh 
export VAULT_ADDR='http://127.0.0.1:8200'
```

```sh 
vault operator init
```

* ` copy the unseal tokens and initial root token, save it somewhere for later use `

```sh 
vault operator unseal
```
* `Paste the first unseal token here`
```sh 
vault operator unseal
```
* `Paste the second unseal token here`
```sh 
vault operator unseal
```
* `Paste the third unseal token here`
```sh 
vault login <Initial_Root_Token>
```
* `<Initial_Root_Token>` is found in the output of `vault operator init`

```sh 
vault auth enable approle
```
  	
```sh 
vault write auth/approle/role/jenkins-role token_num_uses=0 secret_id_num_uses=0 policies="jenkins"
```
* `This app role will use for jenkins integration` 
```sh 
vault read auth/approle/role/jenkins-role/role-id
```
* `Copy the role_id and token, and store somewhere`
```sh 
vault write -f auth/approle/role/jenkins-role/secret-id
```
* `Copy the secret-id and token, store them somewhere`


### Stage-03: SonarQube Server Configuration

1. Access the sonarqube ui using the public IP of the server and port 9000
2. default username-password `admin`  and ` admin`

## Project setup

1. chose use global setting
![11](./images/sonarqube-.png)

2.  create a project manually, give some name to project, project key
![22](./images/sonarqubedb.png) 

3. click on setup
4. click on other ci
5. give some name to the token and click on generate, save it for a later user
6. click on global
7. select the project type, in this case, I used Maven

 ![333](./images/soanr.png)  

8. copy the whole command and save it somewhere

#### Create Quality Gate 

1. Click on Quality Gates
2. Create a new Quality Gate according to your conditions

![444](./images/quality%20gate.png)

3. Click on Projects > click on all > select your project

![122](./images/qualiygate.png   )
4. Set as default

##### Create webhook

1. Click on Administration
2. Click on Configuration > click on webhooks
3. Create a webhook > Give some name
4. for url use `http://jenkins-server-url-with-port/sonarqube-webhook/`

![452](./images/webhook.png)

5. In secret leave the blank
6. Click on create

> Note: if this webhook does not work fine, then recreate the webhook after integrating the soanrqube with jenkins

### Stage-04: Artifactory Configuration

1. access the UI with public IP and port 8081
2. use username-password as `admin` and `password`
3. update the password
4. create a Maven repo
5. now go to Administration > User management > Create a new user
6. now go to Repositories > create > locally > give some name like `my-local-repo`

### Stage-05: S3 Bucket creation to store Trivy report

1. login into aws account
2. search for S3
3. create a bucket with a unique name

### Stage-06: DockerHub account creation

If you already have a dockerhub account then no need to create another

1. go to dockerhub official website
![256](./images/dockerhub.png)

2. click on sign up
3. fill in the details and sing up
4. login into dockerhub

Note: we can create token from dockerhub to integrate jenkins but in this case, I am using docker username and password.

### Stage-07: Slack Configuration for jenkins

1. Go to this site https://slack.com/intl/en-in
2. sign up with Google
3. create a workspace
4. just give a name
5. you can skip add team member
6. give some name to team working ( channel name like - cicd-pipeline)
7. now go to this site https://slack-t8s2905.slack.com/intl/en-in/apps
8. login into your workspace (if need)
9. now click on Get Essential Apps
10. search Jenkins in search bar > click on it 
11. Click on Add to Slack
12. select channel name

![785](./images/slack.png)

13. Click on Add Jenkins CI Integration
14. Go down  to step 3 and copy Integration Token Credential ID and save it somewhere
15. Click on Save settings

### Stage-08: Slack Configuration for ArgoCD 

1. Go to this site https://api.slack.com/apps
2. click on Create New App
3. select From scratch
4. give some app name
5. pick your workspace
6. click on Create App
7. go to OAuth & Permission
8. go to Scope > Bot Token Scope
9. search in the search bar and select `chat:write` ,`chat:write.customize`
10. now to up to OAuth Token for Your Workspace
11. click on Install to workspace
12. allow your app to access your workspace
13. now copy Bot user OAuth Token and save it somewhere
14. now open slack , you will find your app in Apps
15. now create a channel - click on channels > create channel > give some name to channel > create
16. now in message bar type `@your-app-name` and click on send icon >  click on add to channel

> Done with Configuration of all tools, Now will we store the credentials into Vault server.

## Step: 3 Store the Credentials in the Vault server
Run all these commands into the vault server

1. enable secrets path

```sh
vault secrets enable -path=secrets kv
```

2. write the secret into secret path

```sh
vault write secrets/creds/docker username=abcd password=xyz
```

Likewise, we can store all the credentials in the vault server. I have stored only the docker credential. But you can store all your credential like this.

3. create a jenkins policy file with vi or nano ` jenkins-policy.hcl`

```groovy
path "secrets/creds/*" {
 capabilities = ["read"]
}
```

The policy is created with * means the vault server can read credentials from every path. No need to create policies for each path like `secrets/creds/docker` , `secrets/creds/slack` etc…

4. run this command to create a policy

```sh
vault policy write jenkins jenkins-policy.hcl
```

> Done with Configuration of all tools, Now will we integrate tools with jenkins

## Step: 4 Integrate all the tools into jenkins for CI

### Stage-01: Hashicorp Vault server integration with Jenkins

1. go to Jenkins>  Manage  Jenkins >Manage Credentials > system > Add credentials > Vault App Role Credentials > Paste role-id and secret-id token (we create in Vault - approle)  and save and apply.

![252](./images/approleVault.png) 

2. now to  Manage  Jenkins  >  configure system/system>  search for vault plugin
3. give the URL of the vault server
4. attach the credentials we created
5. click on Advanced
6. select k/v engine as 1
7. click on skip ssl verification
8. Apply and Save

### Stage-02: SonarQube server integration with Jenkins

1.  go to Manage Jenkins>Manage Credentials > system > Add credentials > secret text file > paste the token we create in sonarqube and save and apply.
2. now to  Manage  Jenkins  >  configure system/system>  search for SonarQube Server
3. enable the environment  variables
4. write the name of Sonaqube server
5. paste the url of SonarQube server
6. select the credential
7. Apply and Save

### Stage-03: Jfrog Artifactory integration with Jenkins

1. go to Manage Jenkins>Manage Credentials > system > Add credentials > username and password > write the username and password we created in Jfrog artifacotry and save and apply.

2. now to  Manage  Jenkins  >  configure system/system>  search for Jfrog
3. give instance id as artifactory name
4. Jfrog Platform url - artifactory url like - http://localhost:8082
5. click on Advanced
6. JFrog Artifactory URL - http://localhost:8082/artifactory
7. JFrog Distribution URL - http://localhost:8082/distribution
8. Default Deployer Credentials – give username and password of artifactory (not admin user)
9. Apply and save

### Stage-04:  AWS S3 integration with Jenkins

1. for S3 integration we will configure aws cli in the pipeline itself
2. create credentials for aws cli, use both as the secret  text

### Stage-05:  DockerHub integration with Jenkins

1. go to Manage jenkins >Manage Credentials > system > Add credentials > vault Username-Password Credential
2. namespace – leave blank
3. Prefix Path – leave blank
4. Path – secrets/creds/docker
5. Username Key- username
6. Password key – password
7. k/v engine – 1
8. id – give some id like docker-cred
9. Description -  give some description
10. click on Test Vault Secrets retrieval  > should give output as secrets retrieved successfully otherwise reconfigure the vault server in jenkins
11. Apply and Save

### Stage-05:  Slack integration with Jenkins

1. Go to Manage Jenkins>Manage Credentials > system > Add credentials > secret text file > give some name to credentials, paste the token we create in the Slack app and save and apply.
2. now to  Manage  Jenkins  >  configure system/system>  search for Slack
![142](./images/slcakws.png)

3. workspace – your workspace name ( you create after login into Slack)
4. Credential – attach the slack token
5. Default channel name – write the channel name we created at the time of slack installation like - #cicd-pipeline
6. Apply and save

### Stage-06:  GitHub integration with Jenkins ( application code repo)

1. Go to GitHub  > go to application code repo > settings
2. Go to webhook >  Add webhook
3. Payload URL -  http://jenkins-server-public-ip-with-port/github-webhook/
4. Click on Add Webhook

> Done with the integration  of tools with jenkins, Now will we integrate tools with ArgoCD

## Step: 5 Integrate ArgoCD with GitHub and Slack for CD

### Stage-01:  ArgoCD integration with Github ( k8s manifest repo)

1. access the argocd UI – node public ip and node port
2. user username as `admin`
3. for password run this command

```sh
kubectl -n argocd get secret argocd-initial-admin-secret -o yaml
```

4. copy the password and decode it using

```sh
echo “copied-password” | base64 -d
```

5. Copy the decoded password and login into argocd
6. Go to User Info – update password
7. Now go to Application
8. Click on New Application
9. Give app name
10. Chose Project Name as default
11. SYNC Policy – Automatic
12. enable PRUNE RESOURCES and SELF HEAL
13. SOURCE-
14. Repository URL – give your repo URL where you stored the k8s manifest
15. Path – yamls
16. DESTINATION -
17. Cluster Url – chose default
18. namespace- default
19. click on create

### Stage-02:  Slack integration with ArgoCD

1. encode your Slack token using this command ( Bot Token )

```sh
echo "your-slack-token" | base64
```

2. edit `argocd-notifications-secret` secret to add slack token

```sh
kubectl -n argocd edit secret argocd-notifications-secret
```

3. Add data field after `apiVersion: v1`, Replace `xxxx-xxxxx-xx` with your encoded slack token

```sh
data:
  slack-token: xxxxx-xxxxxx-xxxxxx
```

4. now edit `argocd-notifications-cm` configmap

```sh
kubectl -n argocd edit cm argocd-notifications-cm
```

5. add this service for slack after `apiVersion: v1`

```yml
data:
  service.slack: |
    token: $slack-token
    username: argocd-bot
    icon: ":rocket:"
  template.app-sync-succeeded-slack: "message: | \n      Application {{.app.metadata.name}}
    is now {{.app.status.sync.status}}\n"
  trigger.on-sync-succeeded: |
    - when: app.status.sync.status == 'Synced'
      send: [app-sync-succeeded-slack]
```

6. add slack notification annotation in application

```groovy
kubectl -n argocd edit application your-app-name-you-created-in-argocd
```

7. add this annotation in metadata section like this

```yml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: your-slack-channel-name
  name: argocd-demo
  namespace: argocd
```

### Stage-03:  Prometheus and Grafana Integration

use this docs to import grafana Dashboard into grafana
https://www.DevOpsCloudNinjas.com/2022/05/how-to-setup-monitoring-on-kubernetes.html

> We integrated all the tools with Jenkins, Now Create a declarative jenkins  pipeline for each stage.

## Step: 6 Pipeline creation

### General Jenkins  declarative Pipeline Syntax

```groovy
pipeline {
    agent any
    tools {
        maven 'apache-maven-3.0.1' 
    }
    stages {
        stage('Example') {
            steps {
                sh 'mvn --version'
            }
        }
    }
}
```

### Stage-01 : Git Checkout

1. Define a stage as git checkout
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for checkout: check out version control
4. give your GitHub URL, branch and generate the pipeline syntax
5. paste it into stage steps git check

```groovy
stage('Checkout git') {
            steps {
              git branch: 'main', url:'https://github.com/DevOpsCloudNinjas/DEVOPS_JENKINS_101.git'
            }
        }
```

### Stage-02: Build and Junit test

1. Define a stage as Build and Junit test 
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for sh: shell script 
4. give your shell command and generate the pipeline syntax
5. paste it into stage >  steps > sh ‘ shell command’

```groovy
stage ('Build & JUnit Test') {
	steps {
		sh 'mvn install' 
	}
}
```

### Stage-03 : SonarQube Analysis

In this stage, I used withSonarQubeEnv to  Prepare the SonarQube Scanner environment
and shell command sh

1. Define  a stage SonarQube Analysis
2. paste the command that we created at the time of the sonarqube project creation

```groovy
stage('SonarQube Analysis'){
            steps{
                withSonarQubeEnv('SonarQube-server') {
                        sh '''mvn clean verify sonar:sonar \
                        -Dsonar.projectKey=gitops-with-argocd \
                        -Dsonar.projectName='gitops-with-argocd' \
                        -Dsonar.host.url=$sonarurl \
                        -Dsonar.login=$sonarlogin'''
                }
            }
        }
```

### Stage-04 : Quality gate

This step pauses Pipeline execution and waits for the previously submitted SonarQube analysis to be completed and returns quality gate status. Setting the parameter abortPipeline to true will abort the pipeline if the quality gate status is not green.

1. Define a stage as a Quality gate
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for  waitForQualityGate: Wait for SonarQube analysis to be completed and return quality gate status
4. generate pipeline syntax and paste it into steps
5. timeout is optional 

```groovy
stage("Quality Gate") {
            steps {
              timeout(time: 1, unit: 'HOURS') {
                waitForQualityGate abortPipeline: true
              }
            }
          }
```

### Stage-05 : Jfrog Artifactory

1. We wrap the steps in a script block to execute them as a Groovy script.
2. Inside the try block, we create a reference to the Artifactory server using the Artifactory.newServer method. You need to provide the URL of your Artifactory instance and the credentials ID configured in Jenkins.
3. We define an uploadSpec as a JSON string, specifying the pattern of files to upload and the target repository in Artifactory.
4. We call the server.upload(uploadSpec) method to upload the files to Artifactory based on the specified upload specification.
5. If any exception occurs during the upload process, the catch block will be executed, and an error message will be displayed.

```groovy
steps {
    script {
        try {
            def server = Artifactory.newServer(url: 'http://13.232.95.58:8082/artifactory', credentialsId: 'jfrog-cred')
            def uploadSpec = """{
                "files": [
                    {
                        "pattern": "target/*.jar",
                        "target": "${TARGET_REPO}/"
                    }
                ]
            }"""
            server.upload(uploadSpec)
        } catch (Exception e) {
            error("Failed to deploy artifacts to Artifactory: ${e.message}")
        }
    }
}
```

### Stage-06 : Docker Build

First, write your dockerfile to build docker images. I have posted my dockerfile in  the application repo code
In this stage, I  used the shell command sh to build the docker image

1. Define  a stage Docker Build
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for sh: shell script 
4. give your shell command to build image > generate pipeline syntax
5. I used the build-id of jenkins and git commit id for versions of docker images

```groovy
stage('Docker  Build') {
            steps {
      	         sh 'docker build -t ${IMAGE_REPO}/${NAME}:${VERSION}-${GIT_COMMIT} .'
                
            }
        }
```

### Stage-07: Trivy Image scan

In this stage, I  trivy shell command sh to scan the docker image

1. Define  a stage Trivy Image scan
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for sh: shell script
4. Give your Trivy shell command to scan the docker image

> Note – There are 3 types of report output  formats of trivy ( Table, JSON, Template). I used  HTML template for the output report of the trivy scan

```groovy
stage('Image Scan') {
    steps {
        // Scanning the image using Trivy and generating an HTML report
        sh 'trivy image --format template --template "@/usr/local/share/trivy/templates/html.tpl" -o report.html ${IMAGE_REPO}/${NAME}:${VERSION}-${GIT_COMMIT}'

        // Assuming you want to push the image to a repository after scanning
        // sh 'docker push ${IMAGE_REPO}/${NAME}:${VERSION}-${GIT_COMMIT}'
    } 
}
```

### Stage-08: Upload report generated by trivy to AWS S3

In this stage, I used the shell command sh to Upload Scan report to AWS S3

1. Define  a stage Upload report to AWS S3
2. first create an AWS s3 bucket
3. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
4. search for sh: shell script
5. give your shell command to upload the object to aws s3

```groovy
stage('Upload Scan report to AWS S3') {
    steps {
        // Uncomment and use these lines if AWS credentials are not set elsewhere in your Jenkins setup
        // sh 'aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"'
        // sh 'aws configure set aws_secret_access_key "$AWS_ACCESS_KEY_SECRET"'
        // sh 'aws configure set region "ap-south-1"'
        // sh 'aws configure set output "json"'

        // Command to copy the report to an S3 bucket
        sh 'aws s3 cp report.html s3://devops-mastepiece/'
    }
}
```

### Stage-09: Push Docker images to DockerHub

In this stage, I used   the shell command sh to push the docker image to the docker hub. I stored Credentials in Vault and accessed them in jenkins using  the Vault key. You can store DockerHub credentials in jenkins and use them as environment variables

1. Define  a stage Docker images push
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/

3. search for sh: shell script
4. give your shell command to push docker images to the docker hub

 ```groovy
stage ('Docker Build') {
            steps {
                withVault(configuration: [skipSslVerification: true, timeout: 60, vaultCredentialId: 'vault-token', vaultUrl: 'http://13.232.53.209:8200'], vaultSecrets: [[path: 'secrets/creds/docker', secretValues: [[vaultKey: 'username'], [vaultKey: 'password']]]]) {
                    
                    sh "docker login -u ${username} -p ${password} "
                    sh 'docker push ${IMAGE_REPO}/${NAME}:${VERSION}-${GIT_COMMIT}'
		    	sh 'docker rmi  ${IMAGE_REPO}/${NAME}:${VERSION}-${GIT_COMMIT}'
                    
                    
                }
            }
        }
 ``` 

### Stage-10: Clone/Pull Repo (k8s manifest repo )

1. In this stage first we check whether the repo already exists or not
2. If exists then pull the changes
3. If not then will clone the repo

 ```groovy
stage('Clone/Pull Repo') {
            steps {
                script {
                    if (fileExists('DevOps_MasterPiece-CD-with-argocd')) {

                        echo 'Cloned repo already exists - Pulling latest changes'

                        dir("DevOps_MasterPiece-CD-with-argocd") {
                          sh 'git pull'
                        }

                    } else {
                        echo 'Repo does not exists - Cloning the repo'
                        sh 'git clone -b feature https://github.com/DevOpsCloudNinjas/DevOps_MasterPiece-CD-with-argocd.git'
                    }
                }
            }
        }
```

### Stage: 11 Update Manifest

1. used sed command to replace images tag in deployment manifests

```groovy
stage('Update Manifest') {
            steps {
                dir("DevOps_MasterPiece-CD-with-argocd/yamls") {
                    sh 'sed -i "s#praveensirvi.*#${IMAGE_REPO}/${NAME}:${VERSION}-${GIT_COMMIT}#g" deployment.yaml'
                    sh 'cat deployment.yaml'
                }
            }
        }
```

### Stage: 12 Commit and Push Changes to the k8s manifest repo

1. set the global username
2. set the remote repo URL
3. checkout the branch to feature
4. stage the changes
5. commit the changes
6. push the changes to the feature branch

```groovy
stage('Commit & Push') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    dir("DevOps_MasterPiece-CD-with-argocd/yamls") {
                        sh "git config --global user.email 'praveen@gmail.com'"
                        sh 'git remote set-url origin https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME}'
                        sh 'git checkout feature'
                        sh 'git add deployment.yaml'
                        sh "git commit -am 'Updated image version for Build- ${VERSION}-${GIT_COMMIT}'"
                        sh 'git push origin feature'
                    }
                }    
            }
        }
```

### Stage: 13 Create Pull Request

`The reason to create a pull request is that argocd is sync automatically with Git Hub. GitHub is the only single source of truth for argocd. So if jenkins push the changes to the main branch then argocd will deploy changes directly without reviewing the changes. This should not happen in the Production environment. That’s why we create pull requests against the main branch. So a senior person from the team can review the changes and merge them into the main branch. Then n then only changes should go to the production environment.`

Here `token.txt` contain the GitHub token, the reason for storing the GitHub token in the text file bcoz `gh auth login --with-token` accept only STDIN Input.

```groovy
stage('Raise PR') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    dir("DevOps_MasterPiece-CD-with-argocd/yamls") {
                        sh '''
                            set +u
                            unset GITHUB_TOKEN
                            gh auth login --with-token < token.txt
                            
                        '''
                        sh 'git branch'
                        sh 'git checkout feature'
                        sh "gh pr create -t 'image tag updated' -b 'check and merge it'"
                    }
                }    
            }
        } 
```

### Stage: 14 Post build action 

In post build action I used Slack notification. After  the build jenkins will send a notification message to Slack whether your build success or failure.

1. Go to jenkins > your project > pipeline syntax > search for slacksend: send slack message 

2. write your channel name and message > generate pipeline syntax.

#### Note – I used custom messages for my project. I created a function for Slack notification and called the function into Post build.

```groovy
post{
	always{
		sendSlackNotifcation()
	}
}
```

### Send SlackNotification function 

```sh
def sendSlackNotifcation()
{
    if ( currentBuild.currentResult == "SUCCESS" ) {
        buildSummary = "Job_name: ${env.JOB_NAME}\n Build_id: ${env.BUILD_ID} \n Status: *SUCCESS*\n Build_url: ${BUILD_URL}\n Job_url: ${JOB_URL} \n"
        slackSend( channel: "#devops", token: 'slack-token', color: 'good', message: "${buildSummary}")
    }
    else {
        buildSummary = "Job_name: ${env.JOB_NAME}\n Build_id: ${env.BUILD_ID} \n Status: *FAILURE*\n Build_url: ${BUILD_URL}\n Job_url: ${JOB_URL}\n  \n "
        slackSend( channel: "#devops", token: 'slack-token', color : "danger", message: "${buildSummary}")
    }
}

 ```

#### Find the whole pipeline here

``` sh
./Jenkinsfile
```

## Step: 7 Project Output

### Final outputs of this Project

### Jenkins Output : 

Sorry, I forgot to change the stage name while building the job, but don't worry I made changes in the Jenkins file.

![deeee](./images/jenkins.png)

### Sonarqube Output: 
![deeee](./images/sonarqube.png) 

### Quality Gate Status in Jenkins
 SonarQube Quality gate status is green and passed.   
You can apply your custom quality gate like there should be zero ( bug, Vulnerability, code smell ) and if your code has greater than 0 (bugs, vulnerability, code smells). Then your quality gate status will become a failure or red. If your quality gate status becomes a failure, stages after the quality gate will be a failure.
![deeee](./images/quality-gate.png)

### Trivy report in AWS S3 push by jenkins
![deeee](./images/trivy-report.png) 


### Trivy report 
![deeee](./images/Screenshot%20from%202023-06-23%2023-59-22.png)


### Images in DockerHub pushed by jenkins 
![deeee](./images/dockerhub.png)

### Image tag updated by jenkins and push changes to feature branch
![deeee](./images/Screenshot%20from%202023-06-24%2000-06-51.png) 

### Pull Request created by jenkins in DevOps_MasterPiece-CD-with-argocd GitHub repo
![deeee](./images/pr.png)

### App in ArgoCD  
![deeee](./images/argocd.png)


### Application output deployed in EKS Cluster by ArgoCD 
![deeee](./images/Screenshot%20from%202023-06-22%2023-24-29.png)

### Slack output of jenkins
![deeee](./images/Screenshot%20from%202023-06-22%2023-24-05.png)

### Slack output of ArgoCD
![deeee](./images/Screenshot%20from%202023-06-22%2023-58-34.png)

### Prometheus  
![deeee](./images/Screenshot%20from%202023-06-22%2023-20-00.png)

### Grafana  
![deeee](./images/Screenshot%20from%202023-06-22%2023-19-50.png)