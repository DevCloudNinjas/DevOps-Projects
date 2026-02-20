# Kubernetes – Architecture and main components overview

### Architecture – an overview

In general, Kubernetes cluster components looks like next:

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--W9L6w5JE--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/maxresdefault.jpg)](https://rtfm.co.ua/wp-content/uploads/2019/07/maxresdefault.jpg)

Or a bit more simple one:

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--76OEflDH--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/API-server-overview.png)](https://rtfm.co.ua/wp-content/uploads/2019/07/API-server-overview.png)

The cluster itself consists of one or more *Master Nodes* and one or more *Worker Nodes*.

#### **Master Node**

Services running on a Master Node are called “[*Kubernetes Control Plane*](https://kubernetes.io/docs/concepts/#kubernetes-control-plane)” (excluding `etcd`), and the Master Node is used for administrative tasks only, while containers with your services will be created on a Worker Node(s).

##### Kubernetes core services aka Kubernetes Control Plane

* [Kubernetes Master Components: Etcd, API Server, Controller Manager, and Scheduler](https://medium.com/jorgeacetozi/kubernetes-master-components-etcd-api-server-controller-manager-and-scheduler-3a0179fc8186)
    

On the Master Node, there are three main Kubernetes components which make the whole cluster working:

* [`kube-apiserver`](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)
    
    * the main entrypoint for all requests to the cluster, for example `kubectl` commands will be sent as an API-requests into the [`kube-apiserver`](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/) on the Master Node
        
    * the API server serves all REST-requests, validates them and sends them to the `etcd` (API server is the only one service which talks to the `etcd` – all other components will speak to the API itself, and API serer in its turn will update data in the `etcd`, see the [*Components interaction*](https://rtfm.co.ua/en/?p=21104#Components_interaction))
        
    * the API server is also responsible for authentification and authorization
        
* [`kube-scheduler`](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/)
    
    * makes a decision about which worker node w will be used for a new Pod creation (see. [*Pod*](https://rtfm.co.ua/en/?p=21104#Pod)) depending on resources requested and nodes usage
        
* [`kube-controller-manager`](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)
    
    * a daemon for [Controllers](https://kubernetes.io/docs/concepts/overview/components/#kube-controller-manager) such as *Replication Controller*, *Endpoints Controller,* and *Namespace Controller*
        
    * periodically compares a cluster state via API server and applies necessary changes
        
    * also used for the Linux Namespaces (see the [What is: Linux namespaces, примеры PID и Network namespaces](https://rtfm.co.ua/what-is-linux-namespaces-primery-na-c-clone-pid-i-net-namespaces/), *Rus*) creation and management and garbage collection
        

##### `etcd`

* [etcd.io](https://etcd.io/)
    

Is a *key:value* storage used by Kubernetes for [service discovery](https://en.wikipedia.org/wiki/Service_discovery) and configuration management.

Also, it keeps a cluster’s *current* and *desired* states: if K8s will find distinguishes between those states – it will apply the *desired* state to make it the *current* state.

#### **Worker Node**

Worker Node (previously known as a *minion*) – a virtual or bare-metal server with Kuberners components to create and manage Pods (see [*Pod*](https://rtfm.co.ua/en/?p=21104#Pod)).

Those components are:

* [`kubelet`](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/): the main Kubernetes component on each cluster’s node which speaks to the API server, to check if there are new Pods to be created on the current Worker Node
    
    * it communicates to a Docker daemon (or other containers system like [`rkt`](https://coreos.com/rkt/) or [`containerd`](https://containerd.io/)) via its API to create and manage containers
        
    * after any changes in a Pod on a Node – will send them to the API server, which in its turn will save them to the `etcd` database
        
    * performs containers monitoring
        
* [`kube-proxy`](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/): like a reverse-proxy service to forwarding requests to an appropriate service or applications inside a Kubernetes private network
    
    * uses [IPTABLES](https://rtfm.co.ua/linux-iptables-rukovodstvo-chast-1-osnovy-iptables/) by default (you can check existing rules by the `kubectl -n kube-system exec -ti kube-proxy-5ctt2 -- iptables --table nat --list` command)
        
    * see. [Understanding Kubernetes Kube-Proxy](https://supergiant.io/blog/understanding-kubernetes-kube-proxy/)
        

#### **Components interaction**

Example when a new Pod created:

1. `kubectl` will send a request to the API server
    
2. the API server will validate it and send to the `etcd`
    
3. `etcd` will reply to the API that requests accepted and saved in a database
    
4. the API server will talk to the `kube-scheduler`
    
5. `kube-scheduler` will choose a Worker Node to create a new Pod and sends this information back to the API server
    
6. the API server will send this information to the `etcd`
    
7. `etcd` will reply it accepted and saved data
    
8. the API server talks to the `kubelet` on a chosen Worker Node
    
9. `kubelet` will talk to the Docker daemon (or another [container runtime](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) used) via its API to create a new container
    
10. `kubelet` will send information about new Pod back to the API server
    
11. the API server will update information in the `etcd`
    

### **Kubernetes abstractions**

Above we spoke about more or less “touchable” things such as virtual machines, networks, IP-addresses and so on.

But the Kubernetes itself is just a big piece of an… abstraction, placed upon a physical or virtual infrastructure.

Thus, Kubernetes has a lot of own objects which are abstract or logical Kubernete’s components.

#### **Pod**

The Pod – main logical unit in a Kubernetes cluster.

Inherently, Pod is kind of a virtual machine inside the Kubernetes cluster: it has own private IP, hostname, shared volumes etc (see. [*Volumes*](https://rtfm.co.ua/en/?p=21104#Volumes)).

A Pod is a deployment unit (see [*Deployment*](https://rtfm.co.ua/en/?p=21104#Deployment)) and inside of this “virtual machine” one or more containers will be created, which are tied by a common goal and which are a logical application with one or more processes running.

Each such a Pod is designated to run and serve an only one copy of an application: if you’ll want to make a horizontal scaling – you need to use a dedicated pod per each Worker Node.

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--0TTQJFiY--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190719_141733.png)](https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190719_141733.png)

Such a nodes group called *Replicated Pods* and are managed by a dedicated controller (see [*Controllers*](https://rtfm.co.ua/?p=21053#Conrtollers)).

In doing so containers itself are not the Kubernetes cluster objects and they are not managed by the Kubernetes directly, instead – Kubernetes manages Pods, while containers inside of this Pod shares its namespaces including IP addresses and ports and can communicate to each other via *localhost* (because of Pod is like a VM).

A Pod’s template example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
    type: front-app
spec:
  containers:
  - name: nginx-container
    image: nginx
```

### **Services**

**Links**:

* [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
    
* [Kubernetes Services: A Beginner’s Guide](https://www.bmc.com/blogs/kubernetes-services/)
    
* [Kubernetes – Services Explained](https://www.youtube.com/watch?v=5lzUpDtmWgM)
    

Services in the first turn are everything about networking in a Kubernetes cluster.

They are used for communications between an application’s components inside and outside of it.

Basically, services are the same Kubernetes objects as [*Pod*](https://rtfm.co.ua/?p=21053#Pod), [*ReplicaSets*](https://rtfm.co.ua/?p=21053#ReplicaSet), [*DaemonSet*](https://rtfm.co.ua/?p=21053#DaemonSet) are, and you can imagine a Service like a dedicated virtual machine inside of a cluster’s Node.

They can be displayed as the next:

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--5mGTA4J2--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190719_161337.png)](https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190719_161337.png)

Here is a user who connects to a frontend application via one Service, then this frontend talks to two backend applications using two additional Services, and backends communicates to a database service via other one Service.

##### `ClusterIP`

Will open access to an application via a cluster’s internal IP, thus will be accessible from within the cluster itself.

Is the default Service type.

##### `NodePort`

This Service type will open access to an application using a Worker Node’s static IP.

Also, automatically will create a `ClusterIP` service for the application to route traffic from the `NodePort`.

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--RZ0On6_7--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190722_110641.png)](https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190722_110641.png)

Here:

* *30008* – an external port on a Worker Node which can be used to connect to the `NodePort` service, must be in the 30000 – 32767 ports range
    
* `NodePort` service with the `ClusterIP`, own port (*Port*) and IP from the `serviceSubnet` block
    
* Pod with an application inside – Pod will accept new connections to its port 80 (*TargetPort*) and has an IP from the `podSubnet` block
    

Those networks can be found using the `kubeadm config view` command:

```yaml
root@k8s-master:~# kubeadm config view
apiServer:
extraArgs:
authorization-mode: Node,RBAC
timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta2
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns:
type: CoreDNS
etcd:
local:
dataDir: /var/lib/etcd
imageRepository: k8s.gcr.io
kind: ClusterConfiguration
kubernetesVersion: v1.15.0
networking:
dnsDomain: cluster.local
podSubnet: 10.244.0.0/16
serviceSubnet: 10.96.0.0/12
scheduler: {}
```

And again – you can imagine a Service like another one VM inside of your Worker Node, in the same way as about Pods.

A `NodePort` service’s template example:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-svc
spec:
  type: NodePort
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008
  selector:
    app: my-app
    type: front-app
```

##### Service, Pod, labels, selectors

* [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
    

To make a Service distinguish which Pod has to be used to route traffic to – the `Labels` и `Selectors` are used.

In the pod’s template example above we added labels for our application:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
    type: front-app
spec:
  containers:
  - name: nginx-container
    image: nginx
```

Here it is – the *labels*:

```yaml
...
  labels: 
    app: my-app
```

Then in a Service’s description – we are using *selectors*:

```yaml
...
  selector:
    app: my-app
```

Thus if a cluster has multiple Pods with such a label – then a Service will try to route traffic to all of them:

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--Bf7_qfce--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190722_113024.png)](https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190722_113024.png)

In case if an application placed on multiple Worker Nodes – then a `NodePort` service will be spread between all those nodes and *30008* port will be opened on every such a node.

Thus, you can access an application via a `NodePort` service using a Public IP of any Worker Node used:

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--b3jbYMhy--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190722_113433.png)](https://rtfm.co.ua/wp-content/uploads/2019/07/Screenshot_20190722_113433.png)

##### `LoadBalancer`

* [Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/#loadbalancer)
    
* [Cloud Providers](https://kubernetes.io/docs/concepts/cluster-administration/cloud-providers/)
    
* [Using Kubernetes LoadBalancer Services on AWS](https://blog.giantswarm.io/load-balancer-service-use-cases-on-aws/)
    

Will create a cloud provider’s Load Balancer, for example – [AWS ALB](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html).

Worker Nodes will be attached to this Load Balancer, and traffic will be routed via internal `LoadBalancer` service to a node’s `NodePort` service.

`NodePort` and `ClusterIP` will be created automatically.

##### `ExternalName`

Will tie the Service to its `externalName` field value to return its CNAME value.

An `ExternalName` service template example:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-google-svc
spec:
  type: ExternalName
  externalName: google.com
```

After it will be created – you can reach it from any Pod via this Service name, for example, *my-google-svc* as per the template example above:

```bash
root@k8s-master:~# kubectl exec -it my-pod -- dig my-google-svc.default.svc.cluster.local +short
google.com.
74.125.193.101
...
```

#### Volumes

* [Volumes](https://kubernetes.io/docs/concepts/storage/volumes)
    
* [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
    
* [Kubernetes Volumes Guide](https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-volumes-example-nfs-persistent-volume.html)
    

Data in containers is an ephemeral, i.e. if a container will be recreated by the `kubelet` – then all data from the old container will be lost.

Also, multiple containers inside of the same Pod can use shared data.

The `Volumes` concept in the Kubernetes is similar to the Docker’s solution just with much more features.

For example, Kubernete’s Volumes supports various drivers to mount volumes to Pods, like [awsElasticBlockStore](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore), [hostPath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath), [nfs](https://kubernetes.io/docs/concepts/storage/volumes/#nfs), etc.

#### Namespaces

* [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
    
* [Share a Cluster with Namespaces](https://kubernetes.io/docs/tasks/administer-cluster/namespaces/)
    
* [What is: Linux namespaces, примеры PID и Network namespaces](https://rtfm.co.ua/what-is-linux-namespaces-primery-na-c-clone-pid-i-net-namespaces/)
    

*Namespace* in the Kubernetes is kind of a dedicated cluster inside of your existing cluster with its own set of namespaces for networking, disks/volumes, processes and so on.

The main idea behind the Namespaces is to dedicate working environments, users and can be used to set resources usage limits – CPU, memory, etc. See [*Resource Quotas*](https://kubernetes.io/docs/concepts/policy/resource-quotas/).

The Namespaces also used in the Kubernetes DNS service to create an URL in a *..svc.cluster.local* view.

Most of the Kubernetes resources live in such a Namespaces, you can list them by the:

```yaml
$ kubectl api-resources --namespaced=true
```

To list resources living outside of any Namespace – use the next command:

```yaml
$ kubectl api-resources --namespaced=false
```

#### Controllers

A *Controller* in the Kubernetes are some continuously working process, which communicates to the API server and checks the current state of a cluster and makes necessary changes to make the *current* state to be equal to the *desired* state.

Besides the standard Controllers – you can create your own, see [How to Create a Kubernetes Custom Controller Using client-go](https://itnext.io/how-to-create-a-kubernetes-custom-controller-using-client-go-f36a7a7536cc).

##### `ReplicaSet`

* [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
    
* [Key Kubernetes Concepts](https://towardsdatascience.com/key-kubernetes-concepts-62939f4bc08e)
    
* [Kubernetes KnowHow – Working With ReplicaSet](https://dzone.com/articles/kubernetes-knowhow-working-with-replicaset)
    
* [Знакомство с Kubernetes. Часть 4: Реплики (ReplicaSet)](https://ealebed.github.io/posts/2018/%D0%B7%D0%BD%D0%B0%D0%BA%D0%BE%D0%BC%D1%81%D1%82%D0%B2%D0%BE-%D1%81-kubernetes-%D1%87%D0%B0%D1%81%D1%82%D1%8C-4-replicaset/) (*Rus*)
    

`ReplicaSet` is created by the `Deployment` and the main goal of the `ReplicaSet` is to create and scale Pods.

`ReplicaSet` is the next generation of the [`ReplicationController`](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/) and can use multiple selectors (see [Service, Pod, labels, selectors](https://rtfm.co.ua/en/?p=21104#Service_Pod_labels_selectors)).

It’s recommended to use `Deployment` instead of creating `ReplicaSet` objects directly.

A `ReplicaSet` template example:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-nginx-rc
  labels:
    app: my-nginx-rc-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx-rc-app
  template: # PODs template
    metadata:
      labels: 
        app: my-nginx-rc-app
    spec:
      containers:
      - name: nginx-container
        image: nginx
```

##### `Deployment`

* [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
    
* [Знакомство с Kubernetes. Часть 5: Развертывания (Deployments)](https://ealebed.github.io/posts/2018/%D0%B7%D0%BD%D0%B0%D0%BA%D0%BE%D0%BC%D1%81%D1%82%D0%B2%D0%BE-%D1%81-kubernetes-%D1%87%D0%B0%D1%81%D1%82%D1%8C-5-deployments/) (*Rus*)
    
* [Kubernetes Deployments: The Ultimate Guide](https://semaphoreci.com/blog/kubernetes-deployment/)
    
* [Deployment Strategies](https://www.weave.works/blog/kubernetes-deployment-strategies)
    
* [Kubernetes Deployment Tutorial For Beginners](https://devopscube.com/kubernetes-deployment-tutorial/)
    
* [Managing Kubernetes Deployments](https://supergiant.io/blog/managing-kubernetes-deployments/)
    
* [K8s: Deployments vs StatefulSets vs DaemonSets](https://medium.com/stakater/k8s-deployments-vs-statefulsets-vs-daemonsets-60582f0c62d4)
    

The *Deployment* controller will apply changes to Pods and `RelicaSets` and currently is the most used resource in the Kubernetes to deploy applications.

It’s mainly used for *stateless* applications, but you can attach a [*Persistent Volume*](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) and use it as a *stateful* application.

See [stateful](https://whatis.techtarget.com/definition/stateful-app) vs [stateless](https://whatis.techtarget.com/definition/stateless-app).

During a `Deployment` creation – it will create a `ReplicaSet` object which in its turn will create and manage Pods for this `Deployment`.

`Deployment` used to:

* update Pods – `Deployment` will create a new `ReplicaSet` and will update a deployment’s revision number (`deployment.kubernetes.io/revision: ""` which is used by a `ReplicaSet`)
    
* roll-back a deployment if it was unsuccessful using revisions
    
* Pods scaling and autoscaling can be done using Deployments (`kubectl scale` и `kubectl autoscale`, see [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/))
    
* can be used for the canary deployments (see the [Intro to deployment strategies: blue-green, canary, and more](https://dev.to/mostlyjason/intro-to-deployment-strategies-blue-green-canary-and-more-3a3))
    

[![](https://res.cloudinary.com/practicaldev/image/fetch/s--to_dDoP6--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://rtfm.co.ua/wp-content/uploads/2019/07/07751442-deployment.png)](https://rtfm.co.ua/wp-content/uploads/2019/07/07751442-deployment.png)

Beside of the `Deployments` the [kubectl rolling-update](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#rolling-update) can be used, although `Deployments` is the recommended way.

##### `StatefulSet`

* [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
    
* [Updating StatefulSets](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/#updating-statefulsets)
    

`StatefulSet` are used to manage stateful applications.

It will create a Pod with a unique name directly instead of the `ReplicaSet`. Because of this when using `StatefulSet` you have no ability to run a deployment roll-back. Instead, you can delete a resource or make its scaling.

During the `StatefulSet` updates – a [RollingUpdate](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/#updating-statefulsets) will be applied to all nodes.

##### `DaemonSet`

* [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
    

`DaemonSet` is used when you need to run an application over all nodes in your cluster – not only on the Worker Nodes. If a new Pod will be created after `DaemonSet` – an application will be deployed on this new Pod as well.

`DaemonSet` is the perfect desition to run applications which has to be present on every node, for example – monitoring, logs collectors, etc.

During this, some nodes will decline to create Pods on them, such as the Master Node for example, because it has the `node-role.kubernetes.io/master:NoSchedule` set (see [Taints and Tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/)):

```yaml
$ kubectl describe node k8s-master | grep Taint
Taints:             node-role.kubernetes.io/master:NoSchedule
```

Respectively, when creating a `DaemonSet` which has to create Pods on the Master Node too you have to specify `tolerations`.

Such a `DaemonSet` template example:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-nginx-ds
spec:
  selector:
    matchLabels:
      app: my-nginx-pod
  template: 
    metadata:
      labels: 
        app: my-nginx-pod
    spec:
      tolerations:
      - effect: NoSchedule
        operator: Exists
      containers:
      - name: nginx-container
        image: nginx
        ports:
        - containerPort: 80
```

During `DaemonSet` update – the [RollingUpdate](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/#updating-statefulsets) for all pods will be applied.

##### `Job`

* [Jobs – Run to Completion](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/)
    
* [Однократные задачи в Kubernetes](https://dotsandbrackets.com/one-off-kubernetes-jobs-ru/)
    
* [Working with Kubernetes Jobs](https://medium.com/coryodaniel/working-with-kubernetes-jobs-848914418)
    

`Job` in the Kubernetes indented to be used to create a Pod which will execute the only one task, once after it will finish a task execution – this Pod will be stopped.

Such a `Job` can create one or more Pods, can run your tasks in parallel, execute this task specified number of attempts.

A `Job` template example:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-example
spec:
  completions: 2
  parallelism: 2
  template:
    metadata:
      name: counter
    spec:
      containers:
      - name: counter
        image: ubuntu
        command: ["bash"]
        args: ["-c",  "for i in {1..10}; do echo $i; done"]
      restartPolicy: Never
```

###### `CronJob`

Similar to the `Job` but intended to run tasks by a schedule – check the `schedule` parameter below:

```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: cronjob-example
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      completions: 2
      parallelism: 2     
      template:
        metadata:
          name: counter
        spec:
          containers:
          - name: counter
            image: ubuntu
            command: ["bash"]
            args: ["-c",  "for i in {1..10}; do echo $i; done"]
          restartPolicy: Never
```

### **Useful links**

#### **Common**

* [Concepts](https://kubernetes.io/docs/concepts/?origin_team=T08E6NNJJ)
    
* [Key Kubernetes Concepts](https://towardsdatascience.com/key-kubernetes-concepts-62939f4bc08e)
    
* [Kubernetes Master Components: Etcd, API Server, Controller Manager, and Scheduler](https://medium.com/jorgeacetozi/kubernetes-master-components-etcd-api-server-controller-manager-and-scheduler-3a0179fc8186)
    
* [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/?origin_team=T08E6NNJJ)
    
* [Kubernetes](https://ealebed.github.io/tags/kubernetes/) (*все посты по тегу, интересный блог у человека*)
    
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/?origin_team=T08E6NNJJ)
    
* [Taints and Tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/?origin_team=T08E6NNJJ)
    

#### **Networking**

* [Service](https://kubernetes.io/docs/concepts/services-networking/service/?origin_team=T08E6NNJJ)
    
* [Cloud Providers](https://kubernetes.io/docs/concepts/cluster-administration/cloud-providers/?origin_team=T08E6NNJJ)
    
* [Understanding Kubernetes Kube-Proxy](https://supergiant.io/blog/understanding-kubernetes-kube-proxy/)
    
* [Kubernetes Services: A Beginner’s Guide](https://www.bmc.com/blogs/kubernetes-services/)
    
* [Kubernetes – Services Explained](https://www.youtube.com/watch?v=5lzUpDtmWgM)
    
* [Using Kubernetes LoadBalancer Services on AWS](https://blog.giantswarm.io/load-balancer-service-use-cases-on-aws/)
    

#### **Deployments**

* [Kubernetes Deployment Strategies](https://www.weave.works/blog/kubernetes-deployment-strategies)
    
* [Kubernetes Deployments: The Ultimate Guide](https://semaphoreci.com/blog/kubernetes-deployment/)
    
* [Kubernetes Deployment Tutorial For Beginners](https://devopscube.com/kubernetes-deployment-tutorial/)
    
* [Managing Kubernetes Deployments](https://supergiant.io/blog/managing-kubernetes-deployments/)
    
* [K8s: Deployments vs StatefulSets vs DaemonSets](https://medium.com/stakater/k8s-deployments-vs-statefulsets-vs-daemonsets-60582f0c62d4)

### If you like this article, please share with others. ❤️
