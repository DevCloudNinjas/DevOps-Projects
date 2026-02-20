# IMPLEMENTATION OF WEB APPLICATION ARCHITECTURE WITH A SINGLE DATABASE AND NFS SERVER
## INTRODUCTION
In this project, I implemented a DevOps tooling website solution which makes access to DevOps tools with the following components: 
1.	**Infrastructure:** AWS
2.	**3 Linux Webservers:** Red Hat Enterprise Linux 8 that will serve the DevOps tooling weebsite  
3.	**A Database Server:** Ubuntu 20.04 for reads and write 
4.	**A Storage Server:** Red Hat Enterprise Linux 8 that will serve as NFS Server for storing shared files that the 3 Web Servers will use
5.	**Programming Language:** PHP
6.	**Code Repository:** GitHub

The following are the steps I took to set up this 3-tire Web Application Architecture with a single database and an NFS server as a shared file storage:

## Step 0: Preparing The Servers To Be Used
I launched 4 linux EC2 instances from AWS which are Red Hat Enterprise Linux 8, one is used as an NFS sever while the remaining 3 is used as webservers which will be connected to the NFS server to make it stateless.

## Step 1:  Setting Up The NFS Server
After launching the EC2 instances, I created 3 volumes from the AWS EBS volume tab, 5G each and attached them to the EC2 instance that will be used as the NFS server.

**creating the volume*
![](./img/project7/1-creating%20EBS%20volumes.png)

**Attaching the 3 volumes to the EC2 Instance for NFS server**
![](./img/project7/attaching%20volume%20to%20NFS%20server.png)
![](./img/project7/attaching%20volume%20to%20NFS%20server-2.png)
![](./img/project7/attaching%20volume%20tp%20NFS%20server-3.png)

## Step 2: Creating And Mounting Logical Volumes On The EC2 Instance For The NFS Server
I connected to the EC2 instance with mobaxterm via ssh connection and ran the following commands inorder to create a logical volume:
1.	To confirm if the 3 disks are really attached to the instance: `$ lsblk`
2.	Partitioning the 3 disks with gdisk utility:
-	For **xvdf** disk: `$ sudo gdisk /dev/xvdf`
-	Entering the **p** key to confirm that there are no partitions available on the disk
-	Entering the key **n** to create new partition and selecting the default settings by hitting enter
-	The partition type I selected is linux file system by entering its HEX code **8300**
-	Entering the **p** key to confirm the partition is created
-	Entering the **w** key to write the partition and confirming with **y** key
![](./img/project7/2-creating%20partition%20on%20xvdf%20drive.png)
![](./img/project7/3-creating%20partition%20on%20xvdf%20drive-2.png)

-	For **xvdg** disk: `$ sudo gdisk /dev/xvdf`
-	Entering the **p** key to confirm that there are no partitions available on the disk
-	Entering the key **n** to create new partition and selecting the default settings by hitting enter
-	The partition type I selected is linux file system by entering its HEX code **8300**
-	Entering the **p** key to confirm the partition is created
-	Entering the **w** key to write the partition and confirming with **y** key
![](./img/project7/4-creating%20partition%20on%20xvdg%20drive.png)
![](./img/project7/5-creating%20partition%20on%20xvdg%20drive-2.png)

-	For **xvdh** disk: `$ sudo gdisk /dev/xvdf`
-	Entering the **p** key to confirm that there are no partitions available on the disk
-	Entering the key **n** to create new partition and selecting the default settings by hitting enter
-	The partition type I selected is linux file system by entering its HEX code **8300**
-	Entering the **p** key to confirm the partition is created
-	Entering the **w** key to write the partition and confirming with **y** key
![](./img/project7/6-creating%20partition%20on%20xvdh%20drive.png)

3.	Confirming that the partitions are successfully created: `$ lsblk`
![](./img/project7/7-confirming%20the%20partitions%20created.png)

4.	Installing lvm2 utility: `$ sudo yum install lvm2`
![](./img/project7/8-installing%20lvm2.png)
![](./img/project7/9-installing%20lvm2-2.png)

5.	To check for available partition: `$ sudo lvmdiskscan`

![](./img/project7/10-to%20check%20for%20available%20partitions.png)

6.	Creating a physical volume from the partitions: `$ sudo pvcreate /dev/xvdf1 /dev/xvdg1 /dev/xvdh1`
![](./img/project7/11-creating%20physical%20volume.png)

7.	To confirm that the physical volume is created `$ sudo pvs`
![](./img/project7/12-to%20verify%20that%20pv%20is%20created.png)

