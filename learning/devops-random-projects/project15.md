# AWS CLOUD SOLUTION FOR 2 COMPANY WEBSITES USING A REVERSE PROXY TECHNOLOGY
## INTRODUCTION

This project demostrates how a secure infrastructure inside AWS VPC (Virtual Private Cloud) network is built for a particular company, who uses WordPress CMS for its main business website, and a Tooling Website for their DevOps team. As part of the company’s desire for improved security and performance, a decision has been made to use a reverse proxy technology from NGINX to achieve this. The infrastructure will look like following diagram:
![](./img/project15/tooling_project_15.png)

The following outlines the steps taken:

## STEP 1: Setting Up a Sub-account And Creating A Hosted Zone
- Creating a sub-account 'DevOps' from my AWS master account in the AWS Organisation Unit console 

![](./img/project15/12-adding%20new%20aws%20account.png)

- Creating an AWS Organization Unit (OU) 'Dev' within the Root account(Dev resources will be launched in there)

![](./img/project15/14-creating%20new%20aws%20organisation.png)

- Moving the DevOps account into the Dev OU

![](./img/project15/15-moving%20devops%20account%20to%20dev.png)

- Logging in to the newly created AWS account

![](./img/project15/16-switching%20to%20the%20new%20aws%20ou.png)

- Creating a hosted zone in the Route 53 console and mapping it to the domain name acquired from freenom.

![](./img/project15/17-creating%20hosted%20zone.png)
![](./img/project15/18-hosted%20zone%20created.png)

## STEP 2: Setting Up a Virtual Private Network (VPC)

- Creating a VPC from the VPC console

![](./img/project15/20-creating%20vpc.png)

- Creating subnets for the public and private resources

![](./img/project15/21-creating%20subnets.png)
![](./img/project15/21-creating%20subnets-2.png)
![](./img/project15/21-creating%20subnets-3.png)
![](./img/project15/21-creating%20subnets-4.png)
![](./img/project15/21-creating%20subnets-5.png)
![](./img/project15/21-creating%20subnets-6.png)
![](./img/project15/22-subnets%20created.png)

- Creating a route table and associating it with public subnets

![](./img/project15/25-creating%20rtb.png)
![](./img/project15/27-associating%20routes%20to%20public.png)

- Creating another route table and associating it with private subnets

![](./img/project15/35-creating%20rtb%20for%20private.png)
![](./img/project15/36-associting%20route%20with%20private.png)

- Creating an Internet Gateway

![](./img/project15/23-creating%20igw.png)

- Attaching the Internet Gateway to the VPC

![](./img/project15/24-attaching%20igw%20to%20vpc.png) 

- Editing a route in public route table, and associating it with the Internet Gateway. (This is what allows a public subnet to be accessible from the Internet).

![](./img/project15/26-creating%20routes%20to%20point%20to%20igw.png)

- Creating 3 Elastic IPs

![](./img/project15/39-creating%20elastic%20ip.png)
![](./img/project15/40-elastic%20ip%20created.png)

- Creating a Nat Gateway and assigning one of the Elastic IPs to it

![](./img/project15/59-creating%20nat%20gateway.png)
![](./img/project15/59-creating%20nat%20gateway-2.png)

- Setting up Security Group for Application load balancer in a way that it will allow https traffic from any IP address.

![](./img/project15/public%20alb%20sg.png)

- Setting up Security Group for Nginx servers in a way that it will allow https traffic only from the Application Load balancer and allow bastion servers to ssh into it.

![](./img/project15/28-creating%20sg%20for%20nginx.png)
![](./img/project15/nginx.png)

- Setting up Security Group for bastion server in a way that it will only allow access from the workstations that need to SSH into the bastion servers.

![](./img/project15/30-creating%20sg%20for%20bastion.png)

- Setting up Security Group for internal Application Load balancer in a way that it will allow traffic only from Nginx servers

![](./img/project15/internal%20sg.png)

- Setting up Security Group for Webservers in a way that it will allow https traffic only from the internal Application Load balancer

![](./img/project15/32-creating%20sg%20for%20webservers.png)
![](./img/project15/webserver%20sg.png)

- Setting Security Group for the Data Layer subnet in a way that it will allow TCP port 3306 traffic only from the webservers.

![](./img/project15/efs-sg.png)

## STEP 3: Creating An AMI Out Of The EC2 Instance For Nginx And Bastion server
- 3 EC2 Instance based on Red Hat of the T2 micro family were launched for Nginx, bastion and the one for the two webservers

![](./img/project15/sxefvcedcw.png)

**For The Baston Server**
- After connecting to it through ssh on the terminal, the following commands are run to install some necessary softwares:

![](./img/project15/bastion-conf1.png)
![](./img/project15/bastion-conf2.png)
![](./img/project15/bastion-conf3.png)
![](./img/project15/bastion-conf4.png)

