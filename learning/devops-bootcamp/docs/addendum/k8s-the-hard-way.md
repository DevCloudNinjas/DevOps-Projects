---
docs/addendum/k8s-the-hard-way.md:
  category: Container Orchestration
  estReadingMinutes: 40
  exercises:
    -
      name: Kubernetes the Hard Way
      description: Follow along with Ivan Fioravanti's fork of Kubernetes the Hard Way, manually creating Terraform and Ansible code to stand up a Kubernetes cluster within Azure. This exercise will provide a deep understanding of the low level, administrative perspective of setting up a Kubernetes cluster.
      estMinutes: 6000
      technologies:
      - Kubernetes
      - Terraform
      - Ansible
      - Azure
      - Networking
      - cfssl
      - cfssljson
      - kubectl
      - azure-cli
---

# K8s the Hard Way

In this section, we will be taking a deep dive into the building blocks of Kubernetes, following along with Ivan Fioravanti's fork of [Kubernetes the Hard Way](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure). We will be creating the Terraform and Ansible code along the way that will manually stand everything up within Azure.

This way of creating a cluster is by no means production-ready and is designed solely for learning the low level, administrative perspective. This implies going the extra mile to make sure you comprehend each step involved in setting up a Kubernetes cluster. (Go into more detail about understanding the k8s control plane and all the different components)

## A Quick High Level of the Kubernetes Control Plane

The Kubernetes control plane is the powerhouse of the cluster. It is in charge of maintaining the cluster's state and scheduling workloads. The control plane consists of several components that run on the controller nodes. These components include:

- [kube-apiserver](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) - The Kubernetes' Control Plane's front end. It is the only component with which the kubectl CLI communicates with. It is responsible for creating, updating, and deleting resources in the cluster.
- [kube-scheduler](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/) - The scheduler monitors newly created pods that have no node assigned, and selects a node for them to run on.
- [kube-controller-manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/) - A collection of controllers that watch the cluster's state and make changes as needed. The node, replication, endpoints, service account and token controllers are among the most important.
- [etcd](https://etcd.io/) - A reliable and highly available key-value store that serves as a sort of database for Kubernetes. This is where all cluster data is kept.

These controller nodes communicate with the worker nodes via:

- kubelet - The primary "node agent" that each node runs. The kubelet accepts a set of PodSpecs provided by various mechanisms and ensures that the containers described in those PodSpecs are up and running.
- kube-proxy - The Kubernetes network proxy runs on each node. This essentially implements part of the Kubernetes service concept.

![Kubernetes Cluster](img-addendum/k8sthw-components-of-kubernetes.svg ':class=cluster')

### Getting Started

We will need to ensure that cfssl, cfssljson, kubectl, Ansible and azure-cli are all installed.

- [cfssl](https://github.com/cloudflare/cfssl) is a tool for creating and managing TLS certificates. These certificates will be used to secure the various components of the cluster, allowing each to communicate with other components inside the cluster.
- [cfssljson](https://github.com/cloudflare/cfssl) is used for converting between JSON and the binary DER format.
- [kubectl](https://kubernetes.io/docs/reference/kubectl/) is the Kubernetes CLI that allows you to run commands against the cluster.
- [Ansible](https://www.ansible.com/resources/get-started/) is a configuration management tool that allows you to automate the configuration of your infrastructure. (The link provided is a refresher on the Ansible basics if needed.)
- [azure-cli](https://learn.microsoft.com/en-us/cli/azure/) is the Azure CLI that allows you to interact with Azure.

You can install them with brew.

```bash
brew install cfssl cfssljson kubectl ansible azure-cli
```

Login into the Azure CLI using "[az login](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli)" and create a resource group using Terraform. This resource group will be used to store all the various resources that we will be creating.

**NOTE**: You will be writing a lot of Ansible and Terraform code. Consider splitting everything up into modules. This will help make it easier to understand and maintain.

### Tips For Success

It is VERY important to understand the networking topology of the cluster. This will help you to understand how the various components communicate with each other. The following diagram shows a more descriptive network topology of the cluster and you can find a link to an overview of the various components [here](https://kubernetes.io/docs/concepts/overview/components/)

![Kubernetes Cluster](img-addendum/k8sthw-network-topology.svg ':class=cluster')

- Overview
  - When starting out, it is important to identify what tool you are using and what it is used for. For example, the lab "Provisioning Compute Resources" would be a case of **building** infrastructure, thus using Terraform. Whereas "Provisioning the CA and Generating TLS Certificates" would be a case of **configuring** infrastructure, thus using Ansible. Be sure to distinguish between the two as you are moving through the labs.
  - Highly recommend making good use of Terraform's variables and outputs. This will help you to keep track of the resources that you are creating and a way to reference them in other modules.
  - **NOTE**: If no notes are provided, it is assumed that the lab is straight forward and does not require any additional information.

- [Provisioning Compute Resources](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/03-compute-resources.md)
  - Output the load balancer IP address as well as the controller and worker node IP addresses.
  - When configuring the controller and worker nodes, look into using the "cidrhost()" function to dynamically assign the IP addresses. This will help you to avoid having to manually update the IP addresses in the Ansible inventory file.
  - Configure the nodes using "azurerm_linux_virtual_machine" and the "tls_private_key" resources. After turning off password authentication, the nodes will be secure as they are only accessible through an SSH key.
  - Pass the various output variables, like the ip addresses, into the Ansible inventory file.

- [Provisioning the CA and Generating TLS Certificates](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/04-certificate-authority.md)
  - Look into Ansible's "[template](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html)" and "[copy](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html)" modules. These will help you to dynamically generate and apply the various configuration files.
  - If using "ssh" or "scp", be sure to add the "-o StrictHostKeyChecking=no" flag to avoid having to manually accept the host key.

- [Generating Kubernetes Configuration Files for Authentication](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/05-kubernetes-configuration-files.md)
  - Reference the "Provisioning the CA and Generating TLS Certificates" tips for success section.

- [Generating the Data Encryption Config and Key](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/06-data-encryption-keys.md)
  - Reference the "Provisioning the CA and Generating TLS Certificates" tips for success section.

- [Bootstrapping the etcd Cluster](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/07-bootstrapping-etcd.md)
  - Use the [kubernetes.core.k8s](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_module.html) module. This will help you to dynamically create the various Kubernetes resources.
  - Look in the "[shell](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html)" module to run the various commands on the controller and worker nodes.

- [Bootstrapping the Kubernetes Control Plane](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/08-bootstrapping-kubernetes-controllers.md)

- [Bootstrapping the Kubernetes Worker Nodes](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/09-bootstrapping-kubernetes-workers.md)

- [Configuring kubectl for Remote Access](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/10-configuring-kubectl.md)
  - Target the load balancer's ip to run the various commands to configure kubectl for remote access.

- [Provisioning Pod Network Routes](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/11-pod-network-routes.md)

- [Deploying the DNS Cluster Add-on](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/12-dns-addon.md)

- [Smoke Test](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/13-smoke-test.md)
  - Would recommend a blend of Terraform and Ansible to deploy the nginx deployment and service while creating the new security group rule.

- [Dashboard Configuration](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/14-dashboard.md)

- [Cleaning Up](https://github.com/ivanfioravanti/kubernetes-the-hard-way-on-azure/blob/master/docs/15-cleanup.md)

### Deliverable

Please provide a link to your GitHub repository containing the Terraform and Ansible code. Be sure to include a readme file walking through the various steps you took and any tips for success that you would like to share.

After completing the labs, you should have a better understanding of how to provision and configure infrastructure using Terraform and Ansible, as well as the inner workings of a Kubernetes cluster.
