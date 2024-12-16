1. Login to the server as super user and perform below
i. Create users and set passwords – user1, user2, user3
ii. Create Groups – devops, aws
iii. Change primary group of user2, user3 to devops group
iv. Add aws group as secondary group to user1
v. Create the file and directory structure shown in the above diagram.
vi. Change group of /dir1, /dir7/dir10, /f2 to “devops” group
vii. Change ownership of /dir1, /dir7/dir10, /f2 to “user1” user

Commands used

# Create users
useradd user1
useradd user2
useradd user3

# Set passwords for each user
passwd user1
passwd user2
passwd user3

# Create groups
groupadd devops
groupadd aws

# Change Primary Group of user2 and user3 to 'devops'
usermod -g devops user2
usermod -g devops user3

# Add 'aws' Group as a Secondary Group to user1
usermod -aG aws user1

# Create the file and directory structure shown in the above diagram.
mkdir -p /dir1/fi /dir2/dir1/dir2/dir10/f3 /dir3/dir11 /dir4/dir12/f5/f4 /dir5/dir13 /dir6 /dir7/dir10/f3 /dir8/dir9 fi f2 opt/dir14/dir10/53


# Change group of /dir1, /dir7/dir10, /f2 to “devops” group
sudo chgrp -R devops /dir1 /dir7/dir10 /f2

# Change the Ownership of /dir1, /dir7/dir10, /f2 to the User "user1"
sudo chown -R user1:user1 /dir1 /dir7/dir10 /f2


2. Login as user1 and perform below
i. Create users and set passwords – user4, user5

Commands used

I first gave the user1 sudo privileges by running the command

sudo usermod -aG sudo user1

Switched to user1.
su - user1

sudo useradd user4
sudo passwd user4

sudo useradd user5
sudo passwd user5

ii. Create Groups – app, database

sudo groupadd app
sudo groupadd database


3. Login as ‘user4’ and perform below
I. Create directory – /dir6/dir4
ii. Create file – /f3
iii. Move the file from “/dir1/f1” to “/dir2/dir1/dir2”
iv. Rename the file ‘/f2′ to /f4’

Commands used:

sudo usermod -aG sudo user4 (for sudo privileges)

su - user4

sudo mkdir -p /dir6/dir4

sudo touch /f3

sudo mkdir /dir1/f1  # created it because the file doesn't exist in user4

sudo mv /dir1/f1 /dir2/dir1/dir2/

sudo mv /f2 /f4


4. Login as ‘user1’ and perform below

I. Create directory – “/home/user2/dir1”
ii. Change to “/dir2/dir1/dir2/dir10” directory and create file “/opt/dir14/dir10/f1” using relative path method.
iii. Move the file from “/opt/dir14/dir10/f1” to user1 home directory
iv. Delete the directory recursively “/dir4”
v. Delete all child files and directories under “/opt/dir14” using single command.
vi. Write this text “Linux assessment for a DevOps Engineer!! Learn with Fun!!” to the /f3 file and save it.

Commands used:

# Task I: Create directory
sudo mkdir -p /home/user2/dir1

# Task II: Create file using relative path
cd /dir2/dir1/dir2/dir10
sudo mkdir -p ../../../opt/dir14/dir10
sudo touch ../../../opt/dir14/dir10/f1

# Task III: Move file to user1 home directory
mv ../../../opt/dir14/dir10/f1 ~/

# Task IV: Delete directory recursively
sudo rm -rf /dir4

# Task V: Delete child files and directories under /opt/dir14
sudo rm -rf /opt/dir14/*

# Task VI: Write text to /f3 file
echo "Linux assessment for a DevOps Engineer!! Learn with Fun!!" | sudo tee /f3


5. Login as ‘user2’ and perform below
I. Create file “/dir1/f2”
ii. Delete /dir6
iii. Delete /dir8
iv. Replace the “DevOps” text to “devops” in the /f3 file without using an editor.
v. Using Vi-Editor, copy line1 and paste 10 times in the file /f3.
vi. Search for the pattern “Engineer” and replace with “engineer” in the file /f3 using a single command.
vii. Delete /f3

Commands used:

sudo chown -R user2:user2 /dir6

sudo usermod -aG sudo user2

sudo su - user2

sudo touch /dir1/f2

sudo rm -r /dir6

sudo rm -r /dir8

sudo sed -i 's/DevOps/devops/g' /f3

echo -e "Linux assessment for a DevOps Engineer!! Learn with Fun!!\n" | vim -c "10r !" -c "wq" /f3

sudo sed -i 's/Engineer/engineer/g' /f3

sudo rm /f3


9. Login as ‘user5’ and perform below
I. Delete /dir1
ii. Delete /dir2
iii. Delete /dir3
iv. Delete /dir5
v. Delete /dir7
vi. Delete /f1 & /f4
vii. Delete /opt/dir14


Commands used:

sudo usermod -aG sudo user5

su - user5

sudo rm -r /dir2

sudo rm -r /dir3

sudo rm -r /dir5

sudo rm -r /dir7

sudo rm -r /f1
sudo rm -r /f4
sudo rm -r /opt/dir14


10. Logins as ‘root’ user and perform below
Delete users – user1, user2, user3, user4, user5
Delete groups – app, aws, database, devops
Delete home directories of all users user1, user2, user3, user4, user5 if any exist still.

Commands used:

# To delete users
sudo userdel -r user1
sudo userdel -r user2
sudo userdel -r user3
sudo userdel -r user4
sudo userdel -r user5

# Delete Groups
sudo groupdel app
sudo groupdel aws
sudo groupdel database
sudo groupdel devops

# Delete Home Directories
sudo rm -rf /home/user1
sudo rm -rf /home/user2
sudo rm -rf /home/user3
sudo rm -rf /home/user4
sudo rm -rf /home/user5












