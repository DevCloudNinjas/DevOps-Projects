# DevSecOps-Project

In this project, I created an end-to-end CI/CD pipeline while keeping in mind Securities Best Practices, DevSecOps principles and used all these tools *Git, GitHub , Jenkins,Maven, Junit, SonarQube, Docker, Trivy, AWS S3, Docker Hub, Kubernetes , Slack and Hashicorp Vault,*  to achive the goal.


## Project Architecture

![blessed](./Images/architecture.png)

## Pipeline flow

1. Jenkins will fetch the code from the remote repo 
2. Maven will build the code, if the build fails, the whole pipeline will become a failure and Jenkins will notify the user, If build success then
3. Junit will do unit testing, if the application passes test cases then will go to the next step otherwise the whole pipeline will become a failureJenkins will notify the user that your build fails.
4. SonarQube scanner will scan the code and will send the report to the SonarQube server, where the report will go through the quality gate and gives the output to the web Dashboard.
                        In the quality gate, we define conditions or rules like how many bugs or vulnerabilities, or code smells should be present in the code.
 Also, we have to create a webhook to send the status of quality gate status to Jenkins.
 If the quality gate status becomes a failure, the whole pipeline will become a failure then Jenkins will notify the user that your build fails.
5. After the quality gate passes, Docker will build the docker image.
if the docker build fails when the whole pipeline will become a failure and Jenkins will notify the user that your build fails.
6. Trivy will scan the docker image, if it finds any Vulnerability then the whole pipeline will become a failure, and the generated report will be sent to s3 for future review and Jenkins will notify the user that your build fails.
7. After trivy scan docker images will be pushed to the docker hub, if the docker fails to push docker images to the docker hub then the pipeline will become a failure and Jenkins will notify the user that your build fails.
8. After the docker push, Jenkins will create deployment and service in minikube and our application will be deployed into Kubernetes.

If Jenkins fails to create deployment and service in Kubernetes, the whole pipeline will become a failure and Jenkins will notify the user that your build fails.

### PreRequisites

1. JDK
2. Git
3. Github
4. Jenkins
5. Sonarqube
6. Docker
7. Trivy
8. AWS account
9. Docker Hub account
10. Minikube & Kubectl
11. Hashicorp Vault
12. Slack

> Want to create this Project by your own  then *Follow these  project steps*

## Step: 1 Installation Part

### Stage-01 : Install JDK and Create a Java Springboot application
Push all the web application page code file into github

![blessed](./Images/code.png) 

### Stage-02 : Install Jenkins and start Jenkins

Jenkins Installation Prequuisities  https://www.jenkins.io/doc/book/installing/linux/
1. Installation guide is available here  ./Jenkins_installation.md
2. After installation, install suggested plugins
3. Open Jenkins Dashboard and install required plugins – SonarQube Scanner, Hashicorp Vault, Slack
4. go to manage jenkins > manage pulgins > search for plugins > install without restart
![blessed](./Images/jenkins.png) 

5. We will required another pulgin called - Kubernetes Continuous Deploy Plugin ( this plugin is deprecated but we can down grade the version for just testing purpose)
Download the Plugin file from here ./kubernetes-cd.hpi
6. Now go to manage jenkins > manage pulgins > Advanced Setting > Deploy Plugin > choose the download file ( kubernetes-cd.hpi) > click on Deploy
![blessed](./Images/plugins.png) 

### Stage-03 : Install Postgre Database and Install SonarQube

7. Installation guide is available here ./sonarqube_installation_with_postgres_database.md
![blessed](./Images/sonarqube.jpeg) 

### Stage-04 : Install Docker and Create DockerHub account

8. Installation guide is available here ./docker_installation.md
9. Create DockerHub account 

![blessed](./Images/dockerhub.png) 

### Stage-05 : Install Trivy for Vulnerability Scanner for Containers and other Artifacts
I am following  Debian/Ubuntu  based installation guide you can choose accourding to your os

```sh
   sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

> After trivy installation you can scan Container Images, FileSystem, Git Repositories

In our can we will scan contianer images

```sh
   trivy image [YOUR_IMAGE_NAME]
