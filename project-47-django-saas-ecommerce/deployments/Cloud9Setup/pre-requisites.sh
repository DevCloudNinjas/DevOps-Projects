#!/bin/bash -x
. /home/ec2-user/.nvm/nvm.sh

#Install python3.8
sudo yum install -y amazon-linux-extras
sudo amazon-linux-extras enable python3.8
sudo yum install -y python3.8
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo alternatives --set python3 /usr/bin/python3.8

# Uninstall aws cli v1 and Install aws cli version-2.3.0
sudo pip2 uninstall awscli -y

echo "Installing aws cli version-2.3.0"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.3.0.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm awscliv2.zip
rm -rf aws 

# Install sam cli version 1.33.0
echo "Installing sam cli version 1.33.0"
wget https://github.com/aws/aws-sam-cli/releases/download/v1.33.0/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install
if [ $? -ne 0 ]; then
	echo "Sam cli is already present, so deleting existing version"
	sudo rm /usr/local/bin/sam
	sudo rm -rf /usr/local/aws-sam-cli
	echo "Now installing sam cli version 1.33.0"
	sudo ./sam-installation/install    
fi
rm aws-sam-cli-linux-x86_64.zip
rm -rf sam-installation

# Install git-remote-codecommit version 1.15.1
echo "Installing git-remote-codecommit version 1.15.1"
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
rm get-pip.py

python3 -m pip install git-remote-codecommit==1.15.1

# Install node v16.20.0
echo "Installing node v16.20.0"
nvm deactivate
nvm uninstall node
nvm install v16.20.0
nvm use v16.20.0
nvm alias default v16.20.0

# Install cdk cli version ^2.0.0
echo "Installing cdk cli version ^2.0.0"
npm uninstall -g aws-cdk
npm install -g aws-cdk@"^2.0.0"

#Install jq version 1.5
sudo yum -y install jq-1.5

#Install pylint version 2.11.1
python3 -m pip install pylint==2.11.1