8.	Creating a volume group called ‘filedata-vg’: `$ sudo vgcreate filedata-vg  /dev/xvdf1 /dev/xvdg1 /dev/xvdh1`
![](./img/project7/13-creating%20vg.png)

9.	To confirm that the volume group is created: `$ sudo vgs`
![](./img/project7/14-to%20verify%20that%20vg%20is%20created.png)

10.	Creating 3 logical volumes ‘lv-apps’, ‘lv-logs’ and ‘lv-opt’ from the volume group and allocating 4.9G to each: 
-	`$ sudo lvcreate –n lv-opt –L 4.9G filedata-vg`
-	`$ sudo lvcreate –n lv-apps –L 4.9G filedata-vg`
-	`$ sudo lvcreate –n lv-logs –L 4.9G filedata-vg`
![](./img/project7/15-creating%20lv.png)

11.	To verify that logical volume is created successfully: `$ sudo lvs`
![](./img/project7/16-verify%20that%20lv%20is%20created.png)

12.	To verify the whole setup: `$ sudo vgdisplay -v`
![](./img/project7/17-verify%20the%20whole%20setup.png)
![](./img/project7/18-verify%20the%20whole%20setup-2.png)
![](./img/project7/19-verify%20the%20whole%20setup-3.png)
![](./img/project7/20-verify%20the%20whole%20setup-4.png)

13.	Formatting the logical volumes created with xfs filesystem:
-	`$ sudo mkfs –t xfs /dev/filedata-vg/lv-opt`
-	`$ sudo mkfs –t xfs /dev/filedata-vg/lv-apps`
-	`$ sudo mkfs –t xfs /dev/filedata-vg/lv-logs`

![](./img/project7/21-formatting%20the%20disks.png)

14.	Creating a directory where the 3 logical volumes will be mounted in */mnt* directory:
-	`$ sudo mkdir /mnt/opt`
-	`$ sudo mkdir /mnt/apps`
-	`$ sudo mkdir /mnt/logs`

![](./img/project7/22-creating%20opt%2Clogs%2Capps%20directory.png)

15.	Mounting the 3 logical volumes:
-	`$ sudo mount /dev/filedata-vg/lv-logs /mnt/logs`	
-	`$ sudo mount /dev/filedata-vg/lv-apps /mnt/apps`
-	`$ sudo mount /dev/filedata-vg/lv-opt /mnt/opt`

![](./img/project7/23-mounting%20the%20lv.png)

16.	To verify the mounts:`$ df -h`
![](./img/project7/24-verify%20the%20mount.png)

17.	To get information on the UUID of the disk mounted: `$ sudo blkid`
![](./img/project7/25-blkid.png)

18.	Configuring the fstab file to enable the mounts to persist on boot: `$ sudo vi /etc/fstab`
![](./img/project7/26-updating%20the%20fstab.png)

19.	Testing the configuration and reloading the daemon:
-	`$ sudo mount -a`
-	`$ sudo systemctl daemon-reload`

![](./img/project7/27-testing%20the%20configuration%20and%20reloading%20daemon.png)

## Step 2: Configuring The NFS Server
1.	Updating the server: `$ sudo yum update`
![](./img/project7/28-updating%20the%20NFS%20server.png)
![](./img/project7/29-updating%20the%20NFS%20server-2.png)

2.	Installing NFS server utilities:`$ sudo yum install nfs-utils -y `
![](./img/project7/30-installing%20nfs%20server.png)
![](./img/project7/31-installing%20nfs%20server-2.png)

3.  Starting and enabling the nfs server service:
-	`$ sudo systemctl start nfs-server.service`
-	`$ sudo systemctl enable nfs-server.service`
![](./img/project7/32-starting%20nfs%20server%20and%20enabling%20it.png)

4.	To check the status of the nfs service: `$ sudo systemctl status nfs-server.service`
![](./img/project7/33-checking%20the%20status%20of%20nfs%20server.png)

5.	Changing the ownership of the 3 directories where disks are mounted:
-	`$ sudo chown -R nobody: /mnt/apps`
-	`$ sudo chown -R nobody: /mnt/logs`
-	`$ sudo chown -R nobody: /mnt/opt`

![](./img/project7/34-chown.png)

6.	Changing the permission of the 3 directories where disks are mounted:
-	`$ sudo chmod -R 777 /mnt/apps`
-	`$ sudo chmod -R 777 /mnt/logs`
-	`$ sudo chmod –R 777 /mnt/opt`
-	Restarting the nfs service: `$ sudo systemctl restart nfs-server.service`

