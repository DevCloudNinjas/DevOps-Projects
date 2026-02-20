# AWS CLOUD SOLUTION FOR 2 COMPANY WEBSITES USING A REVERSE PROXY TECHNOLOGY
In this project, we will build a secure infrastructure inside AWS VPC (Virtual Private Cloud) network for a fictitious company (Choose an interesting name for it) that uses WordPress CMS for its main business website, and a Tooling Website (https://github.com/<your-name>/tooling) for their DevOps team. As part of the company’s desire for improved security and performance, a decision has been made to use a reverse proxy technology from NGINX to achieve this.

`Cost, Security, and Scalability are the major requirements for this project. Hence, implementing the architecture designed below, ensure that infrastructure for both websites, WordPress and Tooling, is resilient to Web Server’s failures, can accomodate to increased traffic and, at the same time, has reasonable cost.`

## Project Design Architecture Diagram
#

![](./images/architecture%20diagram.PNG)

#

## Starting Off AWS Project

1. Properly configure your AWS account and Organization Unit [Watch How To Do This Here](https://youtu.be/9PQYCc_20-Q)
   
- Create an AWS Master account. (Also known as Root Account)
- Within the Root account, create a sub-account and name it DevOps. (You will need another email address to complete this)
- Within the Root account, create an AWS Organization Unit (OU). Name it Dev. (We will launch Dev resources in there)
Move the DevOps account into the Dev OU.
- Login to the newly created AWS account using the new email address.
- Create a free domain name for your fictitious company at Freenom domain registrar here.

- Create a hosted zone in AWS, and map it to your free domain from Freenom. [Watch how to do that here](https://youtu.be/IjcHp94Hq8A)

![](./Images/domain%20creation.PNG)

**NOTE** : As you proceed with configuration, ensure that all resources are appropriately tagged, for example:

- Project: <Give your project a name>
- Environment: <dev>
- Automated: <No> (If you create a recource using an automation tool, it would be <Yes>)
#

## Setting Up Infrastucture

1. Create a VPC

![](./Images/create%20a%20new%20VPC.PNG)

2. Create subnets as shown in the architecture

![](./Images/private%20subnet%20created.PNG)

3. Create a route table and associate it with public subnets



4. Create a route table and associate it with private subnets
   

5. Create an Internet Gateway

![](./Images/create%20TCS-igw.PNG)

1. Edit a route in public route table, and associate it with the Internet Gateway. (This is what allows a public subnet to be accisble from the Internet)
   
![](./img/6.pub-routes.png)

7. Create an Elastic IP

![](./img/7.nat_eip.png)

8. Create a Nat Gateway and assign one of the Elastic IPs (*The other 2 will be used by Bastion hosts)
   
![](./Images/create%20NAT%20gateway.PNG)

9. Create a Security Group for:

- Nginx Servers: Access to Nginx should only be allowed from a Application Load balancer (ALB). At this point, we have not created a load balancer, therefore we will update the rules later. For now, just create it and put some dummy records as a place holder.
  
- Bastion Servers: Access to the Bastion servers should be allowed only from workstations that need to SSH into the bastion servers. Hence, you can use your workstation public IP address. To get this information, simply go to your terminal and type curl www.canhazip.com
  
- Application Load Balancer: ALB will be available from the Internet
Webservers: Access to Webservers should only be allowed from the Nginx servers. Since we do not have the servers created yet, just put some dummy records as a place holder, we will update it later.

- Data Layer: Access to the Data layer, which is comprised of Amazon Relational Database Service (RDS) and Amazon Elastic File System (EFS) must be carefully desinged – only webservers should be able to connect to RDS, while Nginx and Webservers will have access to EFS Mountpoint.

![](./Images/create%20bastion%20SG.PNG)
#

## Proceed With Compute Resources
#

You will need to set up and configure compute resources inside your VPC. The recources related to compute are:

- EC2 Instances
- Launch Templates
- Target Groups
- Autoscaling Groups
- TLS Certificates
- Application Load Balancers (ALB)
  
### TLS Certificates From Amazon Certificate Manager (ACM)
#

You will need TLS certificates to handle secured connectivity to your Application Load Balancers (ALB).

- Navigate to AWS ACM
- Request a public wildcard certificate for the domain name you registered in Freenom
- Use DNS to validate the domain name
- Tag the resource
- Bind the ACM to the route53 hosted zone created earlier


#

### Setup EFS
#
Amazon Elastic File System (Amazon EFS) provides a simple, scalable, fully managed elastic Network File System (NFS) for use with AWS Cloud services and on-premises resources. In this project, we will utulize EFS service and mount filesystems on both Nginx and Webservers to store data.

- Create an EFS filesystem
- Create an EFS mount target per AZ in the VPC, associate it with both subnets dedicated for data layer
- Associate the Security groups created earlier for data layer.
Create an EFS access point. (Give it a name and leave all other settings as default)

![](./Images/creating%20EFS.PNG)

- On the EFS setup, create two access points for both `tooling` and `wordpress` applications
  
![](./Images/access%20points%20for%20tooling%20and%20wordpress.PNG)
#

## Setup RDS
#

**Pre-requisite:** Create a KMS key from Key Management Service (KMS) to be used to encrypt the database instance.

`Amazon Relational Database Service (Amazon RDS) is a managed distributed relational database service by Amazon Web Services. This web service running in the cloud designed to simplify setup, operations, maintenans & scaling of relational databases. Without RDS, Database Administrators (DBA) have more work to do, due to RDS, some DBAs have become jobless`

To ensure that your databases are highly available and also have failover support in case one availability zone fails, we will configure a multi-AZ set up of RDS MySQL database instance. In our case, since we are only using 2 AZs, we can only failover to one, but the same concept applies to 3 Availability Zones. We will not consider possible failure of the whole Region, but for this AWS also has a solution – this is a more advanced concept that will be discussed in following projects.

To configure RDS, follow steps below:

- Create a subnet group and add 2 private subnets (data Layer)
- Create an RDS Instance for mysql 8.*.*

![](./Images/creating%20database.PNG)

- To satisfy our architectural diagram, you will need to select either Dev/Test or Production Sample Template. But to minimize AWS cost, you can select the Do not create a standby instance option under Availability & durability sample template (The production template will enable Multi-AZ deployment)

- Configure other settings accordingly (For test purposes, most of the default settings are good to go). In the real world, you will need to size the database appropriately. You will need to get some information about the usage. If it is a highly transactional database that grows at 10GB weekly, you must bear that in mind while configuring the initial storage allocation, storage autoscaling, and maximum storage threshold.

- Configure VPC and security (ensure the database is not available from the Internet)
- Configure backups and retention
- Encrypt the database using the KMS key created earlier

![](./Images/KMS%20created.PNG)

- Enable CloudWatch monitoring and export Error and Slow Query logs (for production, also include Audit)
  #
## Creating AMIs for Launch Templates

- To create Launch templates and target groups later on, we will need to setup AMI containing configurations to be done on this respective servers.

#
## **[Configurations for this servers can be found on this repository](https://github.com/Micah-Shallom/RCR-Project-Configuration.git)**
#

![](./Images/all%20redhat%20servers.PNG)
![](./Images/create%20tcs-webserver-ami.PNG)


- Prepare Launch Template For Nginx,tooling, WebServers and Bastion (One Per Subnet)
  
- Make use of the AMI to set up a launch template

- Ensure the Instances are launched into their respective subnet; The bastion and Nginx template should be in the public subnets and then tooling and webservers be on the private subnet
  
- Assign appropriate security group

- Configure Userdata to update yum package repository and install nginx

- Configure Target Groups

![](./Images/creating%20target%20groups.PNG)

- Select Instances as the target type
  
- Ensure the protocol HTTPS on secure TLS port 443

- Ensure that the health check path is /healthstatus

- Register Nginx Instances as targets

- Ensure that health check passes for the target group

- Configure Autoscaling For Nginx

- Select the right launch template

- Select the VPC

- Select both public subnets

- Enable Application Load Balancer for the AutoScalingGroup (ASG)

- Select the target group you created before

- Ensure that you have health checks for both EC2 and ALB

The desired capacity is 2

Minimum capacity is 2

Maximum capacity is 4

Set scale out if CPU utilization reaches 90%
Ensure there is an SNS topic to send scaling notifications
#


## CONFIGURE APPLICATION LOAD BALANCER (ALB)
#

Application Load Balancer To Route Traffic To NGINX
Nginx EC2 Instances will have configurations that accepts incoming traffic only from Load Balancers. No request should go directly to Nginx servers. With this kind of setup, we will benefit from intelligent routing of requests from the ALB to Nginx servers across the 2 Availability Zones. We will also be able to offload SSL/TLS certificates on the ALB instead of Nginx. Therefore, Nginx will be able to perform faster since it will not require extra compute resources to valifate certificates for every request.

### Create an Internet facing ALB

- Ensure that it listens on HTTPS protocol (TCP port 443)

- Ensure the ALB is created within the appropriate VPC | AZ | Subnets

- Choose the Certificate from ACM

- Select Security Group

- Select Nginx Instances as the target group

- Application Load Balancer To Route Traffic To Web Servers

- Since the webservers are configured for auto-scaling, there is going to be a problem if servers get dynamically scalled out or in. Nginx will not know about the new IP addresses, or the ones that get removed. Hence, Nginx will not know where to direct the traffic.

- To solve this problem, we must use a load balancer. But this time, it will be an internal load balancer. Not Internet facing since the webservers are within a private subnet, and we do not want direct access to them.

### Create an Internal ALB

- Ensure that it listens on HTTPS protocol (TCP port 443)

- Ensure the ALB is created within the appropriate VPC | AZ | Subnets
- Choose the Certificate from ACM

- Select Security Group

- Select webserver Instances as the target group

- Ensure that health check passes for the target group

![](./Images/loadbalancers.PNG)

**NOTE:** This process must be repeated for both WordPress and Tooling websites.

- Route traffic coming from the nginx server into the internal loadbalancer by sending traffic to the respective target group based on the url being requested by the user.
  
![](./Images/adding%20rules.PNG)


## Creating Databases for Wordpress and Tooling Sites on MySQL rds

- Login into the MySQL RDS from the bastion server

- Create databases 

![](./Images/creating%20database%20tooling%20and%20wordpress.PNG)  


## Adding URL EndPoints to Route53 for Wordpress and Tooling Access
![](./Images/route%2053%20records.PNG)
![](./Images/tooling%20webpage.PNG)