```

### Stage-06 : Install Hashicorp Vault server 

HashiCorp Vault is a secret-management tool specifically designed to control access to sensitive credentials in a low-trust environment.

1. Installation guide is available here https://www.cyberithub.com/how-to-install-hashicorp-vault-on-ubuntu-20-04-lts/

### Stage-07 : Install Slack

Slack is a workplace communication tool, “a single place for messaging, tools and files.” .

Install Slack from official website of Slack https://slack.com/intl/en-in/downloads/linux

### Stage-08: Install Minikube

Minikube installation Guide is Available here  https://www.linuxtechi.com/how-to-install-minikube-on-ubuntu/

> Done with Installation , Now will we integrate all the tools with Jenkins

## Step: 2 Integeration Part

### Stage-01 : Hashicorp Vault integration with Jenkins

I am assuming that your Vault server is running.

Video guide to integrate Hashicorp Vault with Jnekins https://www.youtube.com/watch?v=5-RMu9M_Anc

##### 1. create Vault server App role and secret id 

* Copy the following to `/etc/vault.d/vault.hcl`

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

* `sudo systemctl stop vault`
* `sudo systemctl start vault`

#### Commands to run to configure Vault and create AppRole

* `export VAULT_ADDR='http://127.0.0.1:8200'`
* `vault operator init`
* `vault operator unseal`
* `vault operator unseal`
* `vault operator unseal`
* `vault login <Initial_Root_Token>`
   * `<Initial_Root_Token>` is found in the output of `vault operator init`
* `vault auth enable approle`
* `vault auth enable approle`
  * https://www.vaultproject.io/docs/auth/approle
* `vault write auth/approle/role/jenkins-role token_num_uses=0 secret_id_num_uses=0 policies="jenkins"`
* `vault read auth/approle/role/jenkins-role/role-id`
	* copy the role_id and store somewhere
* `vault write -f auth/approle/role/jenkins-role/secret-id`

##### 2. Now go to jenkins > Manage  Jenkins >Manage Credentials > system > Add credentials > Vault App Role Credentials > paste roleid and secret id token we create in Vault and save and apply.
![blessed](./Images/approleVault.png) 


 ### Stage-02: SonarQube integration with Jenkins

1. Open SonarQube and login using admin username and admin password
2. Create a Project >Enter Project name, Project key > click on setup
![blessed](./Images/sonarqubedb.png)
3. Create sonarqube token > and save it soemwhere
4. click on continue > Run analysis on your project > maven > copy following commands and save it some where
![blessed](./Images/soanr.png)
5. Now go to jenkins >Manage Credentials > system > Add credentials > secret text file > paste token we create in sonarqube and save and apply.

6. go to manage Jenkins > Configure System > Add SonarQube Server name,url and credentials
![blessed](./Images/sonarqube.png)
7. go to manage Jenkins > Global tool configuration >  Add Maven and SonarQube Scanner

8. Now go to SonarQube > Quality gates > create your own quality gate
![blessed](./Images/quality%20gate.png)
8. Add conditions with your own requirement
10. Select your project and Set this quality gate as defalut
![blessed](./Images/qualiygate.png)
11. Now go to your Project > project setting > webhook
12. create webhook with your Jenkins url
![blessed](./Images/webhook.png)

### Stage-03 : Add jenkins user to docker group

```sh 
sudo gpasswd -a jenkins docker
``` 

### Stage-04: Install and Configure AWS CLI

1. Installation Guide is Available here https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html 
2. go to AWS > create access key and secret key
3. configure aws cli using

```sh
aws configure
```

paste your  access key and secret key

#### Method 1
Configure aws cli for jenkins user also

> Note – in this project i used  method 1 but you can also use method 2

#### Method 2

1. go to jenkins > Manage Credentials > system > Add credentials > AWS credentials > give your access key and secret key > save

### Stage-05: DockerHub Integeration with jenkins for docker login

1. go to DockerHub > login into DockerHub
2. go to Account setting > security > generate a token
3. copy this token and save it some where

> in this project i used Hashicorp Vault to store my credentials for security purpose  but you can directly store in jenkins also . 

To store secrets into Vault

#### Commands to store `docker` secret into Vault

* `vault secrets enable -path=secrets kv`
  * https://www.vaultproject.io/docs/secrets/kv
* `vault write secrets/creds/docker username=your-dockerhub-username password=token-generated-in-dockerhub`
* Create jenkins-policy.hcl

```
path "secrets/creds/*" {
 capabilities = ["read"]
}
```

* `vault policy write jenkins jenkins-policy.hcl`

1. Now go to jenkins > Manage credentials > global > create credentials with ‘vault username-password credentials ’
2. give path of your credentials ‘secrets/creds/docker’ 
3. give username key as username and password key as password
4. give id name as you wish and description and save it 

### Stage-06 : kubernetes Integeration  with jenkins

1. go to jenkins > Manage credentials > System ( global) > Add credentials > tkind - Kubernetes configuration ( Kuberconfig)
2. give id and description
3. go to kubeconfig > Enter directly

Now you have to copy the content of your kubeconfig file of your cluster.
for that -

4. go to your home directory , you will find  ` .kube` 
5. change your directory to .kube and cat your config file

You will find your kubeconfig like this

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority:  /home/praveen/.minikube/ca.crt
    extensions:
    - extension:
        last-update: Fri, 24 Feb 2023 19:17:00 IST
        provider: minikube.sigs.k8s.io
        version: v1.28.0
      name: cluster_info
    server: https://192.168.49.2:8443
  name: minikube
contexts:
- context:
    cluster: minikube
    extensions:
    - extension:
        last-update: Fri, 24 Feb 2023 19:17:00 IST
        provider: minikube.sigs.k8s.io
        version: v1.28.0
      name: context_info
    namespace: default
    user: minikube
  name: minikube
- context:
    cluster: ""
    namespace: dev
    user: ""
  name: my-context
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate: /home/praveen/.minikube/profiles/minikube/client.crt
    client-key: home/praveen/.minikube/profiles/minikube/client.key
```

