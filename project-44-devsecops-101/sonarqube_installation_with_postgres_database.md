#Install SonarQube on Ubuntu 22.04
Although the process is simple, there are a few steps involved. Before you start, connect via SSH and update the server.
```sh 
sudo apt update
sudo apt upgrade
 ```
Then install some packages needed to complete the process.

```sh 
sudo apt install wget apt-transport-https gnupg2 software-properties-common unzip
 ```
Now you can continue.

#Install Java on Ubuntu 22.04
The next step is to install Java because SonarQube is created with this language. Therefore, to install Java, simply run the following command
```sh 
sudo apt install openjdk-11-jdk
 ```
At the end of the process, you can check the Java version with this command:
```sh 
java -version
 ```

#Install PostgreSQL on Ubuntu 22.04
SonarQube requires PostgreSQL as a database driver. So, you have to install it and create a new user and database.

First, install PostgreSQL with this command:
```sh 
sudo apt install postgresql postgresql-contrib
 ```
Then, enable and start it.
```sh 
sudo systemctl enable postgresql
sudo systemctl start postgresql ```
 ```
Avoid issues by checking if the service is running well.
```sh 
sudo systemctl status postgresql
 ```

With PostgreSQL installed, the next step is to access the console, to create the new user and database.
```sh 
sudo -u postgres psql
 ```
Inside the console, you can now create the user
```sh 
CREATE USER sonarqube WITH PASSWORD 'pass';
 ```
Replace pass with a stronger password. Now create the new database and make it belong to the user you just created.
```sh 
CREATE DATABASE sonarqube OWNER sonarqube;
 ```
Again, you can replace sonarqube with the database name of your choice.

Assign appropriate permissions to the new database:
```sh
GRANT ALL PRIVILEGES ON DATABASE sonarqube TO sonarqube;
 ```
You can exit now.
```sh
exit
 ```
#Install SonarQube on Ubuntu 22.04
First create a new system user for SonarQube.
```sh
sudo useradd -b /opt/sonarqube -s /bin/bash sonarqube
 ```
Then, modify some system parameters to adjust it to SonarQube
```sh
sudo nano /etc/sysctl.conf
 ```
And set these values. If they are not there, then add them at the end of the file:
```sh
vm.max_map_count=524288
fs.file-max=131072
 ```
Save the changes and close the editor. To apply the changes, run
```sh
sudo sysctl --system
 ```
Now download SonarQube
```sh
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.6.1.59531.zip
 ```
The command may change depending on the latest version of SonarQube. Check first before venturing.

Unzip the file:
```sh
unzip sonarqube-9.6.1.59531.zip
 ```
Move the folder to the /opt/ directory where the sonarqube user’s home has been set up
```sh
sudo mv sonarqube-9.6.1.59531 /opt/sonarqube
```
Make that folder belong to the created user.
```sh
sudo chown -R sonarqube:sonarqube /opt/sonarqube
```
Now it is time to configure it a little bit.

Configuring SonarQube before using it
The configuration file is /opt/sonarqube/conf/sonar.properties where all SonarQube options reside.

Edit it
```sh
sudo vi /opt/sonarqube/conf/sonar.properties
```
The first thing to do is to configure the database connection. At the end of the file you can add these lines:
```sh
sonar.jdbc.username=sonarqube
sonar.jdbc.password=pass
sonar.jdbc.url=jdbc:postgresql://localhost:5432/sonarqube
```
You have to adapt it to the values you have set.

Now with the help of your text editor, uncomment each of these lines.
```sh
sonar.web.port=9000
```

Save the changes and close the editor.

Then it is convenient to create a configuration file to handle SonarQube as a system service
```sh
sudo vi /etc/systemd/system/sonarqube.service
```
And add the following content
```sh
[Unit]
Description=SonarQube service
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/opt/sonarqube/bin/linux-x86-64/sonar.sh start
ExecStop=/opt/sonarqube/bin/linux-x86-64/sonar.sh stop
User=sonarqube
Group=sonarqube
Restart=always
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
```
Save the changes and to apply them, run
```sh
sudo systemctl daemon-reload
```
Start the service:
```sh
sudo systemctl start sonarqube.service
```
Enable it to start with the system:
```sh
sudo systemctl enable sonarqube.service
```
Verify that everything is OK:
```sh
systemctl status sonarqube.service
```


#Access to the SonarQube web interface
Now, open your web browser and access http://yourserver:9000 and you will see this screen indicating that SonarQube is running

Then log in with the default credentials admin/admin.

You will be prompted to change the password, and finally, you will see the main SonarQube screen.
