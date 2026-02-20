# Deploying Spring Boot application on Kubernetes

![](https://miro.medium.com/v2/resize:fit:736/0*pUxaXy4_zjAWtFwf.png)

### **In this article we are deploying Spring Boot application on K8S**

# **Step-by-Step Implementation:-**

## Step 1 — Create an **t2.medium** Instance

![](https://miro.medium.com/v2/resize:fit:736/1*m1tuu0xpgyaPuIA97M8cRw.png)

## Step 2 — Install the following command in instance

```bash
sudo su
yum update -y
yum install docker -y
systemctl enable docker
systemctl start docker
systemctl status docker
docker — version
```

![](https://miro.medium.com/v2/resize:fit:736/1*8qxOf5ULaFfT38rNUXx9ag.png)

## **Step 3 — Install Conntrack**

**conntrack** :- In Kubernetes, “conntrack” refers to the Connection Tracking system used for network traffic management within the cluster. Conntrack is a kernel feature that keeps track of network connections and their states. It allows the kernel to maintain information about network connections, such as source IP addresses, destination IP addresses, ports, and connection states (established, closed, etc.)

```bash
yum install conntrack -y
```

![](https://miro.medium.com/v2/resize:fit:736/1*b9OprU_EyaxGph8vh7Ct2Q.png)

## **Step 4 — Install and run minikube in vm**

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube

/usr/local/bin/minikube start --force --driver=docker
```

![](https://miro.medium.com/v2/resize:fit:736/1*3KWYKJt47caknzbv27AkLg.png)

![](https://miro.medium.com/v2/resize:fit:736/1*oaum5rMKrA7v_hWd0QWN9Q.png)

After that we can check the minikube version ,

```bash
/usr/local/bin/minikube version
```

**Step 5 — Install kubectl command , given permission to kubectl and check version of it.**

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

/usr/local/bin/kubectl version
```

![](https://miro.medium.com/v2/resize:fit:736/1*d3uGseuhtgUKJn6EZA7hNg.png)

## Step 6 — Install git and clone the repository as ,

```bash
yum install git -y
cd /opt
git clone https://github.com/SushantOps/SpringBootOnK8S_PS.git
```

![](https://miro.medium.com/v2/resize:fit:736/1*Wq0x1zA0Q8khebtki1F6Mg.png)

## **Step 7 — Now we will start setting up Database**

To create the persistent database and other services.

```bash
/usr/local/bin/kubectl get pods

/usr/local/bin/kubectl create -f db-deployment.yaml

kubectl get pods
```

![](https://miro.medium.com/v2/resize:fit:736/1*Le-vLbtW-AKSGtM-rZivQw.png)

![](https://miro.medium.com/v2/resize:fit:736/1*QsxPhddh9sweRi2KuNkmOg.png)

check database and it’s content so go inside the container as , ( password is **root** ) so we can see the db create from the container .

```bash
/usr/local/bin/kubectl exec -it <POD_NAME>/bin/bash

mysql -u root -p
```

![](https://miro.medium.com/v2/resize:fit:736/1*ooRy1qXVD2lOVPy3c9cy9Q.png)

After that exit from the shell also container.

**Install maven now and check version.**

```bash
yum install maven -y
mvn -v
```

**Step 8 — Create an image from Dockerfile as ,**

```bash
docker build -t <dockerhub_name>/<image_name> .

docker build -t sushantkapare1717/springboot-crud-k8s:1.0 .

#check the docker images 
docker images
```

![](https://miro.medium.com/v2/resize:fit:736/1*dDZ2dfHDr9TZvbVZolUyMg.png)

![](https://miro.medium.com/v2/resize:fit:736/1*IiOyFlD6wVukLPdO8fZ6Xw.png)

Now push that image to dockerhub so first you have to login to dockerhub and then push that image to docker hub

```bash
docker login

docker push sushantkapare1717/springboot-crud-k8s
```

![](https://miro.medium.com/v2/resize:fit:736/1*nZ4u8QWT6pDaNYvPPtbv-w.png)

![](https://miro.medium.com/v2/resize:fit:736/1*eiroqwaqp5npfz_eivrTlA.png)

![](https://miro.medium.com/v2/resize:fit:736/1*niIjqgGVGCaL-dVYC-a27w.png)

## **Step 9 — now create app-deployment.yml file and check pods and check service**

```bash
/usr/local/bin/kubectl apply -f app-deployment.yaml

/usr/local/bin/kubectl get pods

/usr/local/bin/kubectl get svc
```

![](https://miro.medium.com/v2/resize:fit:736/1*V_2x1Dl80JQmNMkDE0Tafw.png)

![](https://miro.medium.com/v2/resize:fit:736/1*hRwbqE0ebmtnkNpkMLWHqw.png)

now check **minikube ip** as,

```bash
/usr/local/bin/minikube ip
```

## **PORT-FORWARDING**

Port forwarding is a networking technique used to redirect network traffic from one port on a host to another port on a different host or the same host. In the context of Kubernetes, port forwarding allows you to access services running inside a Kubernetes cluster from your local machine or another remote host.

```bash
/usr/local/bin/kubectl port-forward --address 0.0.0.0 svc/springboot-crud-svc 8080:8080 &
```

![](https://miro.medium.com/v2/resize:fit:736/1*uHfR-a4k69dTgIQKPUhaEQ.png)

## **Step 10** — go to **POSTMAN** and check the methods you get replay

Now go to the database in the server and check the entries done by you in the SQL database.

```bash
/usr/local/bin/kubectl exec -it <mysql_pod_name>/bin/bash
```

**step 11 — Now we will open the Dashboard of K8S. Inside EC2 our minikube is running so we are setting a proxy for all the local address.The proxy server is started on port 8001.**

```bash
/usr/local/bin/kubectl proxy --address='0.0.0.0' --accept-hosts='^*$'
```

![](https://miro.medium.com/v2/resize:fit:736/1*zNr_s2M15kfdMt3dErvuQA.png)

**Now open another terminal and run below command.**

```bash
/usr/local/bin/minikube dashboard
```

![](https://miro.medium.com/v2/resize:fit:736/1*uNdt2tyvKRxVURaNjP-jog.png)

```bash
http://127.0.0.1:34927/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
change the IP address to your IP address and port mention as 8001

e.g http://54.190.118.228:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```

So you can access the k8s resources on dashboard as ,

![](https://miro.medium.com/v2/resize:fit:736/1*0pLPd-WINJetavpNiEGy5w.png)

![](https://miro.medium.com/v2/resize:fit:736/1*F-KVuk3ST5Yoa6WQUiVdmg.png)

![](https://miro.medium.com/v2/resize:fit:736/1*yImdvieZ0FCD7KA4g4N6tA.png)

### If you like this article, please share with others. ❤️