> Note : I encoded to base64 the data of ca.crt, client.key and client.crt and directly paste the data instead of /home/praveen/.minikube/profiles/minikube/client.crt . But you have to specify the `certificate- authority` to  

`certificate- authority-data` ,  `client-certificate` to  `client-certificate-data`,  `client-key` to  `client-key-data`

Now copy the config file data and paste into jenkins > save

### Stage-07 : Slack Integeration with Jenkins

1. Open Slack > create workspace > create channel
2. Now go to this site https://slack-t8s2905.slack.com/apps/new/A0F7VRFKN-jenkins-ci
3. Now choose your channel name

![blessed](./Images/slack.png)
4. Click on Add Jenkins CI inetegration
5. Copy the workspace name and token
6. store your secret token into Hashicorp Vault

* `vault write secrets/creds/slack secret=your-slack-token `
7. Now go to jenkins > Manage credentials > system (global ) > Vault sceret text credentials 
8. give your vault sercrets path, Vault key and save
9. Now go to configure system > slack > give your slack name and select credentials , give your Default channel name like ‘#devops’
![blessed](./Images/slcakws.png)

> We integrated all the tools with Jenkins, Now Create a declarative jenkins  pipeline for each stage.

## Step: 3 Pipeline creation

### General Jenkins  declarative Pipeline Syntax

I used Tools, Declarative Pipeline beccause we required build tool called maven

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

1. Defiine a stage as git checkout
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for checkout: check out version control
4. give your github url, branch and generate the pipeline synatx
5. paste it into stage steps git check

```groovy

stage('Checkout git') {
    steps {
	    git branch: 'main', url: 'https://github.com/DevOpsCloudNinjas/DevSecOps-project'
  }
}
```

### Stage-02 : Build and Junit test

1. Defiine a stage as Build and Junit test 
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for sh:shell script 
4. give your shell comman and generate the pipeline synatx
5. paste it into stage >  steps > sh ‘ shell command’
6. after build success , we want to test the code using junit
7. go to https://opensource.triology.de/jenkins/pipeline-syntax/
8. search for Junit:Archived Junit-formatted test result
9. give your xml test cases file > generate pipeline syntax
10. paste it into post success

