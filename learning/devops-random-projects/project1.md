# SETTING UP A LAMP STACK WEB SERVER IN THE AWS CLOUD

A LAMP stack web server is a set of frameworks and tools that comprises Linux, Apache server, MySql and PHP.
 The following are the steps I took in setting up a LAMP stack web server in the AWS cloud:
 
## STEP 1: Launching A New EC2 Instance in the AWS cloud

With my aws account already setup, I launched a new EC2 Instance of t2.micro family with Ubuntu Server 20.04 LTS (HVM) and downloaded a new private key (.pem file). 

## STEP 2: Connecting to my EC2 Instance

As a windows user I downloaded putty application inorder to be able to connect to my EC2 Instance after converting my private key(.pem file). Since Putty does not support .pem files, I have to convert my private key (.pem format) into another file format called .ppk using PuttyGen.
After converting my .pem file to .ppk file, I launched the Putty application and then connected to my EC2 Instance by pasting my public IP address to my Instance in the appropriate field and loaded my .ppk file in the auth section under SSH category. 
![](./img/lamp-images/connecting%20to%20ec2%20machine.png)

## STEP 3: Installing Apache and updating firewall in the EC2 Instance

After a successful connection, next is configuring the EC2 machine to be able to serve a web server. The following are the steps I took to installing Apache on the EC2 machine on the terminal window:
-	Updating a list of packages in package manager: `$ sudo apt update`
-	Run apache2 package installation: `$ sudo apt install apache2`
![](./img/lamp-images/installing%20apache2.png)
-	To verify that apache2 is running as a Service in my OS: `$ sudo systemctl status apache2`
![](./img/lamp-images/Apache2%20running%20perfectly.png)
 **Apache2 is perfectly installed**

- Configuring the security group of my EC2 instance by adding a rule in the inbound section inorder to be able to listen to port 80 and also make it to allow access to any IP when it is accessed by a web browser
![](./img/lamp-images/adding%20http%20rule.png)

- To access it locally in my Ubuntu shell; `$ curl http://localhost:80 or curl http://127.0.0.1:80`

- Testing how the Apache HTTP server can respond to requests from the Internet; Pasting my public address in the browser and tapping enter:
![](./img/lamp-images/Apache2%20working%20on%20browser.png)
**This shows that my web server is now correctly installed and accessible through my firewall.**

## STEP 4: Installing MySQL

Now that the server is up and running, installing MySQL gives the ability to store and manage data for my site in a relational database. The following are the steps I took to installing MySQL in the EC2 machine:
Running the following command in a terminal window that is still connected to the EC2 instance;
-	To acquire and install the software: `$ sudo apt install mysql-server`
![](./img/lamp-images/installing%20mysql%20server.png)

- After a successful installation,  it’s recommended that one runs a security script that comes pre-installed with MySQL which removes insecure default settings and lock down access to my database system. The following command is entered:
`$ sudo mysql_secure_installation`
- Next is accepting to configure the VALIDATE PASSWORD PLUGIN when prompted, and selecting any of the three levels of the password validation policy and then typing a new password that corresponds to the level of password validation policy selected.
- And finally tapping the Y and hitting Enter key at the subsequent prompt that follow after which will remove some anonymous users and the test database, disable remote root logins, and load these new rules so that MySQL immediately respects the changes you have made.
![](./img/lamp-images/mysql%20secure%20installation.png)

-	Testing if I am able to log into MySQL console: `$ sudo mysql`

## STEP 5: Installing PHP

The following steps are taken to installing PHP in the Instance which will allow us to display dynamic content to the end user:

-	Installing PHP and two other packages: `$ sudo apt install php libapache2-mod-php php-mysql`

![](./img/lamp-images/installing%20php.png)

-	To confirm the PHP version installed: `$ php –v`

![](./img/lamp-images/php%20installed%20perfectly.png)

At this point the LAMP stack is completely installed and fully operational

## Step 6 — Creating a Virtual Host for my Website using Apache

Apache on Ubuntu 20.04 has one server block enabled by default that is configured to serve documents from the /var/www/html directory. The following steps are taken to setting up a virtual host:
-	Creating a directory called projectLamp as my domain: `$ sudo mkdir /var/www/projectlamp`
-	Assigning ownership of the directory with the $USER environment variable, which will reference my current system user: `$ sudo chown -R $USER:$USER /var/www/projectlamp`
-	creating and opening a new configuration file in Apache’s sites-available directory: $ sudo vi /etc/apache2/sites-available/projectlamp.conf
-	pasting the following configurations in the file: 
```
<VirtualHost *:80>
	    ServerName projectlamp
	    ServerAlias www.projectlamp 
	    ServerAdmin webmaster@localhost
	    DocumentRoot /var/www/projectlamp
	    ErrorLog ${APACHE_LOG_DIR}/error.log
	    CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
 ```
 ![](./img/lamp-images/configuring%20virtual%20host.png)
 
 - Save and quit by hitting esc key and typing :wq and pressing enter key
 

-	Enabling the new virtual host: `$ sudo a2ensite projectlamp`
-	Disabling the default website that comes installed with Apache: `$ sudo a2dissite 000-default`
-	Ensuring my configuration doesn’t contain any error: `$ sudo apache2ctl configtest`
-	Reloading Apache so these changes take effect: `$ sudo systemctl reload apache2`
-	Creating an index.html file in the location of my domain directory inorder to test that the virtual host works as expected : `$ sudo echo 'Hello LAMP from hostname' $(curl -s http://169.254.169.254/latest/meta-data/public-hostname) 'with public IP' $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4) > /var/www/projectlamp/index.htm`

![](./img/lamp-images/enabling%20the%20new%20config.png)

-	Running my IP address on the browser to test if it works as expected

![](./img/lamp-images/new%20virtual%20host%20working%20on%20browser.png)

## STEP 7: Enabling PHP on the website

With the default DirectoryIndex settings on Apache, a file named index.html will always take precedence over an index.php . To change this behavior is to edit the dir.conf file and change the order in which the index.php file is listed within the DirectoryIndex directive:
- Editing the dir.conf file :`$ sudo vim /etc/apache2/mods-enabled/dir.conf`
```
<IfModule mod_dir.c>
        #Change this:
        #DirectoryIndex index.html index.cgi index.pl index.php index.xhtml index.htm
        #To this:
        DirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm
</IfModule>
```
- Reloading the apache server: `$ sudo systemctl reload apache2`

- Creating an index.php file and adding a PHP script in it to test that PHP is correctly installed and configured on your server: `$ vim /var/www/projectlamp/index.php`

- Adding the following PHP script
 ```
 <?php
phpinfo();
```
![](./img/lamp-images/editing%20the%20dir%20file.png)

- Refreshing my web page and woala!

![](./img/lamp-images/php%20working%20on%20browser.png)

Removing the php file as it contains sensitive information about your PHP environment and my Ubuntu server
$ sudo rm /var/www/projectlamp/index.php
