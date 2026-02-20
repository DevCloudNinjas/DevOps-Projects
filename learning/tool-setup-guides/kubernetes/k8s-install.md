# Kubernetes (K8S) step-by-step installation guide on Ubuntu from scratch

![k8s](https://imgur.com/bKUeyKX.png)

Certainly! Here's a step-by-step guide to installing Kubernetes (K8s) on Ubuntu from scratch. This guide will walk you through the process of setting up a basic Kubernetes cluster using `kubeadm`, `kubelet`, and `kubectl`.

**Prerequisites:**

1. **Ubuntu**: You should have a clean installation of Ubuntu on the machines where you plan to set up your Kubernetes cluster.

2. **Minimum 2 Nodes**: For a basic Kubernetes cluster, you need at least two nodes - one for the master and one or more for worker nodes.

3. **Network Configuration**: Ensure that your nodes can communicate with each other over the network. You should have a static IP address for each node.

4. **Root Privileges**: You need to run some commands with root privileges, so make sure you have `sudo` access.

**Step 1: Update and Install Required Packages**

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```

**Step 2: Disable Swap**

Kubernetes requires that swap be disabled. You can disable it temporarily with the following command:

```bash
sudo swapoff -a
```

To disable it permanently, edit the `/etc/fstab` file and comment out the line that references swap:

```bash
sudo nano /etc/fstab
# Comment out the line containing swap
```

**Step 3: Install Kubernetes Tools**

```bash
sudo apt install -y curl apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
```

**Step 4: Initialize the Kubernetes Master Node**

On your master node, initialize the Kubernetes cluster using `kubeadm`. Replace `MASTER_IP` with the actual IP address of your master node.

```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=MASTER_IP
```

After the initialization is complete, you will see a message with a `kubeadm join` command to add worker nodes to the cluster. Make sure to save this command for later use.

**Step 5: Set Up Kubectl for Your User**

Run these commands on your master node to configure `kubectl` for your user:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

**Step 6: Install a Network Plugin**

Choose a network plugin for your cluster. In this example, we'll use Calico:

```bash
kubectl apply -f https://docs.projectcalico.org/v3.18/manifests/calico.yaml
```

**Step 7: Join Worker Nodes**

On each worker node, run the `kubeadm join` command you saved from Step 4. It should look something like this:

```bash
sudo kubeadm join MASTER_IP:6443 --token TOKEN --discovery-token-ca-cert-hash SHA256_HASH
```

**Step 8: Verify Cluster**

Back on the master node, you can check the status of your cluster:

```bash
kubectl get nodes
```

You should see all nodes in the "Ready" state.

Congratulations! You've successfully installed Kubernetes on Ubuntu from scratch. You can now deploy and manage containers using Kubernetes.

## By [Harshhaa Reddy](https://www.github.com/NotHarshhaa)
