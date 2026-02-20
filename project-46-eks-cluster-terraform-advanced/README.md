# 𝐓𝐞𝐫𝐫𝐚𝐟𝐨𝐫𝐦:  𝐃𝐞𝐩𝐥𝐨𝐲 𝐚𝐧 𝐄𝐊𝐒 𝐂𝐥𝐮𝐬𝐭𝐞𝐫 — 𝐋𝐢𝐤𝐞 𝐚 𝐁𝐨𝐬𝐬!

<p align="center">
  <img src="https://imgur.com/7iDEQQH.png" />
</p>

------
###  :loudspeaker: ᴛᴇʀʀᴀғᴏʀᴍ: ᴀʙᴏᴜᴛ ᴛʜɪs ᴘʀᴏᴊᴇᴄᴛ ᴍᴏᴅᴜʟᴇs 

*Kubernetes, often abbreviated as “K8s” (because there are 8 letters between the “K” & “s” in Kubernetes), orchestrates containerized applications to run on a cluster of hosts. K8s also allocates storage and persistent volumes to running containers, provides automatic scaling, and works continuously to maintain the desired state of applications, providing resiliency.*

*Terraform is an extremely popular infrastructure provisioning tool among DevOps. EKS is managed K8S solution provided by AWS, which is widely used managed K8S platform by AWS consumers.*

*Separately, Kubernetes and Terraform are powerful and popular tools for DevOps operations. However, when you decide to use them together, you will see even more benefits for container cluster management!*

-----
## :loudspeaker: ᴛᴇʀʀᴀғᴏʀᴍ: ᴡʜʏ ᴅᴇᴘʟᴏʏ ᴡɪᴛʜ ᴛᴇʀʀᴀғᴏʀᴍ?

*While you could use the built-in AWS provisioning (UI, CLI, CloudFormation) for EKS clusters, Terraform provides you with several benefits:*

* *Terraform can be used to manage Kubernetes infrastructure, helping you to orchestrate your applications and run them at scale. This alleviates some of the challenges of running Kubernetes, including detecting configuration drift — planned & unplanned changes.*

* *Terraform will create resources, it will also update & delete tracked resources without requiring inspection of the API.*

* *Terraform understands dependency relationships between resources. For example, if an AWS Kubernetes cluster needs a specific VPC and subnet configurations, Terraform won’t attempt to create the cluster if the VPC and subnet failed to create with the proper configuration.*

------
## :loudspeaker: ᴛᴇʀʀᴀғᴏʀᴍ: ᴘʀᴇʀᴇǫᴜɪsɪᴛᴇs

*For this tutorial, you will need:*

* **AWS account**

* **Terraform & Kubernetes installed on your IDE (I will be using VSCode)**

* **AWS CLI installed and configured on your IDE**

------
## :loudspeaker: ᴛᴇʀʀᴀғᴏʀᴍ: ᴏᴜʀ ᴏʙᴊᴇᴄᴛɪᴠᴇ:

1. *Create an EKS cluster (capacity of 2).*

2. *Create a random string that allows 5 characters to build the cluster name.*

3. *They want to output the cluster name and the ip address of the containers in the cluster.*

*Lastly, all code should be in module blocks, not resource blocks.*

***Let’s get started — buckle up Chuck!!***

------

### 𝟷| sᴇᴛ ᴜᴘ ғɪʟᴇ sʏsᴛᴇᴍ

*First, clone my GitHub repository:*

```
git clone https://github.com/harshhaareddy/eks-cluster-terraform
```

*Change into the directory to the folder shown below:*
```
cd eks-cluster-terraform
```

------
### 𝟸| ᴛᴇʀʀᴀғᴏʀᴍ ɪɴɪᴛ, ᴘʟᴀɴ & ᴀᴘᴘʟʏ

*After you have created the above files, the first step is to initialize the terraform backend by using the `terraform init` command. Next, you will run the `terraform plan` command to evaluate the Terraform configuration. Finally, you will run the command `terraform apply` to apply the configuration.*

*Also, run the following command to to retrieve the access credentials for your cluster and configure kubectl:*
```
aws eks update-kubeconfig --name <EKS_CLUSTER_NAME> --region <REGION>
```

*Run kubectl commands to manage your cluster and deploy Kubernetes configurations to it.*

------
### 𝟹| ᴛᴇʀʀᴀғᴏʀᴍ ᴄʟᴏᴜᴅ

*Navigate to the Terraform Cloud platform, choose your organization and create a new workspace.*

![https://www.terraform.io/](https://img.shields.io/badge/Terraform-3EAAAF?style=for-the-badge&logo=terraform&logoColor=white)

*Under ***Choose your workflow***, select the version control workflow option. After you’ve selected your workflow, you’ll be directed to a different page where you will need to connect a version control provider. You will want to connect with your GitHub account and select the repo that you created in the first step.*

*From there, you will create our new Workspace:*

*Then you will set variables for our access keys and region. To get started, click ***Configure Variables*** followed by* ***Add variable.***

*We will be inputting the below variables as ***Keys*** and then ***Value*** will be the password.*

* **IMPORTANT**: *Click ***Sensitive*** for your key variables, as this will ensure your private information is not displayed.*

   ⇥  **AWS_ACCESS_KEY_ID**
   ⇥ **AWS_SECRET_ACCESS_KEY**
   ⇥  **AWS_DEFAULT_REGION**
   ⇥ **CONFIRM_DESTROY**

------
   ### 𝟺| ʀᴜɴ ɴᴇᴡ ᴛᴇʀʀᴀғᴏʀᴍ ᴄʟᴏᴜᴅ ᴘʟᴀɴ

   *Let’s go things kicked off — click* ***Start new run*** *under the Actions tab.*

   *Once you start your run, the next step will be to ***Plan & Apply***. Your plan should finish pretty quickly and once it’s finished, you’ll be prompted to click ***Confirm & Apply****.

   *From here, click the Apply finished box, scroll to the bottom and you’ll see the Outputs in TF Cloud:*

   *Let’s pop to the ***AWS EC2*** console and confirm that you have correctly setup your cluster. As you can see from the image below, everything looks great!*

------
   ### 𝟻| ᴛᴇʀʀᴀғᴏʀᴍ ᴅᴇsᴛʀᴏʏ

   *Let’s destroy our infrastructure! Yay! Navigate back to the Terraform Cloud platform, and under settings click ***Destruction and Deletion***. Click Queue destroy plan and select ***Confirm & Apply***.*

------
   ## ***You’ve just deployed an EKS Cluster using Terraform Cloud CI/CD!***

<p align="center">
  <img src="https://imgur.com/7iMQJlY.gif" />
</p>

------
## :biohazard: ᴄʀᴇᴅɪᴛs & ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ʟɪᴋᴇ ᴛʜɪs ᴏʀ ғᴏʟʟᴏᴡ

Ⓒ [Dev Cloud Ninja Projects](https://github.com/DevCloudNinjas-Projects.git) - Made with :yellow_heart: from [DevCloud Ninjas](https://github.com/DevCloudNinjas.git)