![](./img/project7/35-chmod%20and%20restart.png)

7.	Configuring access to NFS server for clients within the same subnet(the subnet cidr of my webservers is 172.31.80.0/20):
-	Opening the NFS export file `$ sudo vi /etc/exports`
-	Entering the following configuration:

```
	/mnt/apps 172.31.80.0/20(rw,sync,no_all_squash,no_root_squash)
	/mnt/logs 172.31.80.0/20(rw,sync,no_all_squash,no_root_squash)
	/mnt/opt 172.31.80.0/20(rw,sync,no_all_squash,no_root_squash)
```
![](./img/project7/36-export%20config.png)

-	Exporting the configuration to make the mounts directory available for NFS clients to mount: `$ sudo exportfs -arv`

![](./img/project7/37-export%20mounts.png)

-	Checking the port used by NFS: `$ rpcinfo –p | grep nfs`

![](./img/project7/38-to%20check%20ports%20used%20by%20nfs.png)

-	Opening the port in the security group of the NFS server including TCP 111, UDP 111, UDP 2049:

![](./img/project7/39-configuring%20security%20group%20for%20the%20nfs%20server.png)

## Step 3: Setting Up And Configuring The Database Server
I launched another EC2 instance(Ubuntu 20.04) from AWS to be used as database server. Then I connected to it from my terminal via ssh connection and performed the following commands in setting up mysql database:
-	Updating and upgrading the server:
	
`$ sudo apt update`

`$ sudo apt upgrade`
![](./img/project7/62-updating%20database%20server.png)

![](./img/project7/63-upgrading%20database%20server.png)
![](./img/project7/64-upgrading%20database%20server-2.png)

-	Installing mysql server: `$ sudo apt install mysql-server`

![](./img/project7/67-installing%20mysql-server.png)
![](./img/project7/68-installing%20mysql-server-2.png)

-	Creating a database called ‘tooling’ and creating a remote user called ’webaccess’ with the subnet cidr of the webservers as its IP address and granting the user permission  to do anything only from the webservers subnet cidr:
```
mysql> CREATE DATABASE tooling;
mysql> CREATE USER ‘webaccess’@’172.31.80.0/20’ IDENTIFIED BY ‘password1234’;
mysql> GRANT ALL PRIVILEGES ON ‘tooling’.* TO ‘webaccess’@’172.31.80.0/20’;
```
![](./img/project7/69-creating%20a%20mysql%20user.png)

-	Adding a rule in the database security group to listen to TCP port 3306 and only allow access from webservers’ subnet cidr:

![](./img/project7/75-adding%203306%20port%20in%20database.png)

-	Editing the mysqld.cnf file `$ sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf` and changing the bind-address value from ‘127.0.0.1’ to ‘0.0.0.0’:

![](./img/project7/70-configuring%20mysqld.conf.png)

-	Restarting the mysql service:`$ sudo systemctl restart mysql`

![](./img/project7/71-restarting%20mysql%20service.png)

## Step 4: Configuring The Webservers
I connected to the remaining 3 EC2 instances launched, which is to be used as webservers, via ssh connection on my terminal and performed the following commands inorder to configure the webservers:
-	Updating the 3 servers: `$ sudo yum update`

**for webserver A**
![](./img/project7/updating%20the%20web%20serverA.png)
![](./img/project7/updating%20the%20web%20serverA-2.png)

**for webserver B**
![](./img/project7/updating%20the%20web%20serverB.png)
![](./img/project7/updating%20the%20web%20serverB-2.png)

**for webserver C**
![](./img/project7/updating%20the%20web%20serverC.png)
![](./img/project7/updating%20the%20web%20serverC-2.png)

-	Installing nfs clients on the 3 severs:`$ sudo yum install nfs-utils nfs4-acl-tools –y`

**For webserver A**
![](./img/project7/installing%20nfs%20client%20on%20web%20serverA.png)
![](./img/project7/installing%20nfs%20client%20on%20web%20serverA-2.png)

**For webserver B**
![](./img/project7/installing%20nfs%20client%20on%20web%20serverB.png)
![](./img/project7/installing%20nfs%20client%20on%20web%20serverB-2.png)

**For webserver C**
![](./img/project7/installing%20nfs%20client%20on%20web%20serverC.png)
![](./img/project7/installing%20nfs%20client%20on%20web%20serverC-2.png)