```groovy
stage ('Build & JUnit Test') {
	steps {
		sh 'mvn install' 
	}
	post {
	    success {
		   junit 'target/surefire-reports/**/*.xml'
		} 
	}
}
```

### Stage-03 : SonarQube Analysis

In this stage i used withSonarQubeEnv to  Prepare SonarQube Scanner environment
and shell command sh
1. Define  a stage SonarQube Analysis
2. paste the command that we created at the time of sonarqube project creation

```groovy
stage('SonarQube Analysis'){
	steps{
	    withSonarQubeEnv('SonarQube-server') {
		sh 'mvn clean verify sonar:sonar \
		-Dsonar.projectKey=devsecops-project-key \
		-Dsonar.host.url=$sonarurl \
		-Dsonar.login=$sonarlogin'
		}
	}
}
```

### Stage-04 : Quality gate

This step pauses Pipeline execution and wait for previously submitted SonarQube analysis to be completed and returns quality gate status. Setting the parameter abortPipeline to true will abort the pipeline if quality gate status is not green.

1. Defiine a stage as Quality gate
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

### Stage-05 : Docker Build
First write your dockerfile to build docker images.I have posted my  dockerfile here ./Dockerfile .

In this stage i  shell command sh to build docker image

1. Define  a stage Docker Build
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for sh:shell script 
4. give your shell command to build image > generate pipeline syntax
5. I used build id of jenkins to make versions of docker images

```groovy
stage('Docker Build') {
      steps {
           sh 'docker build -t praveensirvi/sprint-boot-app:v1.$BUILD_ID .'
           sh 'docker image tag praveensirvi/sprint-boot-app:v1.$BUILD_ID praveensirvi/sprint-boot-app:latest'
	}
}
```

### Stage-06: Trivy Image scan

In this stage i  trivy shell command sh to scan docker image

1. Define  a stage Trivy Image scan
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for sh:shell script
4. Give your Trivy shell command to scan build image

> Note – There are 3 types of report output  format of trivy ( Table , JSON, Template). I used  html template for output report of trivy scan

```groovy
stage('Image Scan') {
    steps {
        sh '''
            set +e  # Disable immediate exit on error
            trivy image --format template --template "@/usr/local/share/trivy/templates/html.tpl" -o report.html praveensirvi/sprint-boot-app:latest
            SCAN_EXIT_CODE=$?
            if [ $SCAN_EXIT_CODE -ne 0 ]; then
                echo "Image scan failed with exit code $SCAN_EXIT_CODE"
                exit 1
            fi
        '''
    }
}

```

### Stage-07: Upload report generated by trivy to AWS S3

In this stage i  shell command sh to scan docker image

1. Define  a stage Upload report to AWS S3
2. first create a AWS s3 bucket 
3. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
4. search for sh:shell script
5. give your shell command to upload object to aws s3

```groovy
stage('Upload Scan Report to AWS S3') {
    steps {
        sh 'aws s3 cp report.html s3://devsecops-project/'
    }   
}
```

> Note – in this Porject i configure aws cli for jenkins user also and execute just shell command . But you can use another method , save your credentials into jenkins and generate a pipeline to upload object to s3.

For that - S3 plugins should be installed

Pipeline Syntax 

```groovy
stage("Upload") {
    steps {
        withAWS(region: "${env.region}", credentials: "${env.aws_credential}") {
            s3Upload(file: "${env.TAG_NAME}", bucket: "${env.bucket}", path: "${env.TAG_NAME}/")
        }
    }
}
 ``` 

### Stage-08: Push Docker images to DockerHub

In this stage i shell command sh to push docker image to docker hub. I stored Credentials into Vault and access into jenkins using  vault key. You can store DockerHub credentials into jenkins and use as environment variables

1. Define  a stage Docker images push
2. go to this site https://opensource.triology.de/jenkins/pipeline-syntax/
3. search for sh:shell script
4. give your shell command to push docker images to docker hub

