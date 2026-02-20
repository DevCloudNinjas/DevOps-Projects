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
-	Pasting the following private key:
`-----BEGIN OPENSSH PRIVATE KEY-----
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
kmaSGj362OnCCNAAAACWRhcmVARGFyZQE=
-----END OPENSSH PRIVATE KEY-----`
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