-	Creating the directory where to serve our devops tooling web content: `$ sudo mkdir /var/www` and Targeting the NFS exports for apps with the NFS server’s private IP address and mounting it on /var/www directory:
	
` $ sudo mount -t nfs -o rw,nosuid 172.31.84.250:/mnt/apps /var/www`

**For webserver A**
![](./img/project7/40-mounting%20the%20nfs%20server%20export.png)

**For webserver B**
![](./img/project7/mounting%20the%20nfs%20server%20export%20for%20webserverB.png)

**For webserver C**
![](./img/project7/mounting%20the%20nfs%20server%20export%20for%20webserver%20C.png)

-	Verifying that NFS is successfully mounted:`$ df -h`
![](./img/project7/41-to%20verify%20that%20nfs%20export%20is%20mounted.png)

-	Editing the fstab configuration to ensure that the mount persist:`$ sudo vi /etc/fstab`
-	And entering the following configuration:
`172.31.84.250:/mnt/apps /var/www nfs defaults 0 0`

**For webserver A**
![](./img/project7/42-updating%20the%20fstab.png)

**For webserver B**
![](./img/project7/updating%20the%20fstab%20for%20webserverB.png)

**For webserver C**
![](./img/project7/updating%20the%20fstab%20for%20the%20webserver%20C.png)

-	Installing Apache:`$ sudo yum install httpd -y`

**For webserver A**
![](./img/project7/43-installing%20apache.png)
![](./img/project7/44-installing%20apache-2.png)

**For webserver B**
![](./img/project7/installing%20apache%20for%20the%20webserverB.png)
![](./img/project7/installing%20apache%20for%20the%20webserverB-2.png)

**For webserver C**
![](./img/project7/installing%20apache%20for%20webserverC.png)
![](./img/project7/installing%20apache%20for%20webserverC-2.png)

-	Installing EPEL from Fedora repository: `$ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm`

**For webserver A**

![](./img/project7/45-installing%20from%20fedora%20repo.png)

**For webserver B**

![](./img/project7/installing%20from%20fedora%20repo%20on%20webserverB.png)

**For webserver C**

![](./img/project7/installing%20from%20fedora%20repo%20on%20webserverC.png)

-	Installing from remi repo: `$ sudo dnf install dnf-utils http://rpms.remirepo.net/enterprise/remi-release-8.rpm`

**For webserver A**
![](./img/project7/46-installing%20from%20remi%20repo.png)

**For webserver B**
![](./img/project7/installing%20from%20remi%20repo%20on%20webserverB.png)

**For webserver C**
![](./img/project7/installing%20from%20remi%20repo%20on%20webserverC.png)

-	To enable the installation of a newer PHP release: 
	
  ```
  $ sudo dnf module reset php
	$ sudo dnf module enable php:remi-7.4
  ```
  
**For webserver A**
![](./img/project7/47-module%20reset.png)

![](./img/project7/48-module%20enable%20php.png)

**For webserver B**
![](./img/project7/module%20reset%20on%20webserverB.png)

![](./img/project7/module%20enable%20php%20on%20webserverB.png)

**For webserver C**
![](./img/project7/module%20reset%20on%20webserverC.png)

![](./img/project7/module%20enable%20php%20on%20webserverC.png)
-	installing PHP and most of its module:`$ sudo dnf install php php-opcache php-gd php-curl php-mysqlnd`

**For webserver A**
![](./img/project7/49-installing%20php%20and%20its%20dependencies.png)
![](./img/project7/50-installing%20php%20and%20its%20dependencies-2.png)

**For webserver B**
![](./img/project7/installing%20php%20and%20its%20dependecies%20on%20wbsB.png)
![](./img/project7/installing%20php%20and%20its%20dependencies%20on%20wbsB-2.png)

**For webserver C**
![](./img/project7/installing%20php%20and%20its%20dependencies%20on%20wbsC.png)
![](./img/project7/installing%20php%20and%20its%20dependencies%20on%20wbsC-2.png)

-	Starting the FPM service and enabling it to automatically start on boot: 

 `$ sudo systemctl start php-fpm`
 
 `$ sudo systemctl enable php-fpm`
 
 **For webserver A**
 ![](./img/project7/51-start%20and%20enable%20php%20service.png)
 
 **For webserver B**
 ![](./img/project7/start%20and%20enable%20php-fpm%20on%20wbsB.png)
 
 **For webserver C**
  ![](./img/project7/start%20and%20enable%20php-fpm%20on%20wbsC.png)
  