- Creating an AMI out of the Bastion EC2 instance

![](./img/project15/bastion-image.png)

**For Nginx Server**
- After connecting to EC2 Instance for the Nginx through ssh on the terminal, the following commands are run to install some necessary softwares:
![](./img/project15/nginx-conf1.png)
![](./img/project15/nginx-conf2.png)
![](./img/project15/nginx-conf3.png)
![](./img/project15/nginx-conf4.png)
![](./img/project15/nginx-conf5.png)
![](./img/project15/nginx-conf6.png)
![](./img/project15/nginx-conf7.png)
![](./img/project15/nginx-conf8.png)
![](./img/project15/nginx-conf9.png)
![](./img/project15/nginx-conf10.png)
![](./img/project15/nginx-conf11.png)
![](./img/project15/nginx-conf12.png)

## STEP 4: Creating An AMI Out Of The EC2 Instance For The Tooling and Wordpress Webservers

-  After connecting to the EC2 instance for the tooling and wordpress site through SSH on the terminal, the following commands are run to install some necessary softwares:

![](./img/project15/web-conf1.png)
![](./img/project15/web-conf2.png)
![](./img/project15/web-conf4.png)
![](./img/project15/web-conf5.png)
![](./img/project15/web-conf6.png)
![](./img/project15/web-conf7.png)
![](./img/project15/web-conf8.png)
![](./img/project15/web-conf9.png)
![](./img/project15/web-conf10.png)
![](./img/project15/web-conf11.png)
![](./img/project15/web-conf12.png)

- Creating an AMI out of the EC2 instance

![](./img/project15/wbserver-image.png)

## STEP 5: Creating A Launch Template

**For Bastion Server**
- Setting up a launch template with the Bastion AMI
- Ensuring the Instances are launched into the public subnet
- Entering the Userdata to update yum package repository and install ansible and mysql

![](./img/project15/41-creating%20lt%20for%20bastion.png)
![](./img/project15/bastion-lt.png)
![](./img/project15/bastion-lt2.png)

**For Nginx Server**
- Setting up a launch template with the Nginx AMI
- Ensuring the Instances are launched into the public subnet
- Assigning appropriate security group
- Entering the Userdata to update yum package repository and install Nginx

![](./img/project15/34-creating%20lt%20for%20nginx.png)
![](./img/project15/nginx-lt.png)
![](./img/project15/34-creating%20lt%20for%20nginx-3.png)
![](./img/project15/34-creating%20lt%20for%20nginx-4.png)
![](./img/project15/nginx-lt2.png)

**For Tooling Server**
- Setting up a launch template with the Bastion AMI
- Ensuring the Instances are launched into the public subnet
- Assigning appropriate security group
- Entering the Userdata to update yum package repository and apache server

![](./img/project15/webserver-lt.png)
![](./img/project15/webserver-lt2.png)
![](./img/project15/49-creating%20lt%20for%20tooling-2.png)
![](./img/project15/webserver-lt3.png)

**For Wordpress Server**
- Setting up a launch template with the Bastion AMI
- Ensuring the Instances are launched into the public subnet
- Assigning appropriate security group
- Configure Userdata to update yum package repository and install wordpress and apache server 

![](./img/project15/webserver-lt2.png)
![](./img/project15/47-creating%20lt%20for%20wordpress-2.png)
![](./img/project15/wordpress-lt3.png)

## STEP 6: Configuring Target Groups

**For Nginx Server**
- Selecting Instances as the target type
- Ensuring the protocol HTTPS on secure TLS port 443
- Ensuring that the health check path is `/healthstatus`

![](./img/project15/37-creating%20tg%20for%20nginx.png)

**For Tooling Server**
- Selecting Instances as the target type
- Ensuring the protocol HTTPS on secure TLS port 443
- Ensuring that the health check path is `/healthstatus`

![](./img/project15/50-creating%20tg%20for%20tooling.png)

**For Wordpress Server**
- Selecting Instances as the target type
- Ensuring the protocol HTTPS on secure TLS port 443
- Ensuring that the health check path is `/healthstatus`

![](./img/project15/51-creating%20tg%20for%20wordpress.png)

## STEP 7: Configuring AutoScaling Group

- Selecting the right launch template
- Selecting the VPC
- Selecting both public subnets
- Enabling Application Load Balancer for the AutoScalingGroup (ASG)
- Selecting the target group you created before
- Ensuring health checks for both EC2 and ALB
- Setting the desired capacity, Minimum capacity and Maximum capacity to 2
- Setting the scale out option if CPU utilization reaches 90%
- Activating SNS topic to send scaling notifications

**For Nginx Server**

