# Cloud-Native-Monitoring-App

## Deploying an App built with Python using Flask and psutil on ECR and Kubernete
This is a monitoring app built with python, and it would be contanerized with docker and deployed to EkS

### Prerequisites
- Learn Docker and How to containerize a Python application
- Creating Dockerfile
- Building DockerImage
- Running Docker Container
- Docker Commands
- Create ECR repository using Python Boto3 and pushing Docker Image to ECR
- Learn Kubernetes and Create EKS cluster and Nodegroups
- Create Kubernetes Deployments and Services using Python!

### STEP 1 - Installations of Services on your WorkStation
- Install AWS CLI, then Go to your aws account and get your secret keys and configure the workspace `aws configure`
- Install [python](https://www.python.org/downloads/) on your workstation and a python extention in vscode
- The application uses the **`psutil`** and **`Flask`, Plotly, boto3** libraries. Install them using pip `pip3 install -r requirements.txt`
- Install dependencies psutil `pip3 install psutil` and flask `pip install flask`
- Install python for ECR SDK `pip install boto3` 
- Install kubernetes, add the K8S python dependencies client  library `pip install kubernetes`
 the extenstion of kubernetes in vscode
- Install the docker extention in vscode

### Step 2: Run the application

To run the application, navigate to the root directory of the project and execute the following command:

```
$ python3 app.py
```

This will start the Flask server on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

### Step 3: Dockerizing the Flask application

- Create a **`Dockerfile`** in the root directory of the project with the following contents:

```yml
# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set the environment variables for the Flask app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the Flask app will run
EXPOSE 5000

# Start the Flask app when the container is run
CMD ["flask", "run"]
```

- Build the Docker image, execute the following command:

```yml
$ docker build -t <image_name> .
```

-  Run the Docker container, execute the following command:

```yml
$ docker run -p 5000:5000 <image_name>
```

This will start the Flask server in a Docker container on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

### Step 4 - Pushing the Docker image to ECR

- Create an ECR repository using Python in a folder `ecr.py`:
- Configure the ECR repository to your workspace to enable a push, you will find the process in console `view push commands`

```py
import boto3

# Create an ECR client
ecr_client = boto3.client('ecr')

# Create a new ECR repository
repository_name = 'my-ecr-repo'
response = ecr_client.create_repository(repositoryName=repository_name)

# Print the repository URI
repository_uri = response['repository']['repositoryUri']
print(repository_uri)
```
Then run this `python3 ecr.py`

- Setup password and credentials for ECR

```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 221650130255.dkr.ecr.us-east-1.amazonaws.com
```

- Push the Docker image to ECR using the push commands on the console:

```
 $ docker push <ecr_repo_uri>:<tag>
```

### Step 5 - Creating an EKS cluster and deploying the app using Python**


- Create an EKS cluster `cloud-native-cluster` and add node group in aws console


- Create a node group `nodes` in the EKS cluster.

- Create deployment and service in a folder `eks.py`

```py
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="568373317874.dkr.ecr.us-east-1.amazonaws.com/my-cloud-native-repo:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# This is an automation to run deployment and svc using python
# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)
```

make sure to edit the name of the image on line 25 with your image Url.

> *To run the K8s commands for  deployment and service instead of adding the python script you create `deployment.yml and service.yml`use these commands `kubectl apply -f deployment.yml` and `kubectl apply -f service.yml`*

- Configure the aws EKS to your work space
```yml
aws eks update-kubeconfig --name cloud-native-cluster
```

- Once you run this file by running “python3 eks.py” deployment and service will be created.
- Check by running following commands:

```yml
kubectl get deployment -n default (check deployments)
kubectl get service -n default (check service)
kubectl get pods <name of pod> -n default (to check the pods)

#edit images created if u made errors
kubectl edit deployment my-flask-app -n default 

#this will pull down the editted image
kubectl get pod -n default -w
```

Once your pod is up and running, run the port-forward to expose the service
```yml
kubectl port-forward service/<service_name> 5000:5000
```

# Hit the Star! ⭐
***If you are planning to use this repo for learning, please hit the star. Thanks!***

#### Author by [DevCloud Ninjas](https://github.com/DevCloudNinjas)