-	Executing the Setsebool command:`$ sudo setsebool -P httpd_execmem 1`

 **For webserver A**
 
 ![](./img/project7/52-setsebool.png)
 
 **For webserver B**
 
 ![](./img/project7/setsebool%20on%20wbsB.png)
 
 **For webserver C**

![](./img/project7/setsebool%20for%20wbsC.png)

-	Verifying that the apache files and directories are available on both the webservers in /var/www and on the NFS server in the /mnt/apps directory:

**On the webserver**

![](./img/project7/53-verifying%20nfs%20works-2.png)

**On the NFS server**

![](./img/project7/54-verifying%20nfs%20works.png)

-	Mounting the Apache log folder on the webservers to NFS server’s export for logs:` $ sudo mount -t nfs -o rw,nosuid 172.31.84.250:/mnt/logs /var/log/httpd`

**for webserver A**

![](./img/project7/55-mounting%20logs%20apache%20log.png)

**for webserver B**

![](./img/project7/mounting%20logs%20on%20apache%20log%20wbsB.png)

**for webserver C**

![](./img/project7/mounting%20logs%20on%20apache%20log%20wbsC.png)

-	Updating the fstab config file to make the mount persist on boot: `sudo vi /etc/fstab`

**for webserver A**
![](./img/project7/60-updating%20the%20fstab%20for%20log%20mount.png)

**for webserver B**
![](./img/project7/updating%20the%20fstab%20for%20log%20mount%20on%20wbsB.png)

**for webserver C**
![](./img/project7/updating%20the%20fstab%20for%20the%20webserver%20C.png)

-	Installing git to be able to clone a github repo:`$ sudo yum install git`
![](./img/project7/56-installing%20git.png)
![](./img/project7/57-installing%20git-2.png)

-	Forked the Darey’s repo into my github account and cloning it from the terminal:`$ git clone https://github.com/apotitech/tooling.git`

![](./img/project7/58-cloning%20the%20tooling%20repo.png)

-	Copying the html folder from the cloned repo to /var/www/html:`$ sudo cp –R html/. /var/www/html`

![](./img/project7/59-copying%20html%20folder%20to%20html%20folder%20in%20www.png)

-	Adding a rule in the security group of the webservers to be able to listen to port 80:
![](./img/project7/61-adding%20port%2080%20for%20the%20webservers.png)

-	Disabling SELInux :`$ sudo setenforce 0`

![](./img/project7/65-disabling%20selinx.png)

-	Opening the SELinux file and disabling SELinux option:`$ sudo vi /etc/sysconfig/selinux`

![](./img/project7/66-disabling%20selinux-2.png)

-	Updating the website configuration to connect to the database: `$ sudo vi /var/www/html/functions.php`
![](./img/project7/76-updating%20the%20functions.php.png)

- Installing mysql client on the webserver:`$ sudo yum install mysql`
![](./img/project7/72-installing%20mysql%20in%20webservers.png)

-	Executing the tooling-db.sql script with the database private IP address to load data in tooling database from the webserver:`$ mysql -h 172.31.27.76 -u webaccess -p tooling < tooling-db.sql`
![](./img/project7/73-running%20tooling-db%20script.png)
- verifying that tooling-db.sql executed successfully:
![](./img/project7/74-database%20loaded.png)

-	Starting the apache service to serve the web content on my browser:`$ sudo systemctl start httpd`
![](./img/project7/78-starting%20apache%20service.png)

## Step 5:  Adding A New User In The Tooling Database
-	Activating the mysql shell in the database server terminal:`$ sudo mysql`
-	Switching to tooling database:`mysql> use tooling;`
-	Creating the new user:`mysql> INSERT INTO users (id,username,password,email,user_type,status) VALUES(1, ‘myuser’, ‘password’,‘user@mail.com’,‘admin’,‘1’);`
![](./img/project7/79-creating%20myuser%20on%20db%20server.png)

## Final step: Result
Testing the DevOps Tooling website in my browser:

**For webserver A:** http://3.94.55.87/index.php
![](./img/project7/77-testing%20the%20site%20on%20wbsA.png)
![](./img/project7/78-testing%20the%20site%20on%20wbsA-2.png)

**For webserver B:** http://44.203.88.57/index.php
![](./img/project7/testing%20the%20site%20on%20wbsB.png)
![](./img/project7/testing%20the%20site%20on%20wbsB-2.png)

**For webserver C:** http://54.211.180.27/index.php
![](./img/project7/testing%20the%20site%20on%20wbsC.png)
![](./img/project7/testing%20the%20site%20on%20wbsC-2.png)


