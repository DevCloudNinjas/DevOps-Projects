### BUILDING ELASTIC KUBERNETES SERVICE (EKS) WITH TERRAFORM


Repo to Terraform Code [Link](https://github.com/Tonybesto/EKS-Terraform)

Open up a new directory on your laptop, and name it `EKS`
Use AWS CLI to create an S3 bucket

Create a file – `backend.tf` Task for you, ensure the backend is configured for remote state in S3

```
terraform {
}
```
Create a file – `network.tf` and provision Elastic IP for Nat Gateway, VPC, Private and public subnets.

### Reserve Elastic IP to be used in our NAT gateway

```
resource "aws_eip" "nat_gw_elastic_ip" {
vpc = true

tags = {
Name            = "${var.cluster_name}-nat-eip"
iac_environment = var.iac_environment_tag
}
}
```

### Create VPC using the official AWS module

```
module "vpc" {
source  = "terraform-aws-modules/vpc/aws"

name = "${var.name_prefix}-vpc"
cidr = var.main_network_block
azs  = data.aws_availability_zones.available_azs.names

private_subnets = [
# this loop will create a one-line list as ["10.0.0.0/20", "10.0.16.0/20", "10.0.32.0/20", ...]
# with a length depending on how many Zones are available
for zone_id in data.aws_availability_zones.available_azs.zone_ids :
cidrsubnet(var.main_network_block, var.subnet_prefix_extension, tonumber(substr(zone_id, length(zone_id) - 1, 1)) - 1)
]

public_subnets = [
# this loop will create a one-line list as ["10.0.128.0/20", "10.0.144.0/20", "10.0.160.0/20", ...]
# with a length depending on how many Zones are available
# there is a zone Offset variable, to make sure no collisions are present with private subnet blocks
for zone_id in data.aws_availability_zones.available_azs.zone_ids :
cidrsubnet(var.main_network_block, var.subnet_prefix_extension, tonumber(substr(zone_id, length(zone_id) - 1, 1)) + var.zone_offset - 1)
]

# Enable single NAT Gateway to save some money
# WARNING: this could create a single point of failure, since we are creating a NAT Gateway in one AZ only
# feel free to change these options if you need to ensure full Availability without the need of running 'terraform apply'
# reference: https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.44.0#nat-gateway-scenarios
enable_nat_gateway     = true
single_nat_gateway     = true
one_nat_gateway_per_az = false
enable_dns_hostnames   = true
reuse_nat_ips          = true
external_nat_ip_ids    = [aws_eip.nat_gw_elastic_ip.id]

# Add VPC/Subnet tags required by EKS
tags = {
"kubernetes.io/cluster/${var.cluster_name}" = "shared"
iac_environment                             = var.iac_environment_tag
}
public_subnet_tags = {
"kubernetes.io/cluster/${var.cluster_name}" = "shared"
"kubernetes.io/role/elb"                    = "1"
iac_environment                             = var.iac_environment_tag
}
private_subnet_tags = {
"kubernetes.io/cluster/${var.cluster_name}" = "shared"
"kubernetes.io/role/internal-elb"           = "1"
iac_environment                             = var.iac_environment_tag
}
}
```

`Note`: The tags added to the subnets is very important. The Kubernetes Cloud Controller Manager (cloud-controller-manager) and AWS Load Balancer Controller (aws-load-balancer-controller) needs to identify the cluster’s. To do that, it querries the cluster’s subnets by using the tags as a filter.

* For public and private subnets that use load balancer resources: each subnet must be tagged
```
Key: kubernetes.io/cluster/cluster-name
Value: shared
```
* For private subnets that use internal load balancer resources: each subnet must be tagged
```
Key: kubernetes.io/role/internal-elb
Value: 1
```
* For public subnets that use internal load balancer resources: each subnet must be tagged
```
Key: kubernetes.io/role/elb
Value: 1
```


Create a file – `variables.tf`

### create some variables
```
variable "cluster_name" {
type        = string
description = "EKS cluster name."
}
variable "iac_environment_tag" {
type        = string
description = "AWS tag to indicate environment name of each infrastructure object."
}
variable "name_prefix" {
type        = string
description = "Prefix to be used on each infrastructure object Name created in AWS."
}
variable "main_network_block" {
type        = string
description = "Base CIDR block to be used in our VPC."
}
variable "subnet_prefix_extension" {
type        = number
description = "CIDR block bits extension to calculate CIDR blocks of each subnetwork."
}
variable "zone_offset" {
type        = number
description = "CIDR block bits extension offset to calculate Public subnets, avoiding collisions with Private subnets."
}
```

Create a file – `data.tf` – This will pull the available AZs for use.
```
# get all available AZs in our region
data "aws_availability_zones" "available_azs" {
state = "available"
}
data "aws_caller_identity" "current" {} # used for accesing Account ID and ARN
```

Create a file – `eks.tf` and provision EKS cluster (Create the file only if you are not using your existing Terraform code. Otherwise you can simply append it to the main.tf from your existing code) Read more about this module from the official documentation here – Reading it will help you understand more about the rich features of the module.

```
module "eks_cluster" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"
  cluster_name    = var.cluster_name
  cluster_version = "1.22"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access = true

  # Self Managed Node Group(s)
  self_managed_node_group_defaults = {
    instance_type                          = var.asg_instance_types[0]
    update_launch_template_default_version = true
  }
  self_managed_node_groups = local.self_managed_node_groups

  # aws-auth configmap
  create_aws_auth_configmap = true
  manage_aws_auth_configmap = true
  aws_auth_users = concat(local.admin_user_map_users, local.developer_user_map_users)
  tags = {
    Environment = "prod"
    Terraform   = "true"
  }
}
```


8. Create a file – `locals.tf `to create local variables. Terraform does not allow assigning variable to variables. There is good reasons for that to avoid repeating your code unecessarily. So a terraform way to achieve this would be to use locals so that your code can be kept DRY

### render Admin & Developer users list with the structure required by EKS module
```
locals {
  admin_user_map_users = [
    for admin_user in var.admin_users :
    {
      userarn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${admin_user}"
      username = admin_user
      groups   = ["system:masters"]
    }
  ]
  developer_user_map_users = [
    for developer_user in var.developer_users :
    {
      userarn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${developer_user}"
      username = developer_user
      groups   = ["${var.name_prefix}-developers"]
    }
  ]

  self_managed_node_groups = {
    worker_group1 = {
      name = "${var.cluster_name}-wg"

      min_size      = var.autoscaling_minimum_size_by_az * length(data.aws_availability_zones.available_azs.zone_ids)
      desired_size      = var.autoscaling_minimum_size_by_az * length(data.aws_availability_zones.available_azs.zone_ids)
      max_size  = var.autoscaling_maximum_size_by_az * length(data.aws_availability_zones.available_azs.zone_ids)
      instance_type = var.asg_instance_types[0].instance_type

      bootstrap_extra_args = "--kubelet-extra-args '--node-labels=node.kubernetes.io/lifecycle=spot'"

      block_device_mappings = {
        xvda = {
          device_name = "/dev/xvda"
          ebs = {
            delete_on_termination = true
            encrypted             = false
            volume_size           = 10
            volume_type           = "gp2"
          }
        }
      }

      use_mixed_instances_policy = true
      mixed_instances_policy = {
        instances_distribution = {
          spot_instance_pools = 4
        }

        override = var.asg_instance_types
      }
    }
  }
}
```



Add more variables to the `variables.tf` file

### create some variables
```
variable "admin_users" {
  type        = list(string)
  description = "List of Kubernetes admins."
}
variable "developer_users" {
  type        = list(string)
  description = "List of Kubernetes developers."
}
variable "asg_instance_types" {
  description = "List of EC2 instance machine types to be used in EKS."
}
variable "autoscaling_minimum_size_by_az" {
  type        = number
  description = "Minimum number of EC2 instances to autoscale our EKS cluster on each AZ."
}
variable "autoscaling_maximum_size_by_az" {
  type        = number
  description = "Maximum number of EC2 instances to autoscale our EKS cluster on each AZ."
}

```
Create a file – `variables.tfvars` to set values for variables.
```
cluster_name            = "tooling-app-eks"
iac_environment_tag     = "development"
name_prefix             = "darey-io-eks"
main_network_block      = "10.0.0.0/16"
subnet_prefix_extension = 4
zone_offset             = 8
```

### Ensure that these users already exist in AWS IAM. Another approach is that you can introduce an iam.tf file to manage users separately, get the data source and interpolate their ARN.

```
admin_users                    = ["darey", "solomon"]
developer_users                = ["leke", "david"]
asg_instance_types             = [ { instance_type = "t3.small" }, { instance_type = "t2.small" }, ]
autoscaling_minimum_size_by_az = 1
autoscaling_maximum_size_by_az = 10
```

Create file – `provider.tf`

```
provider "aws" {
  region = "us-west-1"
}
provider "random" {
}
```

Create a file – `variables.tfvars` to set values for variables.
```
cluster_name            = "tooling-app-eks"
iac_environment_tag     = "development"
name_prefix             = "darey-io-eks"
main_network_block      = "10.0.0.0/16"
subnet_prefix_extension = 4
zone_offset             = 8
```

### Ensure that these users already exist in AWS IAM. Another approach is that you can introduce an iam.tf file to manage users separately, get the data source and interpolate their ARN.

```
admin_users                              = ["dare", "solomon"]
developer_users                          = ["leke", "david"]
asg_instance_types                       = ["t3.small", "t2.small"]
autoscaling_minimum_size_by_az           = 1
autoscaling_maximum_size_by_az           = 10
autoscaling_average_cpu                  = 30
```

`Run terraform init`

### Run Terraform plan – Your plan should have an output
```
Plan: 41 to add, 0 to change, 0 to destroy.
```
Run Terraform apply

This will begin to create cloud resources, and fail at some point with the error
```

╷
│ Error: Post "http://localhost/api/v1/namespaces/kube-system/configmaps": dial tcp [::1]:80: connect: connection refused
│ 
│   with module.eks-cluster.kubernetes_config_map.aws_auth[0],
│   on .terraform/modules/eks-cluster/aws_auth.tf line 63, in resource "kubernetes_config_map" "aws_auth":
│   63: resource "kubernetes_config_map" "aws_auth" {
```


### FIXING THE ERROR
To fix this problem

Append to the file data.tf
### Get EKS cluster info to configure Kubernetes and Helm providers
```
data "aws_eks_cluster" "cluster" {
  name = module.eks_cluster.cluster_id
}
data "aws_eks_cluster_auth" "cluster" {
  name = module.eks_cluster.cluster_id
}
```
Append to the file provider.tf
### Get EKS authentication for being able to manage k8s objects from terraform
```
provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}
```

### Run the init and plan again – This time you will see

```
  # module.eks-cluster.kubernetes_config_map.aws_auth[0] will be created
  + resource "kubernetes_config_map" "aws_auth" {
      + data = {
          + "mapAccounts" = jsonencode([])
          + "mapRoles"    = <<-EOT
                - "groups":
                  - "system:bootstrappers"
                  - "system:nodes"
                  "rolearn": "arn:aws:iam::696742900004:role/tooling-app-eks20210718113602300300000009"
                  "username": "system:node:{{EC2PrivateDNSName}}"
            EOT
          + "mapUsers"    = <<-EOT
                - "groups":
                  - "system:masters"
                  "userarn": "arn:aws:iam::696742900004:user/dare"
                  "username": "dare"
                - "groups":
                  - "system:masters"
                  "userarn": "arn:aws:iam::696742900004:user/solomon"
                  "username": "solomon"
                - "groups":
                  - "darey-io-eks-developers"
                  "userarn": "arn:aws:iam::696742900004:user/leke"
                  "username": "leke"
                - "groups":
                  - "darey-io-eks-developers"
                  "userarn": "arn:aws:iam::696742900004:user/david"
                  "username": "david"
            EOT
        }
      + id   = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + labels           = {
              + "app.kubernetes.io/managed-by" = "Terraform"
              + "terraform.io/module"          = "terraform-aws-modules.eks.aws"
            }
          + name             = "aws-auth"
          + namespace        = "kube-system"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```
### Create kubeconfig file using awscli.

```
aws eks update-kubeconfig --name <cluster_name> --region <cluster_region> --kubeconfig kubeconfig
```




### Deploy Jenkins with Helm

Before we begin to develop our own helm charts, lets make use of publicly available charts to deploy all the tools that we need.

One of the amazing things about helm is the fact that you can deploy applications that are already packaged from a public helm repository directly with very minimal configuration. An example is **Jenkins**.

1. Visit [Artifact Hub](https://artifacthub.io/packages/search) to find packaged applications as Helm Charts
2. Search for `Jenkins`
3. Add the repository to helm so that you can easily download and deploy
```
helm repo add jenkins https://charts.jenkins.io
```
![Alt text](<Images/helm add jenkins repo.PNG>)

4. Update helm repo
```
helm repo update 
```
![Alt text](<Images/helm repo update.PNG>)


5. Install the chart 
```
helm install jenkins jenkins/jenkins
```
![Alt text](<Images/helm install jenkins.PNG>)

You should see an output like this 

```
NAME: jenkins
LAST DEPLOYED: Tue Sep  5 12:38:53 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:
  kubectl exec --namespace default -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password && echo
2. Get the Jenkins URL to visit by running these commands in the same shell:
  echo http://127.0.0.1:8080
  kubectl --namespace default port-forward svc/jenkins 8080:8080

3. Login with the password from step 1 and the username: admin
4. Configure security realm and authorization strategy
5. Use Jenkins Configuration as Code by specifying configScripts in your values.yaml file, see documentation: http:///configuration-as-code and examples: https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos

For more information on running Jenkins on Kubernetes, visit:
https://cloud.google.com/solutions/jenkins-on-container-engine

For more information about Jenkins Configuration as Code, visit:
https://jenkins.io/projects/jcasc/


NOTE: Consider using a custom image with pre-installed plugins
```

6. Check the Helm deployment

```
helm ls 
```
![Alt text](<Images/helm ls.png>)

7. Check the pods

```
kubectl get pods 
```
![Alt text](<Images/kubectl get pods.png>)

8. Describe the running pod (review the output and try to understand what you see)
```
kubectl describe pod jenkins-0 
```
![Alt text](<Images/kubectl describe jenkins-0.png>)

![Alt text](<Images/jenkins login page.png>)

![Alt text](<Images/jenkins logged in.png>)



TASK 


### Prometheus installation  

Get Repository Info

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```


```
helm repo update
```


Install Chart

Starting with version 16.0, the Prometheus chart requires Helm 3.7+ in order to install successfully. Please check your helm release before installation.

```
helm install prometheus prometheus-community/prometheus
```
![Alt text](<Images/install prometheus.png>)


![Alt text](<Images/Prometheus pods running.png>)


![Alt text](<Images/homepage Prometheus.png>)



### Grafana installation

helm repo add grafana https://grafana.github.io/helm-charts

![Alt text](<Images/add grafana repo.png>)

helm repo update

helm install grafana grafana/grafana

![Alt text](<Images/grafana install.png>)

```
NAME: grafana
LAST DEPLOYED: Tue Sep  5 22:22:06 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:

   kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo


2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   grafana.default.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:
     export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
     kubectl --namespace default port-forward $POD_NAME 3000

3. Login with the password from step 1 and the username: admin
#################################################################################
######   WARNING: Persistence is disabled!!! You will lose your data when   #####
######            the Grafana pod is terminated.                            #####
#################################################################################
```
![Alt text](<Images/grafana login page.png>)


![Alt text](<Images/grafana homepage.png>)

