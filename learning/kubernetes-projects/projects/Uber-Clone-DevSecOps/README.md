# Uber Clone DevSecOps CI/CD Kubernetes Project

![](https://miro.medium.com/v2/resize:fit:736/0*xJc4sgDsMZqdfPyZ.png)

# **Introduction :-**

In the fast-paced world of app development, the need for a seamless and secure Continuous Integration/Continuous Deployment (CI/CD) pipeline cannot be overstated. For businesses looking to replicate the success of Uber, it’s crucial to implement a DevSecOps approach that ensures both speed and security throughout the software development lifecycle. In this blog post, we’ll explore the key components of a DevSecOps CI/CD pipeline for an Uber clone, emphasizing the importance of integrating security into every stage of the development process.

**Github Repo** :- [uber-clone](https://github.com/SushantOps/uber-clone.git)

## **STEP 1: Launch an Ubuntu instance (T2.large) :-**

Launch an AWS T2 Large Instance. Use the image as Ubuntu. You can create a new key pair or use an existing one. Enable HTTP and HTTPS settings in the Security Group and open all ports .

![](https://miro.medium.com/v2/resize:fit:736/0*eXj5Sn_hPKuI2j4V)

## **STEP 2: Create IAM role :-**

Search for IAM in the search bar of AWS and click on roles

![](https://miro.medium.com/v2/resize:fit:736/0*PoZtjfWGGkd1O2oY.png)

![](https://miro.medium.com/v2/resize:fit:736/0*nIywO8dCvfYYqWbW.png)

Now Attach this role to Ec2 instance that we created earlier, so we can provision cluster from that instance.

Go to EC2 Dashboard and select the instance.

Click on Actions → Security → Modify IAM role.

Select the Role that created earlier and click on Update IAM role.

![](https://miro.medium.com/v2/resize:fit:736/0*ph05Dw_YwIsr4CPV.png)

Connect the instance to Mobaxtreme or Putty

## **STEP 3: Installations of Packages :-**

create shell script in Ubuntu ec2 instance

```bash
sudo su   #run from inside root
vi script1.sh
```

Enter this script into it  
This script installs Jenkins, Docker , Kubectl, Terraform, AWS Cli,Sonarqube

```bash
#!/bin/bash
sudo apt update -y
wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc
echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list
sudo apt update -y
sudo apt install temurin-17-jdk -y
/usr/bin/java --version
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update -y
sudo apt-get install jenkins -y
sudo systemctl start jenkins
#install docker
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg -y
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo usermod -aG docker ubuntu
newgrp docker
```

Now provide executable permissions to shell script

```bash
chmod 777 script1.sh
sh script1.sh
```

Let’s Run the second script

```bash
vi script2.sh
```

Add this script

```bash
#!/bin/bash
# install trivy
sudo apt-get install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy -y
#install terraform
sudo apt install wget -y
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
#install Kubectl on Jenkins
sudo apt update
sudo apt install curl -y
curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
#install Aws cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt-get install unzip -y
unzip awscliv2.zip
sudo ./aws/install
```

Now provide executable permissions to shell script

```bash
chmod 777 script2.sh
sh script2.sh
```

Now check the versions of packages

```bash
docker --version
trivy --version
aws --version
terraform --version
kubectl version
```

![](https://miro.medium.com/v2/resize:fit:736/0*-Lt_XjTgHgidBd0t)

Provide executable permissions

```bash
sudo chmod 777 /var/run/docker.sock
docker run -d --name sonar -p 9000:9000 sonarqube:lts-community
```

## **STEP 4: Connect to Jenkins and Sonarqube :-**

Now copy the public IP address of ec2 and paste it into the browser

```bash
<Ec2-ip:8080> #you will Jenkins login page
```

![](https://miro.medium.com/v2/resize:fit:736/0*6GvmvuP5IoyPXGG3)

Connect your Instance to Putty or Mobaxtreme and provide the below command for the Administrator password

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Now you see Jenkins Dashboard

![](https://miro.medium.com/v2/resize:fit:736/0*Jg-5zIDUh5gHuRDX)

Now Copy the public IP again and paste it into a new tab in the browser with 9000

```bash
<ec2-ip:9000>  #runs sonar container
```

![](https://miro.medium.com/v2/resize:fit:736/0*jK69OFfd_VluUY7I.png)

Enter username and password, click on login and change password

```bash
username admin
password admin
```

Update New password, This is Sonar Dashboard.

![](https://miro.medium.com/v2/resize:fit:736/0*z0gUrkNWFjHwmlaG.png)

## **STEP 5: Terraform plugin install and EKS provision :-**

Now go to Jenkins and add a terraform plugin to provision the AWS EKS using the Pipeline Job.

Go to Jenkins dashboard –&gt; Manage Jenkins –&gt; Plugins

Available Plugins, Search for Terraform and install it.

![](https://miro.medium.com/v2/resize:fit:736/0*NKbH4PhPoA2t-IXz)

Go to Mobaxtream and use the below command

let’s find the path to our Terraform (we will use it in the tools section of Terraform)

```bash
which terraform
```

![](https://miro.medium.com/v2/resize:fit:706/0*ZfU3jF_KlLnFRAew)

Now come back to Manage Jenkins –&gt; Tools

Add the terraform in Tools

![](https://miro.medium.com/v2/resize:fit:736/0*ht-PwEdarZMrXODe)

Apply and save.

CHANGE YOUR S3 BUCKET NAME IN THE [BACKEND.TF](https://github.com/SushantOps/uber-clone/blob/main/EKS_TERRAFORM/backend.tf)

Now create a new job for the EKS provision

![](https://miro.medium.com/v2/resize:fit:736/0*7FzwigThYCAmwYO_)

I want to do this with build parameters to apply and destroy while building only.

you have to add this inside job like the below image

![](https://miro.medium.com/v2/resize:fit:736/0*5UqtfjHDFZVjW5WH)

Let’s add a pipeline

```bash
pipeline{
    agent any
    stages {
        stage('Checkout from Git'){
            steps{
                git branch: 'main', url: 'https://github.com/SushantOps/uber-clone.git'
            }
        }
        stage('Terraform version'){
             steps{
                 sh 'terraform --version'
             }
        }
        stage('Terraform init'){
             steps{
                 dir('EKS_TERRAFORM') {
                      sh 'terraform init'
                   }
             }
        }
        stage('Terraform validate'){
             steps{
                 dir('EKS_TERRAFORM') {
                      sh 'terraform validate'
                   }
             }
        }
        stage('Terraform plan'){
             steps{
                 dir('EKS_TERRAFORM') {
                      sh 'terraform plan'
                   }
             }
        }
        stage('Terraform apply/destroy'){
             steps{
                 dir('EKS_TERRAFORM') {
                      sh 'terraform ${action} --auto-approve'
                   }
             }
        }
    }
}
```

Let’s apply and save and Build with parameters and select action as apply

![](https://miro.medium.com/v2/resize:fit:736/0*O6KWAliZDV2G6lUs)

Stage view it will take max 10mins to provision

![](https://miro.medium.com/v2/resize:fit:736/0*t7DhLpgdQKM7-JVj)

Check in Your Aws console whether it created EKS or not.

![](https://miro.medium.com/v2/resize:fit:736/0*iMaJxL4rezGoQQWU)

Ec2 instance is created for the Node group

![](https://miro.medium.com/v2/resize:fit:736/0*pYjPKkJVgoe1yDDI)

## **STEP 6: Plugins installation & setup (Java, Sonar, Nodejs, owasp, Docker)**

Go to Jenkins dashboard

Manage Jenkins –&gt; Plugins –&gt; Available Plugins

Search for the Below Plugins

`Eclipse Temurin installer`

`Sonarqube Scanner`

`NodeJs`

`Owasp Dependency-Check`

`Docker`

`Docker Commons`

`Docker Pipeline`

`Docker API`

`Docker-build-step`

![](https://miro.medium.com/v2/resize:fit:736/0*-06BuX1Y9bQQBDEJ)

![](https://miro.medium.com/v2/resize:fit:736/0*NNzvqaRQDgmbl8ay)

## **STEP 7: Configure in Global Tool Configuration :-**

Goto Manage Jenkins → Tools → Install JDK(17) and NodeJs(16)→ Click on Apply and Save

![](https://miro.medium.com/v2/resize:fit:736/0*vzZRbUCSN0IMqIFM)

![](https://miro.medium.com/v2/resize:fit:736/0*oFNNs10rbEwhYSgQ)

For Sonarqube use the latest version

![](https://miro.medium.com/v2/resize:fit:736/0*K-J3jqgYbvkB3Bja)

For Owasp use the 6.5.1 version

![](https://miro.medium.com/v2/resize:fit:736/0*qo71Ig8i417eQ3r8)

Use the latest version of Docker

![](https://miro.medium.com/v2/resize:fit:736/0*_31rYDmTfCmIdvtF)

Click apply and save.

## **STEP 8: Configure Sonar Server in Manage Jenkins :-**

Grab the Public IP Address of your EC2 Instance, Sonarqube works on Port 9000, so &lt;Public IP&gt;:9000. Goto your Sonarqube Server. Click on Administration → Security → Users → Click on Tokens and Update Token → Give it a name → and click on Generate Token

![](https://miro.medium.com/v2/resize:fit:736/0*WF7CU5JxPkv9I5Mf)

click on update Token

![](https://miro.medium.com/v2/resize:fit:736/0*s5KZmD682CpU9BCX)

Create a token with a name and generate

![](https://miro.medium.com/v2/resize:fit:736/0*wmo0v6TZas5pxL35)

copy Token , Goto Jenkins Dashboard → Manage Jenkins → Credentials → Add Secret Text. It should look like this

![](https://miro.medium.com/v2/resize:fit:736/0*PUpRah8c3lig8DvQ)

You will this page once you click on create

![](https://miro.medium.com/v2/resize:fit:736/0*fRh-e1-st3N691jq)

Now, go to Dashboard → Manage Jenkins → System and Add like the below image.

![](https://miro.medium.com/v2/resize:fit:736/0*z_ZN_VZuvk88whIx)

Click on Apply and Save

The Configure System option is used in Jenkins to configure different server

Global Tool Configuration is used to configure different tools that we install using Plugins

We will install a sonar scanner in the tools.

![](https://miro.medium.com/v2/resize:fit:736/0*8ZsUcXK5cMDk2IfZ)

In the Sonarqube Dashboard add a quality gate also

Administration → Configuration →Webhooks

![](https://miro.medium.com/v2/resize:fit:736/0*vNVsJ4myibOhj-Q2.png)

Add details

```bash
#in url section of quality gate
<http://jenkins-public-ip:8090>/sonarqube-webhook/
```

![](https://miro.medium.com/v2/resize:fit:736/0*ISW6D59PGyFGI17T.png)

Now add Docker credentials to the Jenkins to log in and push the image

Manage Jenkins –&gt; Credentials –&gt; global –&gt; add credential

Add DockerHub Username and Password under Global Credentials and create.

![](https://miro.medium.com/v2/resize:fit:736/0*6qyutwoP8QL20ZEL)

## **STEP 09: RUN an Pipeline :-**

Add this code to Pipeline

```groovy
pipeline{
    agent any
    tools{
        jdk 'jdk17'
        nodejs 'node16'
    }
    environment {
        SCANNER_HOME=tool 'sonar-scanner'
    }
    stages {
        stage('clean workspace'){
            steps{
                cleanWs()
            }
        }
        stage('Checkout from Git'){
            steps{
                git branch: 'main', url: 'https://github.com/SushantOps/uber-clone.git'
            }
        }
        stage("Sonarqube Analysis "){
            steps{
                withSonarQubeEnv('sonar-server') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=Uber \
                    -Dsonar.projectKey=Uber'''
                }
            }
        }
        stage("quality gate"){
           steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token'
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                sh "npm install"
            }
        }
        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
         stage('TRIVY FS SCAN') {
            steps {
                sh "trivy fs . > trivyfs.txt"
            }
        }
        stage("Docker Build & Push"){
            steps{
                script{
                   withDockerRegistry(credentialsId: 'docker', toolName: 'docker'){
                       sh "docker build -t uber ."
                       sh "docker tag uber sushantkapare1717/uber:latest "
                       sh "docker push sushantkapare1717/uber:latest "
                    }
                }
            }
        }
        stage("TRIVY"){
            steps{
                sh "trivy image sushantkapare1717/uber:latest > trivyimage.txt"
            }
        }
        stage("deploy_docker"){
            steps{
                sh "docker run -d --name uber -p 3000:3000 sushantkapare1717/uber:latest"
            }
        }
    }
}
```

Click on Apply and save. amd Build now,

![](https://miro.medium.com/v2/resize:fit:736/0*lJs6gEQCa4wJJtxU)

To see the report, you can go to Sonarqube Server and go to Projects.

![](https://miro.medium.com/v2/resize:fit:736/0*Wmvx71ihe9tpTfTU)

You can see the report has been generated and the status shows as passed. You can see that there are 1.2k lines it scanned. To see a detailed report, you can go to issues.

OWASP, You will see that in status, a graph will also be generated and Vulnerabilities.

![](https://miro.medium.com/v2/resize:fit:736/0*pywfS4ydDuIMCdrN)

When you log in to Dockerhub, you will see a new image is created

![](https://miro.medium.com/v2/resize:fit:736/1*zdr0TW5f35gUsBdb_65YSQ.png)

## **STEP 10: Kubernetes Deployment**

Go to Putty of your Jenkins instance SSH and enter the below command

```bash
aws eks update-kubeconfig --name <CLUSTER NAME> --region <CLUSTER REGION>
aws eks update-kubeconfig --name EKS_CLOUD --region ap-south-1
```

![](https://miro.medium.com/v2/resize:fit:736/0*2tRX5CIuxui2ur0A)

Let’s see the nodes

```bash
kubectl get nodes
```

![](https://miro.medium.com/v2/resize:fit:736/0*a12UrkVgkprNgIUW)

Copy the config file to Jenkins master or the local file manager and save it

copy it and save it in documents or another folder save it as secret-file.txt

Note: create a secret-file.txt in your file explorer save the config in it and use this at the kubernetes credential section.

Install Kubernetes Plugin, Once it’s installed successfully

![](https://miro.medium.com/v2/resize:fit:736/0*yqwlaK36tju2sT1m)

goto manage Jenkins –&gt; manage credentials –&gt; Click on Jenkins global –&gt; add credentials

![](https://miro.medium.com/v2/resize:fit:736/0*zpHiGNpxLV_01U2m)

final step to deploy on the Kubernetes cluster

```groovy
stage('Deploy to kubernetes'){
            steps{
                script{
                    dir('K8S') {
                        withKubeConfig(caCertificate: '', clusterName: '', contextName: '', credentialsId: 'k8s', namespace: '', restrictKubeConfigAccess: false, serverUrl: '') {
                                sh 'kubectl apply -f deployment.yml'
                                sh 'kubectl apply -f service.yml'
                        }
                    }
                }
            }
        }
```

You will see output like this,

![](https://miro.medium.com/v2/resize:fit:736/1*zNMT9axqs6YIYzXyRt22JA.png)

## **STEP 11: Termination Process :-**

Now Go to Jenkins Dashboard and click on Terraform-Eks job

And build with parameters and destroy action

It will delete the EKS cluster that provisioned

![](https://miro.medium.com/v2/resize:fit:736/0*_sahkDUaJWMl00zM)

After 10 minutes cluster will delete and wait for it. Don’t remove ec2 instance till that time.

![](https://miro.medium.com/v2/resize:fit:736/0*g1qVCP7nfwhBFEyB)

**Cluster deleted**

![](https://miro.medium.com/v2/0*rAIsBEOSHwtnmRo2)

**Delete the Ec2 instance.**

### If you like this article, please share with others. ❤️