![](./img/project15/38-creating%20asg%20for%20nginx.png)
![](./img/project15/38-creating%20asg%20for%20nginx-2.png)
![](./img/project15/38-creating%20asg%20for%20nginx-3.png)
![](./img/project15/38-creating%20asg%20for%20nginx-4.png)
![](./img/project15/38-creating%20asg%20for%20nginx-5.png)
![](./img/project15/38-creating%20asg%20for%20nginx-6.png)
![](./img/project15/38-creating%20asg%20for%20nginx-7.png)
![](./img/project15/38-creating%20asg%20for%20nginx-8.png)

**For Bastion Server**

![](./img/project15/44-creating%20asg%20for%20bastion.png)
![](./img/project15/45-creating%20asg%20for%20bastion.png)
![](./img/project15/46-creating%20asg%20for%20bastion.png)


**For Tooling Server**

![](./img/project15/52-creating%20asg%20for%20tooling.png)
![](./img/project15/53-creating%20asg%20for%20tooling-2.png)
![](./img/project15/53-creating%20asg%20for%20tooling-3.png)

**For Wordpress**

![](./img/project15/54-creating%20asg%20for%20wordpress.png)
![](./img/project15/54-creating%20asg%20for%20wordpress-4.png)
![](./img/project15/54-creating%20asg%20for%20wordpress-5.png)
![](./img/project15/54-creating%20asg%20for%20wordpress-6.png)

## STEP 8: Creating TLS Certificates From Amazon Certificate Manager (ACM)
 TLS certificates is created to handle secured connectivity to the Application Load Balancers (ALB)
- Navigating to AWS ACM
- Requesting a public wildcard certificate for the domain name you registered in Freenom
- Using DNS to validate the domain name

![](./img/project15/55-requesting%20certificate.png)
![](./img/project15/cert.png)

## STEP 9: Configuring Application Load Balancer (ALB)
**For External Load Balancer**
- Selecting Internet facing option
- Ensuring that it listens on HTTPS protocol (TCP port 443)
- Ensuring the ALB is created within the appropriate VPC, AZ and the right Subnets
- Choosing the Certificate already created from ACM
- Selecting Security Group for the external load balancer
- Selecting Nginx Instances as the target group

![](./img/project15/56-creating%20alb%20for%20public.png)
![](./img/project15/56-creating%20alb%20for%20public-2.png)
![](./img/project15/56-creating%20alb%20for%20public-3.png)
![](./img/project15/56-creating%20alb%20for%20public-4.png)
![](./img/project15/56-creating%20alb%20for%20public-5.png)

**For Internal Load Balancer**
- Setting the Internal ALB option
- Ensuring that it listens on HTTPS protocol (TCP port 443)
- Ensuring the ALB is created within the appropriate VPC, AZ and Subnets
- Choosing the Certificate already created from ACM
- Selecting Security Group for the internal load balancer
- Selecting webserver Instances as the target group
- Ensuring that health check passes for the target group

![](./img/project15/57-creating%20alb%20for%20private.png)
![](./img/project15/57-creating%20alb%20for%20private-2.png)
![](./img/project15/57-creating%20alb%20for%20private-3.png)
![](./img/project15/57-creating%20alb%20for%20private-4.png)

**Configuring the Listener on the Internal ALB to route traffic to wordpress server**

![](./img/project15/58-configuring%20listener%20for%20internal%20lb.png)
![](./img/project15/58-configuring%20listeners%20for%20internal%20lb-2.png)

## STEP 10: Setting Up EFS Storage For The Webservers

- Create an EFS filesystem
- Create an EFS mount target per AZ in the VPC, associate it with both subnets dedicated for data layer
- Associate the Security groups created earlier for data layer.
- Create an EFS access point. (Give it a name and leave all other settings as default)

![](./img/project15/efs.png)
![](./img/project15/efs-1.png)
![](./img/project15/efs-4.png)

## STEP 11: Creating Key Management Service(KMS)

![](./img/project15/kms-1.png)
![](./img/project15/kms-2.png)
![](./img/project15/kms-3.png)
![](./img/project15/kms-5.png)

## STEP 12: Setting Up A Relational Database System

![](./img/project15/rds-1.png)
![](./img/project15/rds-2.png)
![](./img/project15/rds-3.png)
![](./img/project15/rds-4.png)

## STEP 13: Creating DNS Records In The Route53 For the Tooling And Wordporess site 
**For Tooling DNS record**

![](./img/project15/tooling%20dns%20record.png)

**For Wordpress record**

![](./img/project15/wordpress%20dns%20record.png)

## STEP 14: Result
- Entering the url https://www.wordpress.somdev.ga will route traffic from the application load balancer to the nginx and then to the server for wordpress site through the internal ALB:

![](./img/project15/wordpress%20result.png)

- Entering the url https://www.tooling.somdev.ga will route traffic from the application load balancer to the nginx and then to the internal ALB which forwards the traffic to the server for tooling site:

![](./img/project15/result%20for%20tooling.png)
