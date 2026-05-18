# AUX PROJECT 1: ONBOARDING NEW LINUX USERS ONTO A SERVER WITH SHELL SCRIPT

## Introduction
In this project, 20 new users are created on a server and assigned to a group called 'developers' of which a default home directory is created for each of them. For each of the users, an authorized_keys file is created and a public key is inserted which will be used to connect to the new users from the client. This task is automated using shell scripting.
The following steps are taken to create an automated task that onboard 20 new users on server with shell script:

## Step 1 :	Creating the users on the server

-	Editing the authorized_keys file of the current user in the server from the home directory :`$ nano .ssh/authorized_keys`
-	Pasting the following public key:
`ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCzKZyicHxIkklSrNlxsJyyTrcIdBIt84Z0cQb3R4k0jH53kxkaT5hP8tfWTe62LXi7vV86fY+SX7TBNM76XGCbw/6vrMGegm6J1x2i1AiLNwq5nqTjOGn0AIwku4IlCCLAB7tdfRyVuCarmBlwny3lzRyybIUAWXR/D6vpN09MsDILbKdhay+Q/p9OUBMSLPqXdY/QIh/Oe3rVv1lwY3AohNfq7V3tO88zKswfA5iiexNiSYX1myT0OrX8cBE771j9quoNZhQgaLI1mIMtAvnHQChrn9k2nUaO/BMBCQGol5XzGv1ado7hgoVPoluIUD+FGNo/pH4zcmDLICH6drXY/C9MESnkMUPLFxBXKO/OitApY71vRao9nAhAwpVMsy6FqiOb5uawhvhoHYIHTV/f4EtagVagRMP2PxYMYR6jykIV4MPJTkCm+lGhTyMlRu+qRQjdLn8AAtHf4aEV8dIkoGh088DI7eA/4o0wz4OV4upH5ewSFS+5IHmRECEW5Nc= `
![](./img/auxProject/copied%20and%20paste%20the%20pub_key%20in%20current%20user%20in%20server.png)

-	Creating a new folder and moving into it: `$ mkdir shell && cd shell`
-	Creating a file that holds the names of the users: `$ touch names.csv`
-	Inputting the names: `$ nano names.csv`
![](./img/auxProject/names.csv%20file.png)
-	Creating a shell script file in the same folder that will automate the task: `$ touch addusers.sh`
-	Opening the file: `$ nano addusers.sh`
-	Entering the following lines of commands:
```
#! /bin/bash

users=$(cat ./names.csv)

# TO CREATE A USER
for user in $users
 do
if [ -e "/etc/passwd/$user" ]
 then
        echo "The user $user exist"
 else
        sudo useradd $user
        echo "The user $user is created successfully"
        sudo usermod -a -G developers $user
        echo "User $user is added to developers group"
fi
done

# TO CREATE HOME DIRECTORY FOR A USER IF IT DOES NOT EXIST
for user in $users
 do
if [ -d "/home/$user" ]
 then
       echo "The directory /home/$user exist"
 else
sudo mkdir -p /home/$user
        echo "The home directory of the user $user /home/$user is created successfully"
        sudo usermod -d /home/$user $user
fi
done

# TO CREATE .SSH FOLDER FOR THE USER AND PASTE THE AUTHORIZED_KEYS FROM THE CURRENT USER IN THE SERVER TO THE NEW USER
for user in $users
 do
if [ -d "/home/$user/.ssh" ]
 then
       echo "The directory /home/$user/.ssh exist"
 else
        sudo mkdir "/home/$user/.ssh"
        echo "The directory /home/$user/.ssh is created successfully"
        sudo touch "/home/$user/.ssh/authorized_keys"
        echo "The file authorized_keys is created successfully"
        sudo chown $USER:$USER /home/$user/.ssh
        sudo chown $USER:$USER /home/$user/.ssh/authorized_keys
        sudo cat "/home/somex/.ssh/authorized_keys" >> "/home/$user/.ssh/authorized_keys"
        echo "authorized_key file transffered successfully"
fi
done
```

-	 Running the shell script file: `$ ./addusers.sh`
![](./img/auxProject/executing%20the%20shell%20script-1.png)
![](./img/auxProject/executing%20the%20shell%20script-2.png)
![](./img/auxProject/executing%20the%20shell%20script-3.png)

## Step 2:	On the client

-	Updating the private key file: `$ nano .ssh/id_rsa`
-	Pasting a private key generated for your own lab environment. Do not commit real private key material to this repository.
![](./img/auxProject/editing%20the%20private%20key%20file%20for%20the%20client.png)
-	Updating the public key file: `$ nano .ssh/id_rsa.pub`
-	Pasting the following public key which is the same as the one pasted on the server
![](./img/auxProject/updating%20the%20public%20key%20file%20in%20the%20client.png)

## Step 3: Connecting to the new users created on the server 

On the client machine: Testing Few users 
-	**Connecting to the user victor: ssh victor@192.168.43.55**
![](./img/auxProject/connecting%20to%20the%20user%20victor.png)
-	**Connecting to the user David: ssh david@192.168.43.55**
![](./img/auxProject/connecting%20to%20the%20user%20david.png)
-	**Connecting to the user Luarel: ssh luarel@192.168.43.55**
![](./img/auxProject/connecting%20to%20the%20user%20luarel.png)
-	**Connecting to the user Raymond: ssh raymond@192.168.43.55**
![](./img/auxProject/connecting%20to%20the%20user%20raymond.png)
-	**Connecting to the user Stella: ssh stella@192.168.43.55**
![](./img/auxProject/connecting%20to%20the%20user%20stella.png)

