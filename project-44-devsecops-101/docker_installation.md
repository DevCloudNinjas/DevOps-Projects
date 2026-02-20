#Step 1: Update system repositories
```sh 
   sudo apt update
   ``` 
#Step 2: Install required dependencies
```sh 
   sudo apt install lsb-release ca-certificates apt-transport-https software-properties-common -y

   ```
#Step 3: Adding Docker repository to system sources
```sh 
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
#Step 4: Update system packages  
```sh 
   sudo apt update
   ```
 #Step 5: Install Docker on Ubuntu 22.04
   

   ```sh 
   sudo apt install docker-ce -y
   ```
   #Step 6: Verify Docker status
   

   ```sh 
   sudo systemctl status docker
   ```
   #Step 6: Add user to docker group 
   

   ```sh 
    sudo usermod -aG docker $USER
   ```
