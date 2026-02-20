#!/bin/bash

Java Installations
sudo apt-get install openjdk-11-jdk -y
sudo apt-get install zip -y
echo 'JDK Installed successfully installer'


# Jenkins installations
sudo apt update
apt install make
sudo apt-get install debian-keyring debian-archive-keyring --assume-yes
sudo apt-key update
sudo apt-get update
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5
sudo apt update
sudo apt install openjdk-11-jre-headless --assume-yes
sudo java -version
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins --assume-yes
# sudo service jenkins status
echo 'Jenkins successfully installer'
# # Postgres Installation
# sudo apt update
# # enable repository to install postgresql
# sudo apt install postgresql postgresql-contrib --assume-yes
# # Install PostgreSQ L server and initialize the database 
# # cluster for this server
# # Start the db service
# # systemctl stop postgresql
# # systemctl enable postgresql
# # systemctl start postgresql
# # systemctl status postgresql
echo 'Postgresql Installed successfully installer'

# # Docker installation
# sudo apt install apt-transport-https ca-certificates curl software-properties-common --assume-yes
# sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable'
# apt-cache policy docker-ce
# sudo apt install docker-ce --assume-yes
# sudo chmod 777 /var/run/docker.sock

# # sudo systemctl status docker
# echo 'Docker successfully installer'

# # install docker compose
# sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 
# sudo chmod +x /usr/local/bin/docker-compose
# docker-compose --version
# echo "Docker Compose Installed successfully installer"

# # nginx installation for testing purpose
# docker run --name mynginx1 -p 80:80 -d nginx
# echo "nginx server running in your domain.com at port 80"

# curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
# sudo mv /tmp/eksctl /usr/local/bin 
# eksctl version
# echo "eksctl Installed successfully installer"

# curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.27.1/2023-04-19/bin/linux/amd64/kubectl
# chmod +x ./kubectl
# mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
# echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
# kubectl version --short --client