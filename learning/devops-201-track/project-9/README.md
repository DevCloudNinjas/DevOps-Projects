## TOOLING WEBSITE DEPLOYMENT AUTOMATION WITH CONTINUOUS INTEGRATION.
---

The Architecture of the project is shown below:

![Architecture](./Images/jenkins%20architecture.PNG)

**INSTALL AND CONFIGURE JENKINS SERVER**


**Step 1 – Install Jenkins server**

1. Create an AWS EC2 server based on Ubuntu Server 20.04 LTS and name it "Jenkins"

![jenkins server](./Images/jenkins%20server.PNG)

2. Install JDK (since Jenkins is a Java-based application)

```
sudo apt update
sudo apt install default-jdk-headless
```

3. **Install Jenkins**

```
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
    /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt-get install jenkins
```

Make sure Jenkins is up and running:

**`sudo systemctl status jenkins`**

![jenkins status](./Images/jenkins%20status.PNG)

4. By default Jenkins server uses TCP port 8080 – open it by creating a new Inbound Rule in your EC2 Security Group

![port 8080](./Images/port%2080.PNG)

5. Perform initial Jenkins setup.

From your browser access http://<Jenkins-Server-Public-IP-Address-or-Public-DNS-Name>:8080

You will be prompted to provide a default admin password

![jenkins login page](./Images/jenkins%20login%20page.PNG)


Retrieve it from your server:

**`sudo cat /var/lib/jenkins/secrets/initialAdminPassword`**

Then you will be asked which plugings to install – choose suggested plugins.

![jenkins plugins](./Images/installed%20suggested%20plugin.PNG)

Once plugins installation is done – create an admin user and you will get your Jenkins server address.

![jenkins complete](./Images/welcome%20to%20jenkins.PNG)


**The installation is completed!**



**Step 2 – Configure Jenkins to retrieve source codes from GitHub using Webhooks**

In this part, you will learn how to configure a simple Jenkins job/project (these two terms can be used interchangeably). This job will will be triggered by GitHub webhooks and will execute a ‘build’ task to retrieve codes from GitHub and store it locally on Jenkins server.

1. Enable webhooks in your GitHub repository settings


![configure webhook](./Images/configure%20jenkins%20to%20retrieve%20source%20code.PNG)

2. Go to Jenkins web console, click "New Item" and create a "Freestyle project"


![add new item](./Images/add%20new%20item.PNG)

To connect your GitHub repository, you will need to provide its URL, you can copy from the repository itself

![github code](./Images/copy%20link%20for%20code.PNG)


In configuration of your Jenkins freestyle project choose Git repository, provide there the link to your Tooling GitHub repository and credentials (user/password) so Jenkins could access files in the repository.

![source code mgt](./Images/source%20code%20mgt.PNG)


Save the configuration and let us try to run the build. For now we can only do it manually.

Click "Build Now" button, if you have configured everything correctly, the build will be successfull and you will see it under #1

![build 1](./Images/build.PNG)


You can open the build and check in "Console Output" if it has run successfully.


But this build does not produce anything and it runs only when we trigger it manually. Let us fix it.


3. Click "Configure" your job/project and add these two configurations

Configure triggering the job from GitHub webhook:

![build trigger](./Images/build%20triggers.PNG)

Configure "Post-build Actions" to archive all the files – files resulted from a build are called "artifacts".

**click on add post-build actions and click "Archive the Artifact" then save**

Now, go ahead and make some change in any file in your GitHub repository (e.g. README.MD file) and push the changes to the master branch.

You will see that a new build has been launched automatically (by webhook) and you can see its results – artifacts, saved on Jenkins server.


![after change to the master branch ](./Images/changes%20made%20to%20master%20branch.PNG)


we have now successfully configured an automated Jenkins job that receives files from GitHub by webhook trigger (this method is considered as ‘push’ because the changes are being ‘pushed’ and files transfer is initiated by GitHub). There are also other methods: trigger one job (downstreadm) from another (upstream), poll GitHub periodically and others.

By default, the artifacts are stored on Jenkins server locally, note the build_number is the value of the build created

**`ls /var/lib/jenkins/jobs/tooling_github/builds/<build_number>/archive/`**




**CONFIGURE JENKINS TO COPY FILES TO NFS SERVER VIA SSH**


**Step 3 – Configure Jenkins to copy files to NFS server via SSH**


Now we have our artifacts saved locally on Jenkins server, the next step is to copy them to our NFS server to `/mnt/apps` directory.

Jenkins is a highly extendable application and there are 1400+ plugins available. We will need a plugin that is called `"Publish Over SSH"`.

1. Install "Publish Over SSH" plugin.

On main dashboard select "Manage Jenkins" and choose "Manage Plugins" menu item.

On "Available" tab search for **"Publish Over SSH"** plugin and install it

![publish over ssh ](./Images/publish%20over%20ssh.PNG)



2. Configure the job/project to copy artifacts over to NFS server.

On main dashboard select "Manage Jenkins" and choose "Configure System" menu item.

Scroll down to Publish over SSH plugin configuration section and configure it to be able to connect to your NFS server:

* Provide a private key (content of .pem file that you use to connect to NFS server via SSH/Putty)

* Arbitrary name

* Hostname – can be `private IP address` of the NFS server

* Username – `ec2-user` (since NFS server is based on EC2 with RHEL 8)

* Remote directory – `/mnt/apps` since our Web Servers use it as a mointing point to retrieve files from the NFS server


Test the configuration and make sure the connection returns Success. Remember, that TCP port 22 on NFS server must be open to receive SSH connections.

![publish over ssh configure ](./Images/publish%20over%20ssh%20configuration.PNG)


Save the configuration, open your Jenkins job/project configuration page and add another one "Post-build Action"

![send build over ssh ](./Images/send%20build%20artifact%20over%20ssh.PNG)


Configure it to send all files probuced by the build into our previouslys define remote directory. In our case we want to copy all files and directories – so we use **.

![syntax](./Images/syntax.PNG)


Save this configuration and go ahead, change something in README.MD file in your GitHub Tooling repository.


Webhook will trigger a new job and in the "Console Output" of the job you will find something like this:

```
SSH: Transferred 25 file(s)
Finished: SUCCESS
```

To make sure that the files in /mnt/apps have been udated – connect via SSH/Putty to your NFS server and check README.MD file

```
cat /mnt/apps/README.md
```
If you see the changes you had previously made in your GitHub – the job works as expected.


If you are having issues with the build failing or been unstable, follow the steps below to correct such.

* In your NFS server change permissions for the /mnt/apps directory

```
sudo chmod 777 /mnt/apps
sudo chown nobody:nobody /mnt/apps
sudo chmod -R 777 /mnt
sudo chown -R nobody:nobody /mnt
```

![change permission](./Images/change%20permissions.PNG)


## THANK YOU!!!
