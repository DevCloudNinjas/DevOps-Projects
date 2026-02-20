# IMPLEMENTING A CLIENT SERVER ARCHITECTURE USING MYSQL DATABASE MANAGEMENT SYSTEM (DBMS)

## INTRODUCTION:
  Client-server refers to architecture in which two or more computers are connected together over a network to send and receive requests between one another. In this project, two computers(severs) were made to connect to each other using MySQL which is a Database Management System. 
The following steps were taken in setting up a client-server architecture using MySQL:

## STEP 1:	SETTING UP TWO VIRTUAL SERVERS IN THE CLOUD
In order to demonstrate a basic client-server architecture using MySQL, two virtual servers(ubuntu 20.04 LTS) were launched in AWS cloud and are designated as;
- **Server A** – ‘mysql-server’
- **Server B** – ‘mysql-client’

## STEP 2:	CONFIGURING THE TWO SERVERS
Updating and upgrading the two servers with the command:
`$ sudo apt update`
`$ sudo apt upgrade`
- **Server A:**
![](./img/project5/updating%20and%20upgrading%20%20server%20A.png)
- **Server B:**
![](./img/project5/updating%20and%20upgrading%20server%20B.png)

## STEP 3:	INSTALLING MYSQL-SERVER IN SERVER A
-	Installing mysql-server: `$ sudo apt install mysql-server`
![](./img/project5/installing%20mysql-server%20on%20server%20A.png)

## STEP 4: 	CONFIGURING MYSQL-SERVER IN SERVER A
For the remote host(server B) to be able to connect to server B, mysql-server is configured to allow connections from server B:
-	Editing the mysqld.cnf file:` $ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf`
-	Changing the value of bind-address from ‘127.0.0.1’ to ‘0.0.0.0’:
![](./img/project5/configuring%20the%20mysql-server.png)
-	Ensuring that mysql is listening to ‘0.0.0.0’ on port 3306:`$ sudo netstat -plunt | grep mysqld`
![](./img/project5/ensuring%20that%20mysql%20is%20listening%20to%200.0.0.0.png)
-	Opening up that port on the firewall to allow traffic through:`$ sudo ufw allow mysql`

## STEP 5: 	CREATING AND GRANTING FULL ACCESS TO A MYSQL USER IN SERVER A
To be able to connect to server A from server B a remote user is created and granted privileges:
-	Activating mysql shell: `$ sudo mysql`
-	Creating a database: `mysql>	CREATE DATABASE todoapp;`
-	Creating a remote user with server B’s ip_address: `mysql>	CREATE USER 'remote_somex'@'3.88.230.169' IDENTIFIED BY 'password12345';`
-	Granting the remote user full access to the database:`mysql>  GRANT ALL PRIVILEGES ON todoapp.* TO 'remote_somex'@'3.88.230.169';`
-	Lastly, flushing the privileges so that MySQL will begin to use them: `mysql>	 FLUSH PRIVILEGES;`
-	Exit: `mysql>	 exit`
![](./img/project5/creating%20a%20mysql%20user%20in%20server-A.png)

## STEP 6:	CONFIGURING THE SECURITY GROUP OF SERVER A
-	Adding a rule to the security group of server A to be able to listen to port 3306 because MySQL uses TCP port 3306 by default, and for extra security customizing it to allow access only to the ip address of server B:
![](./img/project5/configuring%20the%20security%20group%20of%20server-A.png)

## STEP 7:	INSTALLING MYSQL-CLIENT IN SERVER B AND CONNECTING TO SERVER A
-	Installing MySQL client utilities: `$ sudo apt install mysql-client`
![](./img/project5/installing%20mysql-client%20on%20server%20B.png)
-	Lastly, connecting to the database server(server A) with its ip address: `$ mysql -u remote_somex -h 3.83.11.153 –p`
![](./img/project5/connecting%20to%20mysql%20server%20from%20the%20client%20server.png)
-	**Connection established!**

