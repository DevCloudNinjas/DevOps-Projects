# Kubernetes for everyone ☸️

![kubernetes](https://imgur.com/12s2Bi8.png)

# Kubernetes

Kubernetes is the `de facto` standard for running containerized applications.

> Kubernetes (K8s) is an open-source system for `automating deployment`, `scaling`, and `management` of containerized applications.

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--RWDsJZoQ--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://thepracticaldev.s3.amazonaws.com/i/idtqaj43wbzw5704fwdb.png)](https://res.cloudinary.com/practicaldev/image/fetch/s--RWDsJZoQ--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://thepracticaldev.s3.amazonaws.com/i/idtqaj43wbzw5704fwdb.png)

**Kubernetes** makes it easy to deploy and run containerized applications. **Kubernetes** is simple to use.

**Kubernetes** is complex to understand because it provides a huge set of options to make your deployment easier.

Aptly named, **Kubernetes** is a pilot (or) **helmsman** that helps you to sail the container world. **Kubernetes** is a portable and extensible system built by the community for the community.

As Kelsey, correctly quotes

> Kubernetes does the things that the very best system administrator would do automation, failover, centralized logging, monitoring. It takes what we’ve learned in the DevOps community and makes it default, out of the box.

In order to work with Kubernetes, it is very important to understand

* How Kubernetes works?
    
* How Kubernetes is architected?
    
* What are the various components in Kubernetes?
    

Let us start hacking on Kubernetes.

## **How does Kubernetes work?**

The Kubernetes run in a highly available cluster mode. Each Kubernetes cluster consists of one or more master node and a few worker nodes.

[![Alt Text](https://res.cloudinary.com/practicaldev/image/fetch/s--cB_xIijv--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/gkc90lkkd9cdfqjx2i2m.png)](https://res.cloudinary.com/practicaldev/image/fetch/s--cB_xIijv--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/gkc90lkkd9cdfqjx2i2m.png)

### **Master Node**

The master node consists of an API server, Scheduler, Controllers, etcd. This node is called the `control plane` of Kubernetes. This control plane is the `brain` of Kubernetes.

That is the control plane is responsible for all the actions inside Kubernetes.

[![Alt Text](https://res.cloudinary.com/practicaldev/image/fetch/s--AIO49EkR--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/wgenne5f9y8a25shgb29.png)](https://res.cloudinary.com/practicaldev/image/fetch/s--AIO49EkR--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/wgenne5f9y8a25shgb29.png)

Via the `API server`, we can instruct the Kubernetes or get information from the Kubernetes.

The `Scheduler` is responsible for scheduling the pods.

The `controllers` are responsible for running the resource controllers.

The `etcd` is a storage for the Kubernetes. It is key-value storage.

### **Node**

[![Alt Text](https://res.cloudinary.com/practicaldev/image/fetch/s--mQTCJBI0--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/g9w3a7g1ytmxz83m46n3.png)](https://res.cloudinary.com/practicaldev/image/fetch/s--mQTCJBI0--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/g9w3a7g1ytmxz83m46n3.png)

The worker nodes have a Kubelet and proxy.

The Kubelets are the actual workhorse and the Kube-proxy handles the networking.

#### **Working**

[![Alt Text](https://res.cloudinary.com/practicaldev/image/fetch/s--phm0eKIo--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/h0hxgch8ape716dwxl0t.png)](https://res.cloudinary.com/practicaldev/image/fetch/s--phm0eKIo--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/i/h0hxgch8ape716dwxl0t.png)

We provide the `yaml` file to the Kubernetes cluster through `kubectl apply` command.

The `apply` command calls the API server, which will send the information to the `controller` and simultaneously stores the information to the `etcd`.

The `etcd` then replicate this information across multiple nodes to survive any node failure.

The `controller` will check whether the given state matches the desired state. If it is not it initiates the pod deployment, by sending the information to the `scheduler`

The checks are called as the **reconciliation loop** that runs inside the Kubernetes. The job of this loop is to validate whether the state requested is maintained correctly. If the expected state and actual states mismatch this loop will do the necessary actions to convert the actual state into the expected state.

The `scheduler` has a queue inside. Once the message is received in the queue.

The `scheduler` will then invoke the kubelet to do the intended action such as deploying the container.

This is a 10000 feet bird view of how Kubernetes does the deployment.

There are various components inside the Kubernetes. Let us take a look at what are they and how are they useful.

## **Components of Kubernetes**

### **Pods**

> In general terms, pods are nothing but a group of dolphins or whales.

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--L_UYK4z0--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://thepracticaldev.s3.amazonaws.com/i/wri3njxsoku0z6na9zj8.png)](https://res.cloudinary.com/practicaldev/image/fetch/s--L_UYK4z0--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://thepracticaldev.s3.amazonaws.com/i/wri3njxsoku0z6na9zj8.png)

Similarly, in Kubernetes world, `pods` are a group of containers living together. A pod may have one or more containers in it.

The `pod` is the smallest unit of deployment in Kubernetes. Usually, the containers that cannot live outside the scope of another container are grouped to form a pod.

This is how you define a pod in Kubernetes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 3600']
```

* *apiVersion* denotes the Kubernetes cluster which version of API to use when parsing and executing this file.
    
* *kind* defines what is the **kind** of Kubernetes object, this file will refer to.
    
* *metadata* includes all the necessary metadata to identify the Pod.
    
* *spec* includes the container information.
    

### **Deployments**

While pods are the unit of deployment. For an application to work, it needs one or more pods. Kubernetes considers this entire set as deployment.

Thus deployment is recorded information about pods. Kubernetes uses this deployment information to manage and monitor the applications that are deployed in them.

The below file is the sample deployment file that tells the Kubernetes to create a deployment of `nginx` using the `nginx:1.7.9` container.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

### **Replicasets**

While deployment tells the Kubernetes what containers are needed for your application and how many replicas to run. The `replica sets` are the ones that ensure those replicas are up and running.

ReplicaSet is responsible for managing and monitoring the replicas.

### **StatefulSet**

Often times we will need to have persistent storage or permanent network identifiers or ordered deployment, scaling, and update. During those times we will use `StatefulSets`.

You can define the StatefulSet like below:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx # has to match .spec.template.metadata.labels
  serviceName: "nginx"
  replicas: 3 # by default is 1
  template:
    metadata:
      labels:
        app: nginx # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: k8s.gcr.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```

We mounted the volume and also claimed the volume storage.

### **DaemonSet**

Sometimes you need to run a pod on every node of your Kubernetes cluster. For example, if you are collecting metrics from every node, then we will need to schedule some pods on every node that collects the metrics. We can use DaemonSet for those nodes.

### **Services**

The deployments define the actual state of the application running on the containers. Users will need to access the application or you might need to connect to the container to debug it. Services will help you.

The services are the Kubernetes object that provides access to the containers from the external world or between themselves.

We can define the service like below:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
```

The above `service` maps incoming connections on port `80` to the targetPort `9376`.

> You can consider the services as the load balancer, proxy or traffic router in the world of Kubernetes.

### **Networking**

This is the most important element of Kubernetes. The pods running should be exposed to the network. The containers that are running inside the pods should communicate between themselves and also to the external world.

While service provides a way to connect to the pods, networking determines how to expose these services.

In Kubernetes we can expose the service through the following ways:

* **Load Balancer**
    
    * The Load Balancer provides an external IP through which we can access the pods running inside.
        
    * The Kubernetes will start the services and then `asynchronously` starts a load-balancer.

![](https://res.cloudinary.com/practicaldev/image/fetch/s--ZsEzQUH9--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_800/https://thepracticaldev.s3.amazonaws.com/i/29miv7gkc1bmpz0yfdze.gif)

* **Node Port**
    
    * Each of the services will have a dynamically assigned port.
        
    * We can access the services using the Kubernetes master IP.

![](https://res.cloudinary.com/practicaldev/image/fetch/s--YLZmwUts--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_800/https://thepracticaldev.s3.amazonaws.com/i/pactfmoby255r4pny8iq.gif)

* **Ingress**
    
    * Each of the services will have a separate address.
        
    * These services are then accessed by an ingress controller.
        
    * The ingress controller is not a public IP or external IP.

![](https://res.cloudinary.com/practicaldev/image/fetch/s--yK1H6ka8--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_800/https://thepracticaldev.s3.amazonaws.com/i/09tndignuksgqrjdqlze.gif)

### **Secrets**

Often for the applications, we need to provide passwords, tokens, etc., Kubernetes provides `secrets` object to store and manage the sensitive information. We can create a secret like below:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
stringData:
  config.yaml: |-
    apiUrl: "https://my.api.com/api/v1"
    username: {{username}}
    password: {{password}}
```

## Best practices

> While Kubernetes is an ocean and whatever we have seen is just a drop in it. Since Kubernetes supports a wide range of applications and options, there are various different options and features available.

Few best practices to follow while working with Kubernetes are:

#### **Make smaller YAML**

The `yaml` files are the heart of Kubernetes configuration.

We can define multiple Kubernetes configurations in a single `yaml`. While `yaml` reduces the boilerplate when compared with `JSON`. But still `yaml` files are space-sensitive and error-prone.

So always try to minimize the size of `yaml` files.

For every service, deployment, secrets, and other Kubernetes objects define them in a separate `yaml` file.

> Split your yaml files into smaller files.

The `single responsibility principle` applies here.

#### **Smaller and Fast boot time for images**

Kubernetes automatically restarts the pods when there is a crash or upgrade or increased usage. It is important to have a faster boot time for the images. In order to have a faster boot time, we need to have smaller images.

Alpine images are your friends. Use the Alpine images as the base and then add in components or libraries to the images only when they are absolutely necessary.

> Always remember to have smaller image sizes. Use `builder pattern` to create the images from Alpine images.

#### Healthy - Zombie Process

Docker containers will terminate only when all the processes running inside the container are terminated. The Docker containers will return `healthy` status even when one of the processes is killed. This creates a `Healthy-Zombie` process.

Try to have a single process inside the container. If running a single process is not possible then try to have a mechanism to figure out whether all the required processes are running.

#### Clean up unused resources

In the container world, it is quite common to have unused resources occupying the memory. It is important to ensure the resources are properly cleaned.

#### Think about Requests & Limits

Ensure that requests and limits are properly specified for all the containers.

```yaml
resources:
    requests:
        memory: "100Mi"
        cpu: "100m"
    limits:
        memory: "200Mi"
        cpu: "500m"
```

The `requests` are the limits that the container is guaranteed to get. The `limits` are is the maximum or minimum resource a container is allowed to use.

> Each container in the pod can request and limit their resources.

#### RED / USE pattern

Monitor and manage your services using `RED` pattern.

* Requests
    
* Errors
    
* Duration
    

Track the requests, errors in the response and the duration to receive the response. Based on this information, tweak your service to receive optimum performance.

For the resources, use the `USE` pattern.

* Utilization
    
* Saturation
    
* Errors
    

Monitor the resource utilization and how much the resources are saturated and what are the errors. Based on this information, tweak your resources to optimize resource allocation.

Hopefully, this might have given you a brief overview of `Kubernetes`. Head over [kubernetes.io](https://kubernetes.io/) for more information on Kubernetes.

### **If you like this article, please share with others. ❤️**
