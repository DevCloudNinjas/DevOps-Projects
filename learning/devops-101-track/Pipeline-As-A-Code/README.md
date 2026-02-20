# JENKINS - PIPELINE AS A CODE (PAAC)
![jenkins](./images/jenkins-PAAC.png)
Jenkins is an open source continuous integration/continuous delivery and deployment (CI/CD) automation software DevOps tool written in the Java programming language.

Pipeline As A Code (PAAC) is jenkins way of setting up pipe automatically using a file called `Jenkinsfile`. Jenkins files defines stages in CI/CD pipeline.

We will be exploring at jenkins in two form:-
+ How to automatically create a jenkins job and
+ Scripted way of creating pipelines

# Tools Used For Entire Project
+ Jenkins
+ Sonarqube
+ Nexus
+ AWS

# Installing Jenkins On AWS EC2 Instance
+ Log in to your AWS console and launch EC2 instance (ubuntu 20.04) and also allowing port 22 and 8080 (instance type  - t2.small) for jenkins as we do in previous project and paste the following command on the userdata section while launching the instance.


      #!/bin/bash
      sudo apt update
      sudo apt install openjdk-11-jdk -y
      sudo apt install maven -y
      curl -fsSL https://pkg.jenkins.io/debian/jenkins.io.key | sudo tee \
        /usr/share/keyrings/jenkins-keyring.asc > /dev/null
      echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
        https://pkg.jenkins.io/debian binary/ | sudo tee \
        /etc/apt/sources.list.d/jenkins.list > /dev/null
      sudo apt-get update
      sudo apt-get install jenkins -y

+ Now we have successfully launch our server with jenkins installed in it. It is time to access it from the browser by taking the public ip of the instance to the port 8080

      <public ip>:8080
    ![jen](./images/jenkins-int.png)
+ We are left with unlocking the jenkins and working with it. Log in to your instance using ssh on your terminal. Change to the root directory while in the server terminal

      sudo -i
+ We can then access the password from there by pasting the command

      cat /var/lib/jenkins/secrets/initialAdminPassword
+ Then copy the password and paste it onto your Jenkins user interface for authentication

+ Install suggested Plugins from the user interface and follow the prompt provided by filling in youir details

    ![jenkin](./images/jenkins-ui.png)
+ Install jdk8 by also ssh into the instance and run

      sudo apt update
      sudo apt install openjdk-8-jdk -y
+ Go to the dashbord, navigate to Manage Jenkins > Global Tool Configuration then install openjdk8 by adding the below homepath property

      /usr/lib/jvm/java-1.8.0-openjdk-amd64

##  Now let us create a job 
+ Navigate to Manage Jenkins > Plugin Manager and add `Pipeline Utility Steps`, `Pipeline Maven Integration`then install the plugins stated.
+ Click on Create a job then add a name and select pipeline because we will be executing Pipeline As A Code and paste the below script in the pipeline script section

      pipeline {
        agent any
        stages {
          stage ('fetch code'){
            steps {
              git branch: 'paac', url: 'https://github.com/devopshydclub/vprofile-project.git'
            }
          }
          stage ('Build') {
            steps {
              sh 'mvn install'
            }
          }
          stage ('Test') {
            steps {
              sh 'mvn test'
            }
          }
        }
      }


+ Build the Job and it is a success.
  ![job](./images/build.png)

