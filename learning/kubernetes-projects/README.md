# Practical Realtime Kubernetes Projects + Learning

𝐀 𝐫𝐞𝐩𝐨 𝐭𝐨 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐏𝐫𝐚𝐜𝐭𝐢𝐬𝐞 𝐊𝐮𝐛𝐞𝐫𝐧𝐞𝐭𝐞𝐬 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐠𝐫𝐨𝐮𝐧𝐝 𝐮𝐩 𝐛𝐲 𝐝𝐨𝐢𝐧𝐠 𝐩𝐫𝐚𝐜𝐭𝐢𝐜𝐚𝐥 𝐑𝐞𝐚𝐥𝐭𝐢𝐦𝐞 𝐩𝐫𝐨𝐣𝐞𝐜𝐭𝐬 𝐚𝐧𝐝 𝐭𝐞𝐚𝐜𝐡 𝐲𝐨𝐮 𝐡𝐨𝐰 𝐭𝐨 𝐮𝐬𝐞 𝐊𝐮𝐛𝐞𝐫𝐧𝐞𝐭𝐞𝐬 𝐭𝐨 𝐝𝐞𝐩𝐥𝐨𝐲, 𝐦𝐚𝐧𝐚𝐠𝐞, 𝐚𝐧𝐝 𝐬𝐜𝐚𝐥𝐞 𝐜𝐨𝐧𝐭𝐚𝐢𝐧𝐞𝐫𝐢𝐳𝐞𝐝 𝐚𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧𝐬.