``` groovy
stage('Docker Push') {
    steps {
        withVault(
            configuration: [
                skipSslVerification: true, 
                timeout: 60, 
                vaultCredentialId: 'vault-cred', 
                vaultUrl: 'http://your-vault-server-url:8200'
            ],
            vaultSecrets: [
                [
                    path: 'secrets/creds/docker', 
                    secretValues: [
                        [vaultKey: 'username'], 
                        [vaultKey: 'password']
                    ]
                ]
            ]
        ) {
            sh "docker login -u ${env.username} -p ${env.password}"
            sh "docker push praveensirvi/sprint-boot-app:v1.${env.BUILD_ID}"
            sh "docker push praveensirvi/sprint-boot-app:latest"
            sh "docker rmi praveensirvi/sprint-boot-app:v1.${env.BUILD_ID} praveensirvi/sprint-boot-app:latest"
        }
    }
}
```

### Stage-08: Deploy to kubernetes

Write your kubernetes  deployment and service manifest.Find my kubernetes manifest here ./spring-boot-deployment.yaml .

Now generate pipeline syntax:-
For this Kubernetes continuous Deploy plugins should be installed

1. go to jenkins > your project > pipeline syntax > search for kubernetesDeploy: Deploy to kubernetes
2. choose your kubeconfig , we created kubeconfig credentials into stage 6 kubernetes Integeration with jenkins
3. generate pipeline syntax
4. write your kubernetes manifest name  into configs: 'your-k8s-manifest-name'

```groocy
stage('Deploy to k8s') {
    steps {
        script {
            kubernetesDeploy(
                configs: 'spring-boot-deployment.yaml', 
                kubeconfigId: 'kubernetes'
            )
        }
    }
}
```

## Stage: Post build action 

In post build action i used slack notification . After  build jenkins will send notification massage to slack whether your build success or failed.

1. go to jenkins > your project > pipeline syntax > search for slacksend: send slack message 
2. write your channel name and message > generate pipeline synatx .

> Note – i used custom messages for my project . I Created a function for slack notification and called the function into post build .

```groovy
post {
    always {
        sendSlackNotification()
    }
}
```

`sendSlackNotification function`

```groovy
def sendSlackNotification() {
    def buildStatus = currentBuild.currentResult
    def buildSummary = """
        Job_name: ${env.JOB_NAME}
        Build_id: ${env.BUILD_ID}
        Status: *${buildStatus}*
        Build_url: ${BUILD_URL}
        Job_url: ${JOB_URL}
    """

    if (buildStatus == "SUCCESS") {
        slackSend(channel: "#devops", token: 'slack-token', color: 'good', message: buildSummary)
    } else {
        slackSend(channel: "#devops", token: 'slack-token', color: 'danger', message: buildSummary)
    }
}
```

> Find whole pipeline here ./Jenkinsfile

## Step: 4 Projecct Output

# Final outputs of this Project

### Jenkins Output

After 86th  Build my  jenkins pipeline became successful.
![blessed](./Images/pipelineop.png)

### Sonarqube Output

![blessed](./Images/sonarqubeop.png)

### Quality Gate Status in Jenkins

This Output is the build number 86th. SonarQube Quality gate status is green and passed .   
You applied your custom quality gate like : there should be zero ( bug, Vulnerability , code smell ) and your code have greater then 0 (bugs, vulnerability , code smells) . Then your quality gate status will become failure or red. If your quality gate status beome failure , stages after quality gate will be failure.

![blessed](./Images/qualitygateop.png)

### Trivy report in AWS S3 push by jenkins

![blessed](./Images/trivy-report-s3.png)

### Trivy report

![blessed](./Images/TrivyReprt.png)

### Images in DockerHub pushed by jenkins 

![blessed](./Images/dockerhubop.png)

### kubernetes output ( deployment and service created by jenkins)

![blessed](./Images/kubernetesop.png)

### Application output deployed in k8s

![blessed](./Images/spring-boot-app-op.png)

### Slack output

![blessed](./Images/slackop.png)