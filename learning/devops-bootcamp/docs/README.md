---
docs/1-introduction/1.1-devops-defined.md:
  category: Fundamentals
  estReadingMinutes: 30
docs/1-introduction/1.2-devcloudninjas-and-devops.md:
  category: Fundamentals
  estReadingMinutes: 5
docs/1-introduction/1.2.1-dojo.md:
  category: Fundamentals
  estReadingMinutes: 5
docs/1-introduction/1.3.1-unix.md:
  category: Fundamentals
  estReadingMinutes: 30
docs/1-introduction/1.3.2-vim.md:
  category: Fundamentals
  estReadingMinutes: 15
  exercises:
    - name: hello vim
      description: create a file in Vim
      estMinutes: 5
      technologies:
        - Vim
docs/1-introduction/1.3.3-installations.md:
  category: Fundamentals
  estReadingMinutes: 10
docs/1-introduction/1.3.4-passwords-and-keys.md:
  category: Fundamentals
  estReadingMinutes: 10
  exercises:
    - name: hello ssh
      description: create ssh keypair and ssh to a host
      estMinutes: 15
      technologies:
        - ssh
docs/1-introduction/1.3.5-networking.md:
  category: Fundamentals
  estReadingMinutes: 10
  exercises:
    - name: hello network
      description: explore the network of your local computer
      estMinutes: 15
docs/1-introduction/1.4-external-resources.md:
  category: Fundamentals
  estReadingMinutes: 50
docs/2-Github/2.2-Actions.md:
  category: CI/CD
  estReadingMinutes: 20
  exercises:
    - name: Augment basic workflow
      description: >-
        Take a basic workflow and update it to include a few common things
        you'll see inside GitHub Actions
      estMinutes: 60
      technologies:
        - GitHub Actions
    - name: Going Deeper
      description: >-
        Take the newly improved workflow and use different methods to achieve
        the same thing.  Introduces new important concepts/actions
      estMinutes: 120
      technologies:
        - GitHub Actions
    - name: Consolidate what we have and make it reusable
      description: >-
        Now we go one step further and take one of our jobs and make it into a
        composite action then take our whole workflow and bundle it into a
        reusable version
      estMinutes: 240
      technologies:
        - GitHub Actions
docs/2-Github/2.3-Projects.md:
  category: Agile Development
  estReadingMinutes: 5
  exercises:
    - name: Create your own Project
      description: >-
        Play around with GitHub Projects and get used to using its many features
        and interfaces to organize your work.
      estMinutes: 80
      technologies:
        - GitHub Projects
docs/2-Github/2.4-APIs.md:
  category: Fundamentals
  estReadingMinutes: 30
  exercises:
    - name: Interact with GitHub using its two available APIs
      description: >-
        Create and retrieve resources in GitHub using the REST and GraphQL
        APIs.  Get some experience using them and compare the two approaches.
      estMinutes: 180
      technologies:
        - APIs
        - Javascript
docs/2-Github/2.5-Security.md:
  category: Fundamentals
  estReadingMinutes: 30
  exercises:
    - name: Code-scanning
      description: >-
        Setup code-scanning in your own repository and view its results in the
        Security tab
      estMinutes: 30
      technologies:
        - GitHub Security
    - name: Dependabot
      description: 'Setup dependabot alerts, version and security updates'
      estMinutes: 20
      technologies:
        - GitHub Security
    - name: Code-scanning
      description: >-
        Setup secret-scanning in your own repository and see how it prevents you
        from committing secrets
      estMinutes: 20
      technologies:
        - GitHub Security
docs/3-virtual-machines-containers/3.1-golden-images.md:
  category: Virtualization
  estReadingMinutes: 15
  exercises:
    - name: Hello VMWare Fusion
      description: >-
        Configure a VM with VMWare Fusion. Install some software and configure
        it for SSH
      estMinutes: 90
      technologies:
        - VMWare Fusion
        - Debian
    - name: hello Packer
      description: >-
        Use Packer to create an OVF configured identically to the VM you
        configured in exercise 1
      estMinutes: 210
      technologies:
        - VMWare Fusion
        - Packer
        - Debian
docs/3-virtual-machines-containers/3.2-local-development.md:
  category: Virtualization
  estReadingMinutes: 15
  exercises:
    - name: Packer to Vagrant
      description: >-
        Use Packer to create an image compatible with Vagrants Base Box
        requirements. Leverage a Packer provisioner to add ssh key, install
        dependencies and tools, leverage Packer post-processor to output an vmx
        and a vagrant box
      estMinutes: 420
      technologies:
        - Vagrant
        - Packer
        - Debian
docs/3-virtual-machines-containers/3.3-managing-infrastructure.md:
  category: Virtualization
  estReadingMinutes: 10
  exercises:
    - name: GitHub self-hosted runner and Nexus on VMs
      description: >-
        Create a VM from your golden image and install and configure Nexus OSS
        and deploy an artifact to that VM from a GitHub Action
      estMinutes: 390
      technologies:
        - Vagrant
        - Debian
        - GitHub Actions
        - Nexus OSS
docs/3-virtual-machines-containers/3.4-containers.md:
  category: Containerization
  estReadingMinutes: 20
  exercises:
    - name: Hello Containers
      description: Complete Docker's 'Hello World'
      estMinutes: 30
      technologies:
        - Docker
    - name: Self-hosted GitHub Action to Nexus containerized
      description: >-
        Containerize a self-hosted GitHub Action and Nexus and build a pipeline
        that pushes a PetClinic build artifact from one container to the other.
      estMinutes: 150
      technologies:
        - Docker
        - GitHub Actions
        - Nexus OSS
docs/3-virtual-machines-containers/3.5.1-docker-compose.md:
  category: Container Orchestration
  estReadingMinutes: 5
  exercises:
    - name: Docker Compose GitHub Actions and Nexus
      description: >-
        Create a compose file that spins up your GitHub Actions and Nexus
        containers, exposing ports, and using volumes for persistent storage
      estMinutes: 120
      technologies:
        - Docker
        - Docker Compose
        - GitHub Actions
        - Nexus OSS
docs/3-virtual-machines-containers/3.5.2-kubernetes.md:
  category: Container Orchestration
  estReadingMinutes: 15
  exercises:
    - name: Hello Minikube
      description: Complete the 'Hello Minikube' tutorial
      estMinutes: 60
      technologies:
        - Kubernetes
    - name: Kind cluster GitHub Actions and Nexus
      description: Create a Kind cluster running your GitHub Actions and Nexus containers
      estMinutes: 600
      technologies:
        - Kubernetes
        - GitHub Actions
        - Nexus OSS
docs/4-cloud-computing/4.0-overview.md:
  category: Cloud Computing
  estReadingMinutes: 30
docs/4-cloud-computing/4.1.1-aws.md:
  category: Cloud Computing
  estReadingMinutes: 60
docs/4-cloud-computing/4.1.2-azure.md:
  category: Cloud Computing
  estReadingMinutes: 30
docs/4-cloud-computing/4.2.1-s3-cloudfront.md:
  category: Cloud Computing
  estReadingMinutes: 20
  exercises:
    - name: Hello S3
      description: Host a static website in s3 publicly
      estMinutes: 150
      technologies:
        - AWS S3
        - AWS
    - name: Hello Cloudfront
      description: Create a CloudFront distribution for your s3 website
      estMinutes: 60
      technologies:
        - AWS S3
        - AWS
        - CloudFront
docs/4-cloud-computing/4.2.2-ec2.md:
  category: Cloud Computing
  estReadingMinutes: 30
  exercises:
    - name: Hello EC2
      description: >-
        Create EC2 VMs and configure one as a Jenkins controller server and the
        other as a Jenkins agent registered to the server.
      estMinutes: 240
      technologies:
        - AWS
        - EC2
        - Jenkins
docs/4-cloud-computing/4.2.3-auto-scaling.md:
  category: Cloud Computing
  estReadingMinutes: 20
  exercises:
    - name: Create EC2 instance with User Data
      description: Create an EC2 instance running Spring PetClinic.
      estMinutes: 240
      technologies:
        - AWS
        - EC2
    - name: Setup a Network Load Balancer
      description: >-
        Create a Load Balancer in AWS and register 2 EC2 configured to host a
        web application via User Data.
      estMinutes: 60
      technologies:
        - AWS
        - EC2
        - AWS ELB
    - name: Launch Templates
      description: >-
        Create a Launch Template that will create EC2 instances configured like
        the vm you made in exercise 1
      estMinutes: 60
      technologies:
        - AWS
        - EC2
        - AWS Launch Templates
    - name: Auto Scaling Groups
      description: >-
        Create an AutoScaling group leveraging the Launch Template you made in
        exercise 3
      estMinutes: 60
      technologies:
        - AWS
        - EC2
        - AWS Launch Templates
        - AWS Auto Scaling Groups
        - AWS ELB
docs/4-cloud-computing/4.2.4-aws-packer.md:
  category: Cloud Computing
  estReadingMinutes: 20
  exercises:
    - name: Creating a custom AMI
      description: >-
        Create an AMI with Packer that creates a provisioned machine like the
        one you made in exercise 1 from 4.2.3. Create a Launch Template and Auto
        Scaling group to leverage your new AMI via the AWS cli
      estMinutes: 180
      technologies:
        - AWS
        - EC2
        - AWS Launch Templates
        - AWS Auto Scaling Groups
        - Packer
docs/4-cloud-computing/4.2.5-lambda.md:
  category: Cloud Computing
  estReadingMinutes: 20
  exercises:
    - name: Creating a Lambda function with a trigger
      description: >-
        Create a Lambda function that sets up an s3 bucket and a DynamoDB,
        downloads a csv file, and then uses a python script to parse the csv and
        push all the data into DynamoDB.
      estMinutes: 480
      technologies:
        - AWS
        - AWS Lambda
        - AWS S3
        - AWS DynamoDB
docs/4-cloud-computing/4.2.6-ecs.md:
  category: Cloud Computing
  estReadingMinutes: 20
  exercises:
    - name: Creating an EKS cluster
      description: Deploy the SockShop Demo on EKS
      estMinutes: 480
      technologies:
        - AWS
        - AWS EKS
        - Kubernetes
    - name: Adding an autoscaler to your cluster
      description: Adding an autoscaler to your cluster
      estMinutes: 240
      technologies:
        - AWS
        - AWS EKS
        - Kubernetes
    - name: Create a ClusterIP service
      description: Create a ClusterIP service
      estMinutes: 60
      technologies:
        - AWS
        - AWS EKS
        - Kubernetes
    - name: Create a NodePort Service
      description: Create a NodePort Service
      estMinutes: 60
      technologies:
        - AWS
        - AWS EKS
        - Kubernetes
    - name: Create a LoadBalancer Service
      description: Create a LoadBalancer Service
      estMinutes: 30
      technologies:
        - AWS
        - AWS EKS
        - Kubernetes
    - name: Add an Ingress controller and your cluster
      description: Add an Ingress controller and your cluster
      estMinutes: 60
      technologies:
        - AWS
        - AWS EKS
        - Kubernetes
docs/4-cloud-computing/4.3.1-storage-accounts.md:
  category: Cloud Computing
  estReadingMinutes: 10
  exercises:
    - name: Static website on Azure Blob Storage
      description: >-
        Create a basic Angular application and deploy it to an Azure Blob
        Storage with an Azure CDN.
      estMinutes: 240
      technologies:
        - Azure
        - Azure Blob Storage
        - Azure CDN
        - Angular
docs/4-cloud-computing/4.3.2-virtual-machines.md:
  category: Cloud Computing
  estReadingMinutes: 10
  exercises:
    - name: Create Azure VM with NGINX via cloud-init
      description: >-
        Create an Azure VM and configure it as an NGINX web server via
        cloud-init file.
      estMinutes: 360
      technologies:
        - Azure
        - Azure VM
        - NGINX
        - cloud-init
docs/4-cloud-computing/4.3.3-vmss.md:
  category: Cloud Computing
  estReadingMinutes: 15
  exercises:
    - name: Create VMSS and serve content from Azure Storage Account
      description: >-
        Create a VMSS and serve content from an Azure Storage Account. Do this
        via the cli, deploying a simple node web app and provision the VM's with
        cloud-init.
      estMinutes: 330
      technologies:
        - Azure
        - Azure VMSS
        - Azure Storage Account
        - Node.js
        - cloud-init
docs/4-cloud-computing/4.3.4-az-packer.md:
  category: Cloud Computing
  estReadingMinutes: 5
  exercises:
    - name: Create Shared Image Gallery with custom Azure VM image
      description: >-
        Create a Shared Image Gallery and put a custom Azure VM image in it.
        Then redo the exercise in 4.3.2 with the custom image.
      estMinutes: 360
      technologies:
        - Azure
        - Packer
        - Shared Image Gallery
        - Azure VM
docs/4-cloud-computing/4.3.5-aci.md:
  category: Cloud Computing
  estReadingMinutes: 10
  exercises:
    - name: 'Deploy Node app using Docker, ACR, and ACI'
      description: >-
        Create a docker image for your Node application. Push your image into
        ACR. Then deploy your image via ACI.
      estMinutes: 360
      technologies:
        - Azure
        - Azure Container Instances (ACI)
        - Azure Container Registry (ACR)
        - Docker
        - Node.js
docs/4-cloud-computing/4.3.6-aks.md:
  category: Cloud Computing
  estReadingMinutes: 10
  exercises:
    - name: Deploy Node app to AKS using ACR image
      description: >-
        Create an AKS cluster and deploy the Node application via the image
        uploaded to ACR made in the previous section.
      estMinutes: 240
      technologies:
        - Azure
        - Azure Kubernetes Service (AKS)
        - Azure Container Registry (ACR)
        - Node.js
docs/4-cloud-computing/4.3.7-app-service.md:
  category: Cloud Computing
  estReadingMinutes: 10
  exercises:
    - name: Deploy Simple Web Application to App Service
      description: Create A Web App and Scale and Monitor
      estMinutes: 240
      technologies:
        - Azure
        - Azure App Service
        - Azure CLI
docs/5-software-development-practices/5.1-overview.md:
  category: Agile Development
  estReadingMinutes: 90
docs/5-software-development-practices/5.2-jira.md:
  category: Agile Development
  estReadingMinutes: 30
docs/5-software-development-practices/5.3.1-branching-merging.md:
  category: Version Control
  estReadingMinutes: 15
docs/5-software-development-practices/5.3.2-git.md:
  category: Version Control
  estReadingMinutes: 25
  exercises:
    - name: Git Basics
      description: Learn the basics of Git.
      estMinutes: 30
      technologies:
        - Git
    - name: Branching and Merging
      description: Practice branching and merging with Git.
      estMinutes: 30
      technologies:
        - Git
    - name: Merge Conflicts
      description: Learn how to resolve merge conflicts in Git.
      estMinutes: 30
      technologies:
        - Git
    - name: Removing Secrets
      description: Learn how to remove secrets from Git history.
      estMinutes: 30
      technologies:
        - Git
docs/5-software-development-practices/5.3.3-github.md:
  category: Version Control
  estReadingMinutes: 25
  exercises:
    - name: Fork and Merge
      description: Practice forking and merging on GitHub
      estMinutes: 30
      technologies:
        - Git
        - GitHub
docs/5-software-development-practices/5.4-pairprogramming.md:
  category: Agile Development
  estReadingMinutes: 20
  exercises:
    - name: Pair Programing
      description: >-
        Using 'Live Share' or some equivillant try pair programming a 'Hello
        World' app in the language of your choice
      estMinutes: 30
      technologies:
        - VSCode
docs/5-software-development-practices/5.5.1-unit-testing.md:
  category: Software Quality
  estReadingMinutes: 20
  exercises:
    - name: Solve a problem in Go with TDD
      description: Solve a given problem in Go using test-driven development (TDD).
      estMinutes: 120
      technologies:
        - Go
        - TDD
docs/5-software-development-practices/5.5.2-functional-testing.md:
  category: Software Quality
  estReadingMinutes: 20
  exercises:
    - name: Create functional tests with Selenium in Python
      description: Create functional tests for the bootcamp using Selenium in Python.
      estMinutes: 120
      technologies:
        - Selenium
        - Python
docs/5-software-development-practices/5.5.3-code-styling.md:
  category: Software Quality
  estReadingMinutes: 30
docs/5-software-development-practices/5.5.4-code-coverage.md:
  category: Software Quality
  estReadingMinutes: 20
  exercises:
    - name: Achieve 100% code coverage
      description: >-
        Install node dependencies for code coverage (jest) and get 100% code
        coverage for a given module and tests.
      estMinutes: 60
      technologies:
        - Node.js
        - Jest
docs/5-software-development-practices/5.5.5-test-automation.md:
  category: Software Quality
  estReadingMinutes: 5
  exercises:
    - name: Create a GitHub Action to test a Go project
      description: Create a GitHub Action that will run Unit Tests when a change is pushed
      estMinutes: 180
      technologies:
        - GitHub Actions
        - Go
docs/5-software-development-practices/5.5.6-sonarqube.md:
  category: Software Quality
  estReadingMinutes: 10
  exercises:
    - name: Setup SonarQube and GitHub Integration
      description: >-
        Create a SonarQube server and add GitHub action to run SonarQube in our
        build pipeline.
      estMinutes: 180
      technologies:
        - SonarQube
        - GitHub Actions
docs/5-software-development-practices/5.5.7-code-review.md:
  category: Software Quality
  estReadingMinutes: 10
docs/5-software-development-practices/5.6-hello-devops.md:
  category: Agile Development
  estReadingMinutes: 5
  exercises:
    - name: Build an application
      description: >-
        Using what you have leanred thus far create a production ready
        application
      estMinutes: 3000
docs/6-release-management/6.1-versioning.md:
  category: Version Control
  estReadingMinutes: 5
  exercises:
    - name: Docker Image Versioning
      description: >-
        Build a few docker images and play with tagging them with semantic
        versioning.
      estMinutes: 30
      technologies:
        - Docker
docs/6-release-management/6.2.1-maven.md:
  category: CI/CD
  estReadingMinutes: 20
  exercises:
    - name: Maven Web App Creation
      description: >-
        Create a skeleton web application using Maven, add a plugin to help with
        local development, update the version number and create a release.
      estMinutes: 60
      technologies:
        - Maven
docs/6-release-management/6.2.2-maven-integration.md:
  category: CI/CD
  estReadingMinutes: 30
  exercises:
    - name: Maven Integration
      description: >-
        Get an introduction into how Maven interacts with Nexus and how to use
        Maven in GitHub Actions. Fork several projects, use GitHub Actions to
        create GitHub workflow jobs that build these projects, deploy artifacts
        to Nexus, set up jobs to build on commit, make changes and observe the
        results.
      estMinutes: 240
      technologies:
        - Maven
        - GitHub Actions
        - Nexus OSS
docs/6-release-management/6.2.3-make.md:
  category: CI/CD
  estReadingMinutes: 20
  exercises:
    - name: Makefile Exploration
      description: >-
        Explore the Makefile of a complex project (e.g., Rode) to understand its
        structure and functioning. No code writing is required for this
        exercise, but you should spend time studying and understanding the
        Makefile.
      estMinutes: 60
      technologies:
        - Make
docs/6-release-management/6.2.4-npm.md:
  category: CI/CD
  estReadingMinutes: 15
  exercises:
    - name: npm Practice
      description: >-
        Install and run the Dromedary app. Determine and run the appropriate
        command to test the app.
      estMinutes: 45
      technologies:
        - npm
        - Node.js
        - Java
docs/6-release-management/6.2.5-go-releaser.md:
  category: CI/CD
  estReadingMinutes: 5
  exercises:
    - name: Go Releaser Exercise
      description: >-
        Fork and clone an open source Go project, set up a workflow that will
        deploy a release with Go Releaser.
      estMinutes: 240
      technologies:
        - Go
        - Go Releaser
        - GitHub
        - GitHub Actions
docs/6-release-management/6.3.1-docker.md:
  category: Container Orchestration
  estReadingMinutes: 10
  exercises:
    - name: Dockerhub Exercise
      description: >-
        Create a Dockerhub account, create repositories, clone DevOps Knowledge
        Share repositories, build container images, push them to Dockerhub,
        create a Docker Compose file, and create a GitHub Actions Workflow.
      estMinutes: 360
      technologies:
        - Docker
        - Dockerhub
        - GitHub
        - GitHub Actions
docs/6-release-management/6.3.2-helm.md:
  category: Container Orchestration
  estReadingMinutes: 15
  exercises:
    - name: Helm Exercise 1
      description: >-
        Install Helm and create, install, and update a basic chart with a
        ConfigMap Kubernetes resource.
      estMinutes: 180
      technologies:
        - Helm
        - Kubernetes
    - name: Helm Exercise 2
      description: Modify an existing Helm chart to deploy the DevOps Knowledge Share API.
      estMinutes: 120
      technologies:
        - Helm
        - Kubernetes
        - Docker
        - GitHub
    - name: Helm Exercise 3
      description: >-
        Add a Kubernetes deployment and service to our Helm chart to deploy the
        DKS frontend application.
      estMinutes: 180
      technologies:
        - Helm
        - Kubernetes
        - Docker
    - name: Helm Exercise 4
      description: >-
        Create another Helm chart using the Helm Create command and configure it
        to deploy a GitHub self-hosted runner.
      estMinutes: 120
      technologies:
        - Helm
        - Kubernetes
        - Docker
        - GitHub
docs/7-infrastructure-configuration-management/7.1.1-terraform-getting-started.md:
  category: Infrastructure as Code
  estReadingMinutes: 45
  exercises:
    - name: Getting Started with Terraform
      description: >-
        Run through Hashicorp's tutorials to get started with either AWS or
        Azure. Share your experiences and learnings with your team.
      estMinutes: 60
      technologies:
        - Terraform
        - AWS
        - Azure
docs/7-infrastructure-configuration-management/7.1.2-terraform-backends.md:
  category: Infrastructure as Code
  estReadingMinutes: 20
  exercises:
    - name: Sharing Terraform Workspaces
      description: >-
        Learn how to share a Terraform workspace with your teammates and
        understand the role of `terraform.lock.hcl`.
      estMinutes: 60
      technologies:
        - Terraform
        - Terraform Cloud
        - GitHub
    - name: Cloud Native Backends
      description: >-
        Transition from using Terraform Cloud to using cloud native storage
        solutions for storing Terraform state.
      estMinutes: 120
      technologies:
        - Terraform
        - AWS S3
        - Azure Resource Manager
    - name: Terraform CI/CD Automation
      description: >-
        Create a CI/CD pipeline that enforces the main branch as the source of
        truth for the state of the Terraform.
      estMinutes: 420
      technologies:
        - Terraform
        - GitHub Actions
docs/7-infrastructure-configuration-management/7.1.3-terraform-modules.md:
  category: Infrastructure as Code
  estReadingMinutes: 15
  exercises:
    - name: Registry Modules
      description: >-
        Learn how to use registry modules to create an EC2 instance and VPC in
        AWS, or add an EC2 instance to an existing VPC.
      estMinutes: 90
      technologies:
        - Terraform
        - AWS EC2
        - AWS VPC
    - name: Custom Modules/Local Modules
      description: Create and use a local module for an S3 bucket in AWS.
      estMinutes: 75
      technologies:
        - Terraform
        - AWS S3
docs/7-infrastructure-configuration-management/7.1.4-terraform-providers.md:
  category: Infrastructure as Code
  estReadingMinutes: 20
  exercises:
    - name: Provider Boilerplate
      description: Set up the boilerplate for a Terraform provider and test it locally.
      estMinutes: 120
      technologies:
        - Terraform
        - Go
    - name: Implementing the provider client
      description: Implement the Terraform provider client to interact with a custom API.
      estMinutes: 240
      technologies:
        - Terraform
        - Go
    - name: Implementing Engineer resource and datasource
      description: Implement the CRUD operations for the Engineer resource and datasource.
      estMinutes: 300
      technologies:
        - Terraform
        - Go
    - name: Testing
      description: Write comprehensive tests for the Engineer resource and datasource.
      estMinutes: 120
      technologies:
        - Terraform
        - Go
    - name: Implementing Dev or Ops resource and datasource
      description: >-
        Implement the CRUD operations for the Dev or Ops resources and
        datasources.
      estMinutes: 300
      technologies:
        - Terraform
        - Go
docs/7-infrastructure-configuration-management/7.2-ansible.md:
  category: Infrastructure as Code
  estReadingMinutes: 15
  exercises:
    - name: Vagrant and Ansible
      description: >-
        Provision a virtual machine and install a GitHub self-hosted runner
        using Ansible as a provisioner in Vagrant.
      estMinutes: 300
      technologies:
        - Ansible
        - Vagrant
        - GitHub self-hosted runner
    - name: Idempotency
      description: >-
        Provision a virtual machine and install a GitHub self-hosted runner
        using Ansible as a provisioner in Vagrant while maintaining idempotency.
      estMinutes: 300
      technologies:
        - Ansible
        - Vagrant
        - GitHub self-hosted runner
    - name: Ansible and AWS EC2
      description: >-
        Provision an AWS EC2 instance and install a GitHub self-hosted runner
        using Ansible.
      estMinutes: 300
      technologies:
        - Ansible
        - AWS EC2
        - GitHub self-hosted runner
    - name: Terraform and Ansible
      description: >-
        Provision an EC2 instance using Terraform and install a GitHub
        self-hosted runner with Ansible.
      estMinutes: 360
      technologies:
        - Terraform
        - Ansible
        - AWS EC2
        - GitHub self-hosted runner
docs/8-kubernetes-container-orchestration/8.1-kubectl-ref.md:
  category: Container Orchestration
  estReadingMinutes: 120
docs/8-kubernetes-container-orchestration/8.2-volumes.md:
  category: Container Orchestration
  estReadingMinutes: 10
  exercises:
    - name: Creating Persistent Volumes and Persistent Volume Claims
      description: >-
        Create a simple Persistent Volume (PV) and Persistent Volume Claim (PVC)
        in Kubernetes, understand the lifecycle of PVs and PVCs, and explore how
        to utilize them in a pod.
      estMinutes: 120
      technologies:
        - Kubernetes
    - name: Dynamic Provisioning with Storage Classes
      description: >-
        Learn about dynamic provisioning of Persistent Volumes (PVs) using
        Storage Classes, create a StorageClass object, provision a PVC
        dynamically, and deploy Jenkins in the cluster with persistent data.
      estMinutes: 360
      technologies:
        - Kubernetes
        - Jenkins
docs/8-kubernetes-container-orchestration/8.3-probes.md:
  category: Container Orchestration
  estReadingMinutes: 10
  exercises:
    - name: Setup
      description: >-
        Create a service of type NodePort and a deployment for nginx in the
        default namespace using Docker Desktop.
      estMinutes: 25
      technologies:
        - Docker
        - Kubernetes
    - name: Startup Probe Config
      description: Add a startup probe to the nginx deployment and check the logs.
      estMinutes: 45
      technologies:
        - Kubernetes
    - name: Readiness Probe Config
      description: Add a readiness probe to the nginx deployment and check the logs.
      estMinutes: 45
      technologies:
        - Kubernetes
    - name: Liveness Probe Config
      description: >-
        Add a liveness probe to the nginx deployment, configure a hostPath
        volume and volumeMount, and check the logs.
      estMinutes: 45
      technologies:
        - Kubernetes
docs/8-kubernetes-container-orchestration/8.4-rbac.md:
  category: Container Orchestration
  estReadingMinutes: 15
  exercises:
    - name: Grant New Permissions to a ServiceAccount
      description: >-
        Create a namespace for Jenkins, install Jenkins using helm, discover new
        roles, create credentials using a Kubernetes secret, and setup Jenkins.
      estMinutes: 180
      technologies:
        - Docker
        - Kubernetes
        - Helm
        - Jenkins
    - name: Verifying RBAC Permissions
      description: >-
        Create a new namespace, service account, cluster role, and cluster role
        binding, and verify the permissions.
      estMinutes: 120
      technologies:
        - Docker
        - Kubernetes
docs/8-kubernetes-container-orchestration/8.5-hpas.md:
  category: Container Orchestration
  estReadingMinutes: 15
  exercises:
    - name: Create an HPA
      description: >-
        Install Metrics Server, apply the deployment and service for a
        CPU-intensive PHP image, and create an HPA that will scale the PHP
        deployment based on CPU usage.
      estMinutes: 120
      technologies:
        - Docker
        - Kubernetes
        - Metrics Server
    - name: Increase Server Load
      description: Increase the PHP server load and watch how the CPU load scales.
      estMinutes: 30
      technologies:
        - Docker
        - Kubernetes
    - name: Decrease Server Load
      description: Decrease the server load and watch how the CPU load scales down.
      estMinutes: 30
      technologies:
        - Docker
        - Kubernetes
    - name: HPAs with Multiple Metrics
      description: >-
        Configure the HPA to use multiple metrics, add memory as a resource in
        the PHP-Apache deployment, update the HPA, and verify its functionality.
      estMinutes: 180
      technologies:
        - Docker
        - Kubernetes
docs/8-kubernetes-container-orchestration/8.6-webhooks.md:
  category: Container Orchestration
  estReadingMinutes: 15
  exercises:
    - name: Setup
      description: >-
        Set up the environment for admission webhooks by deploying a KIND
        cluster with Admission Controller enabled, installing cert-manager, and
        creating a validation namespace, root CA, and self-signed certificate.
      estMinutes: 60
      technologies:
        - Kubernetes
        - KIND
        - cert-manager
    - name: Validating Webhooks
      description: >-
        Configure a validating webhook for pod creation and test it using the
        given criteria.
      estMinutes: 90
      technologies:
        - Kubernetes
        - Python
    - name: Mutating Webhooks
      description: >-
        Configure a mutating webhook for pod creation and test it using the
        given criteria.
      estMinutes: 180
      technologies:
        - Kubernetes
        - Python
docs/8-kubernetes-container-orchestration/8.6.1-validating-admission-policy.md:
  category: Container Orchestration
  estReadingMinutes: 35
  exercises:
    - name: Basic ValidatingAdmissionPolicy
      description: >-
        Create a ValidatingAdmissionPolicy to replicate the behavior of a
        Validating Webhook, rejecting pods in a specific namespace based on
        image.
      estMinutes: 60
      technologies:
        - Kubernetes
        - ValidatingAdmissionPolicy
        - CEL
    - name: Dynamic ValidatingAdmissionPolicy with Params
      description: >-
        Create a more complex ValidatingAdmissionPolicy using paramKind and
        paramRef to implement dynamic, namespace-specific validation for
        deployment replica counts.
      estMinutes: 90
      technologies:
        - Kubernetes
        - ValidatingAdmissionPolicy
        - CEL
        - Custom Resources
    - name: Warning ValidatingAdmissionPolicy
      description: >-
        Implement a ValidatingAdmissionPolicy that warns developers about an
        upcoming required label on Deployments.
      estMinutes: 40
      technologies:
        - Kubernetes
        - ValidatingAdmissionPolicy
        - CEL
docs/8-kubernetes-container-orchestration/8.7.1-kustomize.md:
  category: Container Orchestration
  estReadingMinutes: 20
  exercises:
    - name: General Use-Case
      description: >-
        Organize a few manifest files and use Kustomize to build them all at
        once. Learn how to inspect build outputs and apply manifests with
        Kustomize.
      estMinutes: 15
      technologies:
        - Kubernetes
        - Kustomize
    - name: Simple Modifications
      description: >-
        Learn to use Kustomize's "namespace", "commonLabels", and "images"
        operators.
      estMinutes: 30
      technologies:
        - Kubernetes
        - Kustomize
    - name: Patches
      description: >-
        Learn to write Kustomize pathes, and the difference between
        StrategicMergePatch and Json6902 patches.
      estMinutes: 30
      technologies:
        - Kubernetes
        - Kustomize
    - name: Secret Management
      description: >-
        Learn to use the "secretGenerator" Kustomize operator and create another
        Kustomize patch to include the secret as an environment variable in a
        container.
      estMinutes: 30
      technologies:
        - Kubernetes
        - Kustomize
    - name: Script Embedding
      description: >-
        Modify the Nginx server frontend by mounting an HTML script to the
        container. Use the Kustomize configMapGenerator to create the ConfigMap
        that holds the script.
      estMinutes: 40
      technologies:
        - Kubernetes
        - Kustomize
    - name: Bases and Overlays
      description: >-
        See what a more productionalized Kustomize structure looks like with the
        base/overlays pattern.
      estMinutes: 20
      technologies:
        - Kubernetes
        - Kustomize
docs/8-kubernetes-container-orchestration/8.7.2-helm.md:
  category: Container Orchestration
  estReadingMinutes: 5
  exercises:
    - name: Source a Helm Chart
      description: >-
        Declaratively define a Gitea Helm Chart to be sourced and templated
        locally. Deploy it to a cluster, port-forward to its server and log in.
      estMinutes: 45
      technologies:
        - Kubernetes
        - Helm
        - Kustomize
    - name: Modify the Helm Chart
      description: Use the values file and kustomization.yaml to modify the Helm Chart.
      estMinutes: 30
      technologies:
        - Kubernetes
        - Helm
        - Kustomize
docs/8-kubernetes-container-orchestration/8.8-hello-k8s.md:
  category: Container Orchestration
  estReadingMinutes: 15
  exercises:
    - name: Kubernetes Custom Project
      description: >-
        Create a custom Kubernetes project, utilizing kubebuilder,Kubebuilder to
        create a kubernetes custom resource definition and controller which
        reconciles changes to the custom resource.
      estMinutes: 4800
      technologies:
        - Kubernetes
        - Custom Resources
        - Kubebuilder
docs/9-platform-engineering/9.0-overview.md:
  category: Platform Engineering
  estReadingMinutes: 15
docs/9-platform-engineering/9.1-backstage.md:
  category: Platform Engineering
  estReadingMinutes: 20
  exercises:
    - name: Create a GitHub Organization
      description: >
        This exercise involves creating a GitHub Organization to simulate an
        integrated SCM environment, similar to what you would find in a
        real-world development ecosystem. Each student will create their own
        GitHub Organization following the provided instructions.
      estMinutes: 30
      technologies:
        - GitHub
    - name: Stand up local instance of Backstage
      description: >
        Students will set up a local instance of Backstage by following the
        official Getting Started guide. This exercise covers starting the local
        instance, familiarizing with the UI, and customizing the appearance of
        the Backstage instance including logo and application name changes.
        Extra credit is given for applying a custom theme. The customized
        instance should then be pushed to a repo in the newly created GitHub
        Organization.
      estMinutes: 60
      technologies:
        - Backstage
        - Docker
    - name: Configure Authentication via GitHub
      description: >
        This exercise focuses on configuring authentication for the Backstage
        instance using GitHub. Students will create an OAuth app within their
        GitHub Organization and integrate it with Backstage for authentication
        purposes. This includes not storing secrets in plain text and ensuring
        secure authentication practices. Verification of login functionality
        through GitHub is the final step to confirm successful integration.
      estMinutes: 120
      technologies:
        - Backstage
        - GitHub
docs/9-platform-engineering/9.1.1-software-catalog.md:
  category: Backstage Software Catalog
  estReadingMinutes: 20
  exercises:
    - name: Entity Registration
      description: >
        This exercise instructs students to register an entity to their local
        Backstage instance.  The entity should correspond to a repo belonging to
        a GitHub organization that the student owns.  This exercise will require
        students to configure their Backstage instance to have the permissions
        needed to access their GitHub organization and will help pave the way
        for the following exercise.
      estMinutes: 20
      technologies:
        - Backstage
        - GitHub
    - name: Catalog Ingestion
      description: >
        Students will configure their Backstage instance to automatically
        perform read operations on a given GitHub organization and ingest
        `catalog-info.yaml` files existing in that organization in order to
        automatically register entities.  They will need to configure GitHub as
        a catalog and ensure that their Backstage instance combs their
        organization for the correct file(s) at an appropriate interval.
      estMinutes: 80
      technologies:
        - Backstage
        - GitHub
    - name: Dependency Graphs
      description: >
        Students will fork two interdependent repos to their organization and
        ensure that their Backstage instance recognizes the two repos while also
        displaying the repos' interdependence via the "Relations" section of
        their overviews in the UI.  This requires a thorough understanding of
        the available fields in `catalog-info.yaml` files along with a Backstage
        app's configuration file.  
      estMinutes: 120
      technologies:
        - Backstage
        - GitHub
    - name: OpenAPI Definitions
      description: >
        Here, students are required to provide an OpenAPI specification which
        their Backstage instance can ingest and associate with a definition for
        an API having source code in a repo owned by the student's
        organization.  Students may use a repo that already has an OpenAPI spec
        file or they may generate the necessary spec data from an API.  
      estMinutes: 30
      technologies:
        - Backstage
        - GitHub
docs/9-platform-engineering/9.1.2-techdocs.md:
  category: TechDocs
  estReadingMinutes: 10
  exercises:
    - name: Enable Documentation for an Existing Entity
      description: >
        This exercise instructs students to add the bare minimum amount of files
        needed for their Backstage instance to generate an MkDocs site and
        associate it with an entity in their Software Catalog.  Extra credit is
        offered for studying Backstage's ability to search within TechDocs
        stored in the Catalog -- the basic setup we point students towards in
        this exercise can lead to a search-related bug which is valuable for
        understanding the different ways Backstage can be configured to manage
        TechDocs.
      estMinutes: 40
      technologies:
        - GitHub
        - Backstage
docs/9-platform-engineering/9.1.3-software-templates.md:
  category: Software Templates
  estReadingMinutes: 20
  exercises:
    - name: Create a Simple Template
      description: >
        This exercise involves writing a custom Software Template and
        configuring Backstage to register it as an entity that can be used from
        the UI, and then using the template to publish a new repo in a GitHub
        organization.  This can be achieved by following two separate guides in
        Spotify's official Backstage docs: one for writing the Software
        Template, and the other for providing Backstage with the necessary
        permissions to publish new GitHub repos using the Template.  Some extra
        time is allotted for misc. debugging, since it seems that Backstage is
        in a transitory period and there's no telling whether their guides will
        remain accurate.
      estMinutes: 45
      technologies:
        - Backstage
        - GitHub
    - name: Write a Custom Action
      description: >
        Students are to become acquainted with the Scaffold plugin and extend
        this plugin by writing a custom action which can be used in the custom
        template they wrote in the previous exercise.  Some special instructions
        are provided because the only available official guides are outdated.  
      estMinutes: 60
      technologies:
        - Backstage
        - GitHub
docs/9-platform-engineering/9.1.4-plugins.md:
  category: Backstage Plugins
  estReadingMinutes: 10
  exercises:
    - name: Explore the Plugin Directory
      description: >
        Students receive an introduction to Backstage's plugin directory by
        adding a plugin from the directory to their Backstage instance.  They
        are encouraged to look through the plugin's source code and gain a basic
        understanding of how it works.
      estMinutes: 30
      technologies:
        - Backstage
        - GitHub
    - name: Write a Custom Plugin
      description: >
        Students will create their own Backstage plugin that exists outside of
        Backstage's repo so it can be easily imported into any Backstage
        instance.
      estMinutes: 3000
      technologies:
        - Backstage
        - TypeScript
        - GitHub
---
<!-- DO NOT EDIT ABOVE THIS COMMENT. -->
<!-- MANAGED BY ./husky.sh/front-matter-condenser.js -->

<!-- <canvas id="wordcloud-canvas"></canvas> -->

<center>

  ![DevCloudNinjas Logomark](../img/favicon.svg ':size=150x150 :class=logo :alt= DevCloud Ninjas image')

# DevCloudNinjas' DevOps Bootcamp

</center>

## Introduction

Welcome! You must be here because you're interested in DevOps. Don't worry, we'll get to that in a moment! First, let's briefly go over some details.

"1.0" can be referred to as "Chapter One," while "1.2" can be referred to as "Chapter One, Section Two."

## Target Audience

This DevOps Bootcamp is used as an introduction to DevOps for DevCloudNinjas' apprentices. Therefore, there are deliverables at the end of each section and knowledge checks sprinkled throughout that help guide the apprentices' training. However, anyone can go through the DevOps Bootcamp. Feel free to ignore the deliverables, knowledge checks, etc. This bootcamp also assumes the bootcamper is using a Mac for the deliverables.

## Disclaimer

This bootcamp alone will by no means make anyone an expert on DevOps; that's where real, in-the-field experience engineering and shadowing come in. However, this bootcamp is a great start for anyone entering the world of DevOps! It is recommended that anyone going through this bootcamp have a mentor to fill in the gaps of information and answer questions, as well. Also, many of the exercises proposed in this bootcamp have no solution listed. This is because it is up to the bootcamper to come up with the solution on their own. So, if you're wondering where a solution to an exercise is - there is likely none; that's up to you!

## Learning Goals

1. Introduction to DevOps
2. GitHub
3. Virtual Machines and Containers
4. Cloud Computing
5. Development Practices
6. Release Management
7. Infrastructure and Configuration
8. Kubernetes

<canvas id="technology-word-cloud"></canvas>

<canvas id="category-doughnut-canvas"></canvas>

## Expectations

1. Share what you learn. Knowledge is best retained when you can teach it back yourself.
2. If you're participating in the bootcamp with others, lift them up instead of speeding past them.
3. Your learning should be in a demonstrable state at any given time.
4. Slow and steady wins the race. If you don't fully understand something, speak up for help and spend more time on it.
5. Be transparent in your progress.
6. Have fun!

> "It's better to over communicate than to under communicate."

## Deliverable and Knowledge Check Format

**Deliverables**

If you are an apprentice (or if you just want to add to your learning), here's a little insight on the deliverables the bootcamp will provide. At the end of each section, you will typically encounter a bulleted list of deliverables. They will usually be structured to get you thinking/reflecting/researching key points that the section covered.

**Knowledge Checks**

As mentioned before, you'll also find small knowledge checks sprinkled throughout the bootcamp. Don't worry, they aren't graded and scores aren't tracked, so there's zero pressure when it comes to them. That being said, they are very valuable for learning, so it would be wise to take the time to not only get the correct answers on them, but to really understand *why* those are the correct answers.

Here's a sample knowledge check to show you how they'll behave:

<div class="quizdown">
    <div id="landing-page-quiz.js" ></div>
</div>

## Contributing

This bootcamp was adapted from an apprentice training program, and some mistakes may have slipped through the cracks. If you see any errors, outdated methods, or citation errors please submit a pull request.

## Local Development

Below are a number of ways to develop locally, choose whichever you are most comfortable with.

### Using Package.json **Recommended**

Install Docsify locally (in current directory)

1. Run `npm install`
2. Run `npm start`
3. Open <http://localhost:3000>

### Global Install

Install Docsify Globally in your system

1. Install [docsify](https://docsify.js.org/#/quickstart)
2. Navigate to local library of onboarding
3. Run `docsify serve .`
4. Open <http://localhost:3000>

### Docker

Use Docker to build and serve the content, but remember to rebuild the Docker image to review changes

#### Build and Run Docker Container

1. Execute `docker build . -t devops-bootcamp` from the project's root directory to generate a container image
2. Run `docker run -d -p 3000:3000 --name devops-bootcamp devops-bootcamp` to run a detached Docker container
3. Open <http://localhost:3000>

#### Docker Compose

1. Run `docker compose up -d`
2. Open <http://localhost:3000>
3. To stop the container, run `docker compose down`

### More Information on Contributing

- Images should be placed under the root `img` folder and referred to using HTML `<img>` tags
- H3 header (`###`) should be the default header within a page
- H2 header (`##`) will appear in the navigation as the page's table of contents
- To add a new section, add a new file to `docs` such as `x.x-new-section.md`, and then reference it in `docs/_sidebar.md`.

[Contributors](contributors.md)

![classroom image](../img/class_light.svg ':size=100x100 :class=light-mode-icon :alt= classroom image; light mode')
![classroom image](../img/class_dark.svg ':size=100x100 :class=dark-mode-icon :alt= classroom image; dark mode')