![kubernetes](https://imgur.com/kHtYfa8.png)

## Prerequisites

It would be nice if you know what `kubectl` is and have a basic understanding of running conatiners with docker / containerd or cri-o.

## Preparation

To get prepared please install the `kubernetes cli` & `setup cluster` in your env from [**HERE**](https://gist.github.com/DevCloudNinjas/854ed5c12fff07acde88faf95b9decff) and make sure to have bash completion for kubectl in place

## Learning List

1. [**Kubernetes for Everyone**](learning/kubernetes-projects/learning/kubernetes-for-everyone/README.md)

2. [**What is a Pod in Kubernetes?**](learning/kubernetes-projects/learning/What-is-Pod-in-Kubernetes/README.md)

3. [**Deploying an Application on Kubernetes: A Complete Guide!**](learning/kubernetes-projects/learning/Deploying-an-Application-on-Kubernetes/README.md)

4. [**Kubernetes – Architecture and main components overview**](learning/kubernetes-projects/learning/Kubernetes-components-overview/README.md)

**MORE ADDING SOON**

## Projects List

1. [**Designing a 10-Microservices Application Deployment on EKS!**](learning/kubernetes-projects/projects/10-microservices-deployment-eks/README.md)

2. [**Deploying Spring Boot application on K8S**](learning/kubernetes-projects/projects/Deploying-Spring-Boot-K8S/README.md)

3. [**Uber Clone DevSecOps CI/CD Kubernetes Project**](learning/kubernetes-projects/projects/Uber-Clone-DevSecOps/README.md)

4. [**Deploy to Kubernetes Using Jenkins | End to End DevOps Project | CICD**](learning/kubernetes-projects/projects/Kubernetes-Using-Jenkins/README.md)

**MORE ADDING SOON**

![icons-all](https://imgur.com/W53NNea.png)

![k8s-resources-map](https://imgur.com/4vq8Nxz.png)

## Kubernetes  Guides

### Networking

The purpose of [this website](https://www.tkng.io/) is to provide an overview of various Kubernetes networking components with a specific focus on exactly how they implement the required functionality.

The guide is split into multiple parts which can be studied mostly independently, however they all work together to provide a complete end-to-end cluster network abstractions.

Where possible, every topic in this guide will include a dedicated [hands-on labs](https://www.tkng.io/lab/) which can be spun up locally in a matter of minutes. 

### Security
 
The Security checklist aims at providing a basic list of guidance with links to more comprehensive documentation on each topic. It does not claim to be exhaustive and is meant to evolve.

1- https://kubernetes.io/docs/concepts/security/security-checklist/

2- https://github.com/magnologan/awesome-k8s-security

3- https://github.com/freach/kubernetes-security-best-practice

4- https://medium.com/@seifeddinerajhi/kubernetes-security-assessment-guidelines-and-necessary-checklist-9a326f341b68

5- https://medium.com/@seifeddinerajhi/owasp-kubernetes-top-10-a-comprehensive-guide-f03af6fd66ed

5- https://eksclustergames.com:  Kubernetes CTF (Capture The Flag) challenges for EKS 

### Storage

- The key concepts of Kubernetes storage, including [PVs, PVCs, and StorageClass](https://medium.com/@seifeddinerajhi/understanding-storage-in-kubernetes-ee2c19001aae)

### Misc

- Kelsey Hightower's open-source guide, [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way), goes through how to bootstrap a Kubernetes cluster without the use of installers or scripts. 


- [Learnk8s](https://learnk8s.io/): Develop the knowledge and skills to get the most out of Kubernetes with hands-on online courses and instructor-led classes.

- [Introduction to Kubernetes Lecture Notes](https://github.com/kaan-keskin/introduction-to-kubernetes/tree/main): Notes about Kubernetes resources  

- [Kubernetes Handbook](https://github.com/rootsongjc/kubernetes-handbook)

- [Kubeapps](https://github.com/vmware-tanzu/kubeapps): A web-based UI for deploying and managing applications in Kubernetes clusters

- [Start learning Kubernetes today](https://kubebyexample.com/)

- [Step by step guide to learning Kubernetes](https://roadmap.sh/kubernetes)


- [Kubernetes mind map](https://betterprogramming.pub/6-important-things-you-need-to-run-kubernetes-in-production-d573d61258c5): 6 Important Things You Need to Run Kubernetes in Production.

## TroubleShooting

- [COMMON KUBERNETES ERRORS AND HOW THEY IMPACT CLOUD DEPLOYMENTS](https://cloudtweaks.com/2023/01/common-kubernetes-errors/)

- [Exit Codes In Containers & Kubernetes – The Complete Guide](https://komodor.com/learn/exit-codes-in-containers-and-kubernetes-the-complete-guide/)

- [How to identify and troubleshoot common Kubernetes errors](https://newrelic.com/blog/how-to-relic/monitoring-kubernetes-part-three)

- [Kubernetes Troubleshooting: 5 Common Errors & How to Fix Them](https://lumigo.io/kubernetes-troubleshooting/)

- [Kubernetes Troubleshooting – The Complete Guide](https://komodor.com/learn/kubernetes-troubleshooting-the-complete-guide/)


- [A visual guide on troubleshooting Kubernetes deployments](https://learnk8s.io/troubleshooting-deployments)

- [Kubernetes Troubleshooting: Effective Strategies for Unraveling the Puzzle](https://www.groundcover.com/kubernetes-troubleshooting)


- [node-problem-detector](https://github.com/kubernetes/node-problem-detector): This is a place for various problem detectors running on the Kubernetes nodes.


- [Kubernetes Goat](https://github.com/madhuakula/kubernetes-goat): "Vulnerable by Design" cluster environment to learn and practice Kubernetes security using an interactive hands-on playground 🚀

##  Kubernetes in the cloud:

### AWS EKS

- [Terraform module to create AWS Elastic Kubernetes (EKS) resources](https://github.com/terraform-aws-modules/terraform-aws-eks)

- [This project](https://github.com/aws-ia/terraform-aws-eks-blueprints) contains a collection of Amazon EKS cluster patterns implemented in Terraform that demonstrate how fast and easy it is for customers to adopt Amazon EKS. The patterns can be used by AWS customers, partners, and internal AWS teams to configure and manage complete EKS clusters that are fully bootstrapped with the operational software that is needed to deploy and operate workloads.

- [EKS Workshop](https://www.eksworkshop.com/)

- [ (Amazon EKS) Best Practices](https://aws.github.io/aws-eks-best-practices/): A best practices guide for day 2 operations, including operational excellence, security, reliability, performance efficiency, and cost optimization.

- [AWS EKS Kubernetes - Masterclass | DevOps, Microservices](https://github.com/stacksimplify/aws-eks-kubernetes-masterclass)


### Azure AKS

- [Azure AKS Kubernetes Masterclass](https://github.com/stacksimplify/azure-aks-kubernetes-masterclass).

- [Official repository for the AKS Landing Zone Accelerator program](https://github.com/Azure/AKS-Landing-Zone-Accelerator): Azure Landing Zone Accelerators are architectural guidance, reference architecture, reference implementations and automation packaged to deploy workload platforms on Azure at Scale and aligned with industry proven practices.

- [Azure Kubernetes Service Checklist](https://www.the-aks-checklist.com/): This checklist contains a large set of best practices and some of them may not be relevant to your context and thus the rating may be incorrect in your case. Please choose and apply them wisely.


### Google GKE

- [Configures opinionated GKE clusters in terraform](https://github.com/terraform-google-modules/terraform-google-kubernetes-engine)

- [Sample applications for Google Kubernetes Engine (GKE)](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples)

## CNCF certifications:

- [Kubernetes CKS Full Course](https://www.youtube.com/watch?v=d9xfB5qaOfg) Theory + Practice + Browser Scenarios by Kim Wuestkamp

- [Kubernetes CKS Course Environment](https://github.com/killer-sh/cks-course-environment)

- [Certified Kubernetes Security Specialist - CKS](https://github.com/walidshaari/Certified-Kubernetes-Security-Specialist): Curated resources help you prepare for the CNCF/Linux Foundation CKS 2021 "Kubernetes Certified Security Specialist" Certification exam.

- [Kubernetes Certified Administration](https://github.com/walidshaari/Kubernetes-Certified-Administrator): Online resources that will help you prepare for taking the CNCF CKA 2020 "Kubernetes Certified Administrator" Certification exam.

- [CKA preparation](https://github.com/alijahnas/CKA-practice-exercises): This is a guide for passing the CNCF Certified Kubernetes Administrator (CKA) with practice exercises.

- [CKA Exercises](https://github.com/chadmcrowell/CKA-Exercises): Practice for the Certified Kubernetes Administrator (CKA) Exam.

## Kubernetes IAC:

Certainly! Here's a list of some popular tools for managing Kubernetes Infrastructure as Code (IAC):

1. **Helm:**
   - Overview: Helm is a package manager for Kubernetes that simplifies the deployment and management of applications.
   - GitHub: [Helm GitHub Repository](https://github.com/helm/helm)

2. **Kustomize:**
   - Overview: Kustomize is a tool for customizing Kubernetes manifests, allowing you to manage configuration variations in a declarative way.
   - GitHub: [Kustomize GitHub Repository](https://github.com/kubernetes-sigs/kustomize)

3. **Kubeconfig Management:**
   - Tools like `kubectx` and `kubens` help manage and switch between multiple Kubernetes contexts and namespaces.
   - GitHub: [kubectx GitHub Repository](https://github.com/ahmetb/kubectx)

4. **Kubeval:**
   - Overview: Kubeval is a tool for validating Kubernetes manifests against the Kubernetes API schema.
   - GitHub: [Kubeval GitHub Repository](https://github.com/instrumenta/kubeval)

5. **Kops:**
   - Overview: Kops helps you create, destroy, upgrade, and maintain Kubernetes clusters on AWS.
   - GitHub: [Kops GitHub Repository](https://github.com/kubernetes/kops)

6. **Terraform:**
   - Overview: While not specific to Kubernetes, Terraform is widely used for IAC and can be used to provision and manage Kubernetes infrastructure.
   - Website: [Terraform](https://www.terraform.io/)

7. **Pulumi:**
   - Overview: Pulumi allows you to define infrastructure as code using familiar programming languages, including TypeScript, Python, and Go.
   - GitHub: [Pulumi GitHub Repository](https://github.com/pulumi/pulumi)

8. **Helmfile:**
   - Overview: Declaratively deploy your Kubernetes manifests, Kustomize configs, and Charts as Helm releases. Generate all-in-one manifests for use with ArgoCD.
   - GitHub: [Kubeform GitHub Repository](https://github.com/helmfile/helmfile)

9. **Jsonnet:**
   - Overview: Jsonnet is a data templating language that can be used to generate Kubernetes manifests.
   - GitHub: [Jsonnet GitHub Repository](https://github.com/google/jsonnet)

10. **Skaffold:**
    - Overview: Skaffold is a command-line tool that facilitates continuous development for Kubernetes applications.
    - GitHub: [Skaffold GitHub Repository](https://github.com/GoogleContainerTools/skaffold)

***This is not an exhaustive list, and the choice of tools depends on your specific use case and preferences. Always check the official documentation and community support for each tool for the most accurate and up-to-date information.***

---

## Hit the Star! ⭐
***If you are planning to use this repo for learning, please hit the star. Thanks!***

### ❤ by [H A R S H H A A](https://github.com/DevCloudNinjas) - Owner/Creator
