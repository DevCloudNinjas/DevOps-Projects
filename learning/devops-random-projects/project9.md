# WORKING WITH JENKINS- CI/CD PROJECT
## INTRODUCTION
In this project, the web application architecture in [project 8](./project8.md) is enhanced by adding Jenkins server, whereby a job is configured to automatically build on trigger by a webhook whenever there is a change in the tooling repository and sends the artifacts remotely to the NFS server.

The following outlines the steps I took in setting up this project:

## STEP 0: Launching Of EC2 Instance
I launched an EC2 Instance(Ubuntu server 20.04) that will be used as Jenkins Server. I connected to the server on my terminal through ssh connection.

## STEP 1: Installing And Configuring The Jenkins Server
-	Updating and upgrading the server:

`$ sudo apt update`

![](./img/project9/apt%20update.png)

`$ sudo apt upgrade`

![](./img/project9/apt%20upgrade.png)

-	Installing the Java Development Kit(JDK):`$ sudo apt install default-jdk-headless`

![](./img/project9/install%20java.png)

-	Acquiring the Jenkins key:`$ wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -`

![](./img/project9/jenkins%20key.png)

-	Adding to the source file the path to Jenkins installation:`$ sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'`

![](./img/project9/adding%20to%20source%20file.png)

-	Updating the server again:`$ sudo apt update`

![](./img/project9/apt%20update2.png)

-	Installing Jenkins: `$ sudo apt-get install jenkins`

![](./img/project9/install%20jenkins.png)

-	To ensure that Jenkins is up and running:`$ sudo systemctl status jenkins`

![](./img/project9/systemctl%20status%20jenkins.png)

-	Opening TCP port 8080 on the security group:

![](./img/project9/adding%20port%208080.png)

## STEP 2: Performing Initial Jenkins Setup
-	Entering the ubuntu server’s public IP on port 8080 on the web browser: http://54.147.210.46:8080

![](./img/project9/unlock%20jenkins.png)

-	Retrieving the password from the server:`$ sudo cat /var/lib/jenkins/secrets/initialAdminPassword`
-	Selecting **install suggested plugin**

![](./img/project9/installing%20plugins.png)

![](./img/project9/installing%20plugins%202.png)

-	After installation, I created an admin user after which I got my Jenkins server address

![](./img/project9/jenkins%20address.png)

-	Jenkins is ready to be used

![](./img/project9/jenkins%20is%20ready.png)

![](./img/project9/jenkins%20home%20page.png)

## STEP 3: Configuring Jenkins To Retrieve Source Codes From GitHub Using Webhooks

-	Enabling webhooks in my Github account which will trigger a build task, that will retrieve codes from Github and store it locally on Jenkins server. And this is done by going to the Github settings of the tooling repository and clicking on webhooks and inputing the Jenkins public Ip address as the payload URL and saving the settings:

![](./img/project9/webhooks.png)
![](./img/project9/webhooks2.png)

-	Creating a freestyle project on the Jenkins web console by clicking on **New Item**

![](./img/project9/creating%20freestyle%20project.png)

-	Copying the URL of the tooling repository in order to connect it to the freestyle project created

![](./img/project9/copying%20the%20tooling%20repo%20url.png)

-	Pasting the tooling repository URL and setting my credentials so Jenkins can access files in the repository and saving the whole configuration

![](./img/project9/creating%20freestyle%20project2.png)

![](./img/project9/setting%20the%20git%20credential.png)

-	Clicking on **build now** to ensure that the configuration works and that the build is successful.

![](./img/project9/first%20build.png)

-	To make the build to run automatically whenever a change happens in the tooling repository by the help of webhook, going back to the configuration by clicking on “Configure”
-	On the **Build Triggers** section, selecting **GitHub hook trigger for GITScm polling**

![](./img/project9/selecting%20githook.png)

-	And on the **Post-build Actions**, clicking on **Add post-build action** and selecting **Archive the artifacts** to archive all the files resulted from the build

![](./img/project9/archiving%20artifact.png)

-	Then going to the tooling repository on my Github account and making a change in the ReadMe.md file and pushing the change to the master branch
-	Going back to Jenkins web console to confirm that a new build has been triggered automatically:

![](./img/project9/second%20build.png)

![](./img/project9/second%20build2.png)

-	To locate the artifacts on the Jenkins server:`$ ls /var/lib/jenkins/jobs/tooling_github/builds/<build_number>/archive/`

![](./img/project9/artifacts%20directory.png)

## OPTIONAL STEP: Configuring Jenkins To Send Artifacts To NFS Server
- Installing **Publish Over SSH** from **Manage Jenkins > Manage plugin** option in the Jenkins web console and restart:

![](./img/project9/installing%20publish%20over%20ssh-3.png)

![](./img/project9/installing%20publish%20over%20ssh.png)

![](./img/project9/installing%20publish%20over%20ssh-2.png)

- Configuring the **publish over ssh** on the **Manage Jenkins > Configure system** settings to connect to the NFS server and setting the remote directory path to the **/mnt/opt**. Using the NFS server Private IP as the Hostname:

![](./img/project9/configuring%20publish%20over%20ssh.png)

- Enabling the **tooling_github** job to send artifacts to the NFS server by clicking on **Configure** option
- On the **Post-build Action**, selecting **Send build artifacts over ssh** and selecting the NFS Server configuration and click save:

![](./img/project9/setting%20post%20build%20action.png)

- Running the build:

![](./img/project9/third%20build.png)

- Confirming whether the artifacts are suucessfully sent to NFS server in the /mnt/opt directory:

![](./img/project9/artifacts%20achived%20to%20nfs%20server.png)
- This shows that the Jenkins server is connected successfully to the NFS server

