# Setting up Amazon Elastic Container Registry (ECR), Amazon Elastic Container Service (ECS), and Amazon Elastic Kubernetes Service (EKS)

![AWS](https://imgur.com/fOUBFH3.png)

Setting up Amazon Elastic Container Registry (ECR), Amazon Elastic Container Service (ECS), and Amazon Elastic Kubernetes Service (EKS) to deploy a "Hello World" image in a Kubernetes cluster on AWS involves several steps. Here's a high-level overview:

1. **Create an ECR Repository**: Set up an ECR repository to store your Docker image.

2. **Build and Push Docker Image**: Build a Docker image for your "Hello World" application, tag it, and push it to the ECR repository.

3. **Create an ECS Task Definition**: Define a task definition in ECS that references your ECR image and specifies container settings.

4. **Create an ECS Service**: Create an ECS service using the task definition, specifying desired tasks and networking settings.

5. **Set Up an EKS Cluster**: Create an EKS cluster to run your Kubernetes workload.

6. **Deploy the Kubernetes Deployment**: Create a Kubernetes Deployment YAML file referencing your ECR image and deploy it to your EKS cluster.

Here are the detailed steps:

**Step 1: Create an ECR Repository**

1. Go to the AWS Management Console.

2. Navigate to the Amazon ECR service.

3. Click on "Repositories" in the left navigation pane.

4. Click the "Create repository" button.

5. Give your repository a name and configure any repository settings as needed.

6. Click the "Create repository" button.

**Step 2: Build and Push Docker Image to ECR**

1. Build your Docker image for your "Hello World" application locally or using a CI/CD pipeline.

2. Authenticate Docker with your ECR repository:

   ```bash
   aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<your-region>.amazonaws.com
   ```

   Replace `<your-region>` with your AWS region and `<account-id>` with your AWS account ID.

3. Tag your Docker image with the ECR repository URI:

   ```bash
   docker tag hello-world:latest <account-id>.dkr.ecr.<your-region>.amazonaws.com/<repository-name>:latest
   ```

4. Push the Docker image to ECR:

   ```bash
   docker push <account-id>.dkr.ecr.<your-region>.amazonaws.com/<repository-name>:latest
   ```

**Step 3: Create an ECS Task Definition**

1. In the ECS dashboard, click on "Task Definitions" in the left navigation pane.

2. Click the "Create new Task Definition" button.

3. Select the launch type compatibility (Fargate or EC2) based on your requirements.

4. Define your task and container settings. Specify the image you pushed to ECR in the previous step.

5. Configure task execution roles, network, and other settings as needed.

6. Create the task definition.

**Step 4: Create an ECS Service**

1. In the ECS dashboard, click on "Clusters."

2. Click on your cluster to open its details.

3. Click the "Create" button in the "Services" tab.

4. Configure your service settings, including the task definition, cluster, desired count, and network configuration.

5. Click "Next" and review your settings.

6. Create the service.

**Step 5: Set Up an EKS Cluster**

1. In the AWS Management Console, navigate to the Amazon EKS service.

2. Click "Create cluster."

3. Configure your EKS cluster settings, including the VPC, subnets, security group, and role.

4. Click "Create."

**Step 6: Deploy the Kubernetes Deployment**

1. Use `kubectl` to create a Kubernetes Deployment YAML file that references your ECR image.

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: hello-world
   spec:
     replicas: 1
     template:
       metadata:
         labels:
           app: hello-world
       spec:
         containers:
         - name: hello-world
           image: <account-id>.dkr.ecr.<your-region>.amazonaws.com/<repository-name>:latest
   ```

   Replace `<account-id>`, `<your-region>`, and `<repository-name>` with your actual values.

2. Deploy the Kubernetes Deployment to your EKS cluster:

   ```bash
   kubectl apply -f deployment.yaml
   ```

This setup will deploy your "Hello World" Docker image in a Kubernetes cluster running on Amazon EKS, with the image stored in Amazon ECR. Make sure to configure additional resources, such as services and ingress, as needed for your application.

## By [Harshhaa Reddy](https://www.github.com/NotHarshhaa)
