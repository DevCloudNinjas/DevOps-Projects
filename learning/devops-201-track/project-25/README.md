# PACKAGING CONTAINERIZED APPLICATIONS INTO HELM CHARTS

In Project 22, you experienced the use of manifest files to define and deploy resources like pods, deployments, and services into Kubernetes cluster. Here, you will do the same thing except that it will not be passed through `kubectl`. In the real world, Helm is one of the most popular tools used to deploy resources into kubernetes. That is because it has a rich set of features that allows deployments to be packaged as a unit. Rather than have multiple YAML files managed individually - which can quickly become messy.

A Helm chart is a definition of the resources that are required to run an application in Kubernetes. Instead of having to think about all of the various deployments/services/volumes/configmaps/ etc that make up your application, you can use a command like

```
helm install stable/mysql
```
and Helm will make sure all the required resources are installed. In addition you will be able to tweak helm configuration by setting a single variable to a particular value and more or less resources will be deployed. For example, enabling slave for MySQL so that it can have read only replicas.

Behind the scenes, a helm chart is essentially a bunch of YAML manifests that define all the resources required by the application. Helm takes care of creating the resources in Kubernetes (where they don't exist) and removing old resources.

#### Lets begin to gradually walk through how to use Helm (Credit - https://andrewlock.net/series/deploying-asp-net-core-applications-to-kubernetes/) @igor please update the texts as much as possible to reduce plagiarism

1. Parameterising YAML manifests using Helm templates

Let's consider that our Tooling app have been Dockerised into an image called `tooling-app`, and that you wish to deploy with Kubernetes. Without helm, you would create the YAML manifests defining the deployment, service, and ingress, and apply them to your Kubernetes cluster using `kubectl apply`. Initially, your application is version 1, and so the Docker image is tagged as `tooling-app:1.0.0`. A simple deployment manifest might look something like the following:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tooling-app-deployment
  labels:
    app: tooling-app
spec:
  replicas: 3
  strategy: 
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  selector:
    matchLabels:
      app: tooling-app
  template:
    metadata:
      labels:
        app: tooling-app
    spec:
      containers:
      - name: tooling-app
        image: "tooling-app:1.0.0"
        ports:
        - containerPort: 80
```
Now lets imagine that the developers develops another version of the toolin app, version 1.1.0. How do you deploy that? Assuming nothing needs to be changed with the service or other kubernetes objects, it may be as simple as copying the deployment manifest and replacing the image defined in the spec section. You would then re-apply this manifest to the cluster, and the deployment would be updated, performing a [rolling-update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/).

The main problem with this is that all of the values specific to the tooling app – the labels and the image names etc – are mixed up with the entire definition of the manifest.

Helm tackles this by splitting the configuration of a chart out from its basic definition. For example, instead of hard coding the name of your app or the specific container image into the manifest, you can provide those when you install the "chart" (More on this later) into the cluster.

For example, a simple templated version of the tooling app deployment might look like the following:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
  labels:
    app: "{{ template "name" . }}"
spec:
  replicas: 3
  strategy: 
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  selector:
    matchLabels:
      app: "{{ template "name" . }}"
  template:
    metadata:
      labels:
        app: "{{ template "name" . }}"
    spec:
      containers:
      - name: "{{ template "name" . }}"
        image: "{{ .Values.image.name }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 80
```

This example demonstrates a number of features of Helm templates:

The template is based on YAML, with {{ }} mustache syntax defining dynamic sections.
Helm provides various variables that are populated at install time. For example, the {{.Release.Name}} allows you to change the name of the resource at runtime by using the release name. Installing a Helm chart creates a release (this is a Helm concept rather than a Kubernetes concept).
You can define helper methods in external files. The {{template "name"}} call gets a safe name for the app, given the name of the Helm chart (but which can be overridden). By using helper functions, you can reduce the duplication of static values (like tooling-app), and hopefully reduce the risk of typos.

You can manually provide configuration at runtime. The {{.Values.image.name}} value for example is taken from a set of default values, or from values provided when you call helm install. There are many different ways to provide the configuration values needed to install a chart using Helm. Typically, you would use two approaches:

A values.yaml file that is part of the chart itself. This typically provides default values for the configuration, as well as serving as documentation for the various configuration values.

When providing configuration on the command line, you can either supply a file of configuration values using the `-f` flag. We will see a lot more on this later on.


**Now lets setup Helm and begin to use it.**

According to the official documentation [here](https://helm.sh/docs/intro/install/), there are different options to installing Helm. But we will build the source code to create the binary. 

1. [Download the `tar.gz` file from the project's Github release page](https://github.com/helm/helm/releases). Or simply use `wget` to download version `3.6.3` directly

```
wget https://github.com/helm/helm/archive/refs/tags/v3.6.3.tar.gz
```

2. Unpack the `tar.gz`  file
```
tar -zxvf v3.6.3.tar.gz 
```

3. cd into the unpacked directory 
```
cd helm-3.6.3
```
4. Build the source code using `make` utility

```
make build
```

If you do not have `make` installed or for any other reason, you cannot install the tool, simply use the official documentation  [here](https://helm.sh/docs/intro/install/) for other options.

5. Helm binary will be in the `bin` folder. Simply move it to the `bin` directory on your system. You cna check other tools to know where that is. fOr example, check where `pwd` utility is being called from by running `which pwd`. Assuming the output is `/usr/local/bin`. You can move the `helm` binary there.

```
sudo mv bin/helm /usr/local/bin/
```

6. Check that Helm is installed

`helm version`
```
version.BuildInfo{Version:"v3.6+unreleased", GitCommit:"13f07e8adbc57b0e3f96b42340d6f44bdc8d5016", GitTreeState:"dirty", GoVersion:"go1.15.5"}
```

#### Deploy Jenkins with Helm

Before we begin to develop our own helm charts, lets make use of publicly available charts to deploy all the tools that we need.

One of the amazing things about helm is the fact that you can deploy applications that are already packaged from a public helm repository directly with very minimal configuration. An example is **Jenkins**.

1. Visit [Artifact Hub](https://artifacthub.io/packages/search) to find packaged applications as Helm Charts
2. Search for Jenkins
3. Add the repository to helm so that you can easily download and deploy
```
helm repo add jenkins https://charts.jenkins.io
```
4. Update helm repo
```
helm repo update 
```
5. Install the chart 
```
helm install [RELEASE_NAME] jenkins/jenkins --kubeconfig [kubeconfig file]
```
You should see an output like this 

```
NAME: jenkins
LAST DEPLOYED: Sun Aug  1 12:38:53 2021
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
helm ls --kubeconfig [kubeconfig file]
```
Output:
```
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
jenkins default         1               2021-08-01 12:38:53.429471 +0100 BST    deployed        jenkins-3.5.9   2.289.3 
```

7. Check the pods

```
kubectl get pods --kubeconfig [kubeconfig file]
```
Output: 
```
NAME        READY   STATUS    RESTARTS   AGE
jenkins-0   2/2     Running   0          6m14s
```

8. Describe the running pod (review the output and try to understand what you see)
```
kubectl describe pod jenkins-0 --kubeconfig [kubeconfig file]
```

9. Check the logs of the running pod

```
kubectl logs jenkins-0 --kubeconfig [kubeconfig file]
```

You will notice an output with an error

```
error: a container name must be specified for pod jenkins-0, choose one of: [jenkins config-reload] or one of the init containers: [init]
```

This is because the pod has a [Sidecar container](https://www.magalix.com/blog/the-sidecar-pattern) alongside with the Jenkins container. As you can see fromt he error output, there is a list of containers inside the pod `[jenkins config-reload]` i.e `jenkins` and `config-reload` containers. The job of the config-reload is mainly to help Jenkins to reload its configuration without recreating the pod.

Therefore we need to let `kubectl` know, which pod we are interested to see its log. Hence, the command will be updated like:
```
kubectl logs jenkins-0 -c jenkins --kubeconfig [kubeconfig file]
```

10. Now lets avoid calling the `[kubeconfig file]` everytime. Kubectl expects to find the default kubeconfig file in the location `~/.kube/config`. But what if you already have another cluster using that same file? It doesn't make sense to overwrite it. What you will do is to merge all the kubeconfig files together using a kubectl plugin called `[konfig](https://github.com/corneliusweig/konfig)` and select whichever one you need to be active.

      1. Install a package manager for kubectl called [krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/) so that it will enable you to install plugins to extend the functionality of kubectl. Read more about it `[Here](https://github.com/kubernetes-sigs/krew)` 
     
      2. Install the `[konfig plugin](https://github.com/corneliusweig/konfig)` 
          ```
          kubectl krew install konfig
          ```
      3. Import the kubeconfig into the default kubeconfig file. Ensure to accept the prompt to overide.
          ```
          sudo kubectl konfig import --save  [kubeconfig file]
          ```
      4. Show all the contexts - Meaning all the clusters configured in your kubeconfig. If you have more than 1 Kubernetes clusters configured, you will see them all in the output.
          ```
          kubectl config get-contexts
          ```
      5. Set the current context to use for all kubectl and helm commands
          ```
          kubectl config use-context [name of EKS cluster]
          ```
      6. Test that it is working without specifying the `--kubeconfig` flag
          ```
          kubectl get po
          ```
          Output:
          ```
          NAME        READY   STATUS    RESTARTS   AGE
          jenkins-0   2/2     Running   0          84m
          ```
      7. Display the current context. This will let you know the context in which you are using to interact with Kubernetes.
          ```
          kubectl config current-context
          ```

11. Now that we can use `kubectl` without the `--kubeconfig` flag, Lets get access to the Jenkins UI. (*In later projects we will further configure Jenkins. For now, it is to set up all the tools we nee*d)
    1.  There are some commands that was provided on the screen when Jenkins was installed with Helm. See number 5 above. Get the password to the `admin` user
          ```
          kubectl exec --namespace default -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password && echo
          ```
    2. Use port forwarding to access Jenkins from the UI 
          ```
          kubectl --namespace default port-forward svc/jenkins 8080:8080
          ```
          <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project24/Jenkins-Port-forward.png" width="936px" height="550px">
    3. Go to the browser `localhost:8080` and authenticate with the username and password from number 1 above
          <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project24/Jenkins-UI.png" width="936px" height="550px">

#### Now setup the following tools using Helm

This section will be quite challenging for you because you will need to spend some time to research the charts, read their documentations and understand how to get an application running in your cluster by simply running a helm install command.

1. Artifactory
2. Hashicorp Vault
3. Prometheus
4. Grafana
5. Elasticsearch ELK using [ECK](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-install-helm.html)

Succesfully installing all the 5 tools is a great experience to have. But, joining the [Masterclass](darey.io/masterclass) you will be able to see how this should be done end to end.

In the next project, you will have experience;

1. Deploying Ingress Controller
2. Configuring Ingress for all the tools and applications running in the cluster
3. Implementing TLS with applications running inside Kubernetes using Cert-manager



Deploying and Packaging applications into Kubernetes with Helm
============================================

In the previous project, you started experiencing helm as a tool used to deploy an application into Kubernetes. You probably also tried installing more tools apart from Jenkins.

In this project, you will experience deploying more DevOps tools, get familiar with some of the real world issues faced during such deployments and how to fix them. You will learn how to tweak helm values files to automate the configuration of the applications you deploy. Finally, once you have most of the DevOps tools deployed, you will experience using them and relate with the DevOps cycle and how they fit into the entire  ecosystem.

Our focus will be on the. 

1. Artifactory
2. Ingress Controllers
3. Cert-Manager

Then you will attempt to explore these on your own.

4. Prometheus
5. Grafana
6. Elasticsearch ELK using [ECK](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-install-helm.html)

For the tools that require paid license, don't worry, you will also learn how to get the license for free and have true experience exactly how they are used in the real world.

Lets start first with Artifactory. What is it exactly?

Artifactory is part of a suit of products from a company called [Jfrog](https://jfrog.com/). Jfrog started out as an artifact repository where software binaries in different formats are stored. Today, Jfrog has transitioned from an artifact repository to a DevOps Platform that includes CI and CD capabilities. This has been achieved by offering more products in which **Jfrog Artifactory** is part of. Other offerings include 
      
  - JFrog Pipelines -  a CI-CD product that works well with its Artifactory repository. Think of this product as an alternative to Jenkins.
  - JFrog Xray - a security product that can be built-into various steps within a JFrog pipeline. Its job is to scan for security vulnerabilities in the stored artifacts. It is able to scan all dependent code.

In this project, the requirement is to use Jfrog Artifactory as a private registry for the organisation's Docker images and Helm charts. This requirement will satisfy part of the company's corporate security policies to never download artifacts directly from the public into production systems. We will eventually have a CI pipeline that initially pulls public docker images and helm charts from the internet, store in artifactory and scan the artifacts for security vulnerabilities before deploying into the corporate infrastructure. Any found vulnerabilities will immediately trigger an action to quarantine such artifacts.

Lets get into action and see how all of these work.

## Deploy Jfrog Artifactory into Kubernetes

The best approach to easily get Artifactory into kubernetes is to use helm.

1. Search for an official helm chart for Artifactory on [Artifact Hub](https://artifacthub.io/)

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/search-artifactory-on-artifact-hub.png" width="936px" height="550px">
2. Click on **See all results**
3. Use the filter checkbox on the left to limit the return data. As you can see in the image below, "Helm" is selected. In some cases, you might select "Official". Then click on the first option from the result.

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/Select-artifactory-chart.png" width="936px" height="550px">
4. Review the Artifactory page

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/Artifactory-helm-page.png" width="936px" height="550px">
5. Click on the install menu on the right to see the installation commands.
   
    <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/click-install.png" width="936px" height="550px">
6. Add the jfrog remote repository on your laptop/computer

```
helm repo add jfrog https://charts.jfrog.io
```

7. Create a namespace called `tools` where all the tools for DevOps will be deployed. (In previous project, you installed Jenkins in the default namespace. You should uninstall Jenkins there and install in the new namespace)

```
kubectl create ns tools
```

8. Update the helm repo index on your laptop/computer

```
helm repo update
```

9. Install artifactory

```
helm upgrade --install artifactory jfrog/artifactory --version 107.38.10 -n tools
```

```
Release "artifactory" does not exist. Installing it now.
NAME: artifactory
LAST DEPLOYED: Sat May 28 09:26:08 2022
NAMESPACE: tools
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Congratulations. You have just deployed JFrog Artifactory!

1. Get the Artifactory URL by running these commands:

   NOTE: It may take a few minutes for the LoadBalancer IP to be available.
         You can watch the status of the service by running 'kubectl get svc --namespace tools -w artifactory-artifactory-nginx'
   export SERVICE_IP=$(kubectl get svc --namespace tools artifactory-artifactory-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
   echo http://$SERVICE_IP/

2. Open Artifactory in your browser
   Default credential for Artifactory:
   user: admin
   password: password
```


**NOTE:** 

- We have used `upgrade --install` flag here instead of `helm install artifactory jfrog/artifactory` This is a better practice, especially when developing CI pipelines for helm deployments. It ensures that helm does an upgrade if there is an existing installation. But if there isn't, it does the initial install. With this strategy, the command will never fail. It will be smart enough to determine if an upgrade or fresh installation is required.
- The helm chart version to install is very important to specify. So, the version at the time of writing may be different from what you will see from Artifact Hub. So, replace the version number to the desired. You can see all the versions by clicking on "see all" as shown in the image below.
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/click-versions.png" width="936px" height="550px">
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/see-versions.png" width="936px" height="550px">

The output from the installation already gives some Next step directives.

### Getting the Artifactory URL

Lets break down the first *Next Step*. 

1. The artifactory helm chart comes bundled with the Artifactory software, a PostgreSQL database and an Nginx proxy which it uses to configure routes to the different capabilities of Artifactory. Getting the pods after some time, you should see something like the below.

     <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/pods.png" width="936px" height="550px">
2. Each of the deployed application have their respective services. This is how you will be able to reach either of them.
     <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/services.png" width="936px" height="550px">
3. Notice that, the Nginx Proxy has been configured to use the service type of `LoadBalancer`. Therefore, to reach Artifactory, we will need to go through the Nginx proxy's service. Which happens to be a load balancer created in the cloud provider. Run the `kubectl` command to retrieve the Load Balancer URL.
   
   ```
   kubectl get svc artifactory-artifactory-nginx -n tools
   ```
   
4. Copy the URL and paste in the browser
   
    <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/jfrog-page.png" width="936px" height="550px">
5. The default username is `admin` 
6. The default password is `password`
<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/jfrog-getting-started.png" width="936px" height="550px">

### How the Nginx URL for Artifactory is configured in Kubernetes

Without clicking further on the **Get Started** page, lets dig a bit more into Kubernetes and Helm. How did Helm configure the URL in kubernetes?

Helm uses the `values.yaml` file to set every single configuration that the chart has the capability to configure. THe best place to get started with an off the shelve chart from artifacthub.io is to get familiar with the `DEFAULT VALUES`


- click on the `DEFAULT VALUES` section on Artifact hub 
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/click-default-values.png" width="936px" height="550px">
- Here you can search for key and value pairs
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/search-values.png" width="936px" height="550px">
- For example, when you type `nginx` in the search bar, it shows all the configured options for the nginx proxy. 
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/nginx-values.png" width="936px" height="550px">
- selecting `nginx.enabled` from the list will take you directly to the configuration in the YAML file.
    <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/nginx-values-yaml.png" width="936px" height="550px">
- Search for `nginx.service` and select `nginx.service.type`
     <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/nginx-service.png" width="936px" height="550px">
- You will see the confired type of Kubernetes service for Nginx. As you can see, it is `LoadBalancer` by default
     <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/nginx-service-type.png" width="936px" height="550px">
- To work directly with the `values.yaml` file, you can download the file locally by clicking on the download icon.
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/download-values.png" width="936px" height="550px">
### Is the Load Balancer Service type the Ideal configuration option to use in the Real World?

Setting the service type to **Load Balancer** is the easiest way to get started with exposing applications running in kubernetes externally. But provissioning load balancers for each application can become very expensive over time, and more difficult to manage. Especially when tens or even hundreds of applications are deployed.

The best approach is to use [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) instead. But to do that, we will have to deploy an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/).

A huge benefit of using the ingress controller is that we will be able to use a single load balancer for different applications we deploy. Therefore, Artifactory and any other tools can reuse the same load balancer. Which reduces cloud cost, and overhead of managing multiple load balancers. more on that later. 

For now, we will leave artifactory, move on to the next phase of configuration (Ingress, DNS(Route53) and Cert Manager), and then return to Artifactory to complete the setup so that it can serve as a private docker registry and repository for private helm charts.



Deploying Ingress Controller and managing Ingress Resources
============================

Before we discuss what ingress controllers are, it will be important to start off understanding about the **Ingress** resource.

An ingress is an API object that manages external access to the services in a kubernetes cluster. It is capable to provide load balancing, SSL termination and name-based virtual hosting. In otherwords, Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster. Traffic routing is controlled by rules defined on the Ingress resource.

Here is a simple example where an Ingress sends all its traffic to one Service:

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/ingress.svg" width="936px" height="550px">
*image credit:* kubernetes.io

An ingress resource for Artifactory would like like below

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: artifactory
spec:
  ingressClassName: nginx
  rules:
  - host: "tooling.artifactory.sandbox.svc.darey.io"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: artifactory
            port:
              number: 8082
```

- An Ingress needs `apiVersion`, `kind`, `metadata` and `spec` fields
- The name of an Ingress object must be a valid DNS subdomain name
- Ingress frequently uses annotations to configure some options depending on the Ingress controller.
- Different Ingress controllers support different annotations. Therefore it is important to be up to date with the ingress controller's specific documentation to know what annotations are supported.
- It is recommended to always specify the ingress class name with the spec `ingressClassName: nginx`. This is how the Ingress controller is selected, especially when there are multiple configured ingress controllers in the cluster.
- The domain `darey.io` should be replaced with your own domain. 

## Ingress controller

If you deploy the yaml configuration specified for the ingress resource without an ingress controller, it will not work. In order for the Ingress resource to work, the cluster must have an ingress controller running.

Unlike other types of controllers which run as part of the kube-controller-manager. Such as the **Node Controller**, **Replica Controller**, **Deployment Controller**, **Job Controller**, or **Cloud Controller**. Ingress controllers are not started automatically with the cluster. 

Kubernetes as a project supports and maintains [AWS](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/), [GCE](https://github.com/kubernetes/ingress-gce/blob/master/README.md#readme), and [NGINX](https://github.com/kubernetes/ingress-nginx/blob/main/README.md#readme) ingress controllers.

There are many other 3rd party Ingress controllers that provide similar functionalities with their own unique features, but the 3 mentioned earlier are currently supported and maintained by Kubernetes. Some of these other 3rd party Ingress controllers include but not limited to the following;

- [AKS Application Gateway Ingress Controller](https://docs.microsoft.com/en-gb/azure/application-gateway/tutorial-ingress-controller-add-on-existing) (**Microsoft Azure**)
- [Istio](https://istio.io/latest/docs/tasks/traffic-management/ingress/kubernetes-ingress/)
- [Traefik](https://doc.traefik.io/traefik/providers/kubernetes-ingress/)
- [Ambassador](https://www.getambassador.io/)
- [HA Proxy Ingress](https://haproxy-ingress.github.io/)
- [Kong](https://docs.konghq.com/kubernetes-ingress-controller/)
- [Gloo](https://docs.solo.io/gloo-edge/latest/)

An example comparison matrix of some of the controllers can be found [here](https://kubevious.io/blog/post/comparing-top-ingress-controllers-for-kubernetes#comparison-matrix). Understanding their unique features will help businesses determine which product works well for their respective requirements.

It is possible to deploy any number of ingress controllers in the same cluster. That is the essence of an **ingress class**. By specifying the spec `ingressClassName` field on the ingress object, the appropriate ingress controller will be used by the ingress resource.

Lets get into action and see how all of these fits together.

### Deploy Nginx Ingress Controller

On this project, we will deploy and use the **Nginx Ingress Controller**. It is always the default choice when starting with Kubernetes projects. It is reliable and easy to use.

Since this controller is maintained by Kubernetes, there is an official guide the installation process. Hence, we wont be using **artifacthub.io** here. Even though you can still find ready to go charts there, it just makes sense to always use the [official guide](https://kubernetes.github.io/ingress-nginx/deploy/) in this scenario.

Using the **Helm** approach, according to the official guide;

1. Install Nginx Ingress Controller in the `ingress-nginx` namespace
```
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

**Notice**:  

This command is idempotent:

- if the ingress controller is not installed, it will install it,
- if the ingress controller is already installed, it will upgrade it.

- **Self Challenge Task** - Delete the installation after running above command. Then try to re-install it using a slightly different method you are already familiar with. Ensure NOT to use the flag `--repo`
- **Hint** - Run the `helm repo add command` before installation

2. A few pods should start in the ingress-nginx namespace:

```
kubectl get pods --namespace=ingress-nginx
```

3. After a while, they should all be running. The following command will wait for the ingress controller pod to be up, running, and ready:

```
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

4. Check to see the created load balancer in AWS.
```
   kubectl get service -n ingress-nginx
```
Output:
```
NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP                                                              PORT(S)                      AGE
ingress-nginx-controller             LoadBalancer   172.16.11.35    a38db84e7d2104dc4b743ee6df1e667b-954094141.eu-west-2.elb.amazonaws.com   80:32516/TCP,443:31942/TCP   50s
ingress-nginx-controller-admission   ClusterIP      172.16.94.137   <none>                                                                   443/TCP                      50s
```

The `ingress-nginx-controller` service that was created is of the type `LoadBalancer`. That will be the load balancer to be used by all applications which require external access, and is using this ingress controller.

If you go ahead to AWS console, copy the address in the **EXTERNAL-IP** column, and search for the loadbalancer, you will see an output like below.

<img src="(https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/ingress-classic-load-balancer.png" width="936px" height="550px">

5. Check the IngressClass that identifies this ingress controller.

```
kubectl get ingressclass -n ingress-nginx
```
Output:
```
NAME    CONTROLLER             PARAMETERS   AGE
nginx   k8s.io/ingress-nginx   <none>       105s
```

### Deploy Artifactory Ingress

Now, it is time to configure the ingress so that we can route traffic to the Artifactory internal service, through the ingress controller's load balancer.

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/ingress.svg" width="936px" height="550px">
Notice the `spec` section with the configuration that selects the ingress controller using the **ingressClassName** 

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: artifactory
spec:
  ingressClassName: nginx
  rules:
  - host: "tooling.artifactory.sandbox.svc.darey.io"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: artifactory
            port:
              number: 8082
```

```
kubectl apply -f <filename.yaml> -n tools
```

Output:
```
NAME          CLASS   HOSTS                                   ADDRESS                                                                  PORTS   AGE
artifactory   nginx   tooling.artifactory.sandbox.svc.darey.io   a38db84e7d2104dc4b743ee6df1e667b-954094141.eu-west-2.elb.amazonaws.com   80      5s
```

Now, take note of

- CLASS - The nginx controller class name `nginx`
- HOSTS - The hostname to be used in the browser `tooling.artifactory.sandbox.svc.darey.io`
- ADDRESS - The loadbalancer address that was created by the ingress controller

## Configure DNS

If anyone were to visit the tool, it would be very inconvenient sharing the long load balancer address. Ideally, you would create a DNS record that is human readable and can direct request to the balancer. This is exactly what has been configured in the ingress object `- host: "tooling.artifactory.sandbox.svc.darey.io"` but without a DNS record, there is no way that host address can reach the load balancer.

The `sandbox.svc.darey.io` part of the domain is the configured **HOSTED ZONE** in AWS. So you will need to configure Hosted Zone in AWS console or as part of your infrastructure as code using terraform. 

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/hosted-zone.png" width="936px" height="550px">
If you purchased the domain directly from AWS, the hosted zone will be automatically configured for you. But if your domain is registered with a different provider such as **freenon** or **namechaep**, you will have to create the hosted zone and update the name servers.

### Create Route53 record

Within the hosted zone is where all the necessary DNS records will be created. Since we are working on Artifactory, lets create the record to point to the ingress controller's loadbalancer. There are 2 options. You can either use the *CNAME* or AWS *Alias*

#### **CNAME Method**

1. Select the **HOSTED ZONE** you wish to use, and click on the create record button
   
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/create-r53-record-1.png" width="936px" height="550px">
2. Add the subdomain `tooling.artifactory`, and select the record type `CNAME`
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/create-r53-record--cname.png" width="936px" height="550px">
3. Successfully created record
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/create-r53-record-cname-2.png" width="936px" height="550px">
4. Confirm that the DNS record has been properly propergated. Visit https://dnschecker.org and check the record. Ensure to select CNAME. The search should return green ticks for each of the locations on the left.
   ![](https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/dns-checker.png)

#### **AWS Alias Method**

1. In the create record section, type in the record name, and toggle the `alias` button to enable an alias. An alias is of the `A` DNS record type which basically routes directly to the load balancer. In the `choose endpoint` bar, select `Alias to Application and Classic Load Balancer`
 
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/create-r53-record-alias-1.png" width="936px" height="550px">

2. Select the region and the load balancer required. You will not need to type in the load balancer, as it will already populate.

  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/create-r53-record-alias-2.png" width="936px" height="550px">

For detailed read on selecting between CNAME and Alias based records, read the [official documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)

### Visiting the application from the browser

So far, we now have an application running in Kubernetes that is also accessible externally. That means if you navigate to https://tooling.artifactory.sandbox.svc.darey.io/ (*replace the full URL with your domain*), it should load up the artifactory application. 

Using Chrome browser will show something like the below. It shows that the site is indeed reachable, but insecure. This is because Chrome browsers do not load insecure sites by default. It is insecure because it either does not have a trusted TLS/SSL certificate, or it doesn't have any at all.

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/insecure-web.png" width="936px" height="550px">
Nginx Ingress Controller does configure a default TLS/SSL certificate. But it is not trusted because it is a self signed certificate that browsers are not aware of.

To confirm this,

1. Click on the **Not Secure** part of the browser.
   
<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/insecure-web-2.png" width="936px" height="550px">
2. Select the **Certificate is not valid** menu
    <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/insecure-web-3.png" width="936px" height="550px">
3. You will see the details of the certificate. There you can confirm that yes indeed there is encryption configured for the traffic, the browser is just not cool with it.
    
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/insecure-web-4.png" width="936px" height="550px">
Now try another browser. For example Internet explorer or Safari

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/insecure-web-5.png" title="Safari" width="936px" height="550px">
<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/insecure-web-6.png" title="Microsoft Edge" width="936px" height="550px">


### Explore Artifactory Web UI
Now that we can access the application externally, although insecure, its time to login for some exploration. Afterwards we will make it a lot more secure and access our web application on any browser.

1. Get the default username and password - Run a helm command to output the same message after the initial install
    
```
helm test artifactory -n tools
```
Output:
```
NAME: artifactory
LAST DEPLOYED: Sat May 28 09:26:08 2022
NAMESPACE: tools
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Congratulations. You have just deployed JFrog Artifactory!

1. Get the Artifactory URL by running these commands:

   NOTE: It may take a few minutes for the LoadBalancer IP to be available.
         You can watch the status of the service by running 'kubectl get svc --namespace tools -w artifactory-artifactory-nginx'
   export SERVICE_IP=$(kubectl get svc --namespace tools artifactory-artifactory-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
   echo http://$SERVICE_IP/

2. Open Artifactory in your browser
   Default credential for Artifactory:
   user: admin
   password: password
```

2. Insert the username and password to load the Get Started page
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-1.png" width="936px" height="550px">

3. Reset the admin password
    
    <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-2.png" width="936px" height="550px"> 

4. Activate the Artifactory License. You will need to purchase a license to use Artifactory enterprise features. 
    
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-3.png" width="936px" height="550px">

5. For learning purposes, you can apply for a free trial license. [Simply fill the form here](https://jfrog.com/start-free/) and a license key will be delivered to your email in few minutes.
   
 <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/Artifactory-License.pngg" width="936px" height="550px">

  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-4.png" width="936px" height="550px"> 

6. In exactly 1 minute, the license key had arrived. Simply copy the key and apply to the console.

  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-5.png" width="936px" height="550px">  

7. Set the Base URL. Ensure to use `https`
  
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-6.png" width="936px" height="550px"> 

8. Skip the Proxy setting 
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-7.png" width="936px" height="550px">
   
9. Skip creation of repositories for now. You will create them yourself later on.
      
  <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-8.png" width="936px" height="550px">

10. finish the setup
     
   <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-9.png" width="936px" height="550px"> 
  
<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-10.png" width="936px" height="550px">

Next, its time to fix the TLS/SSL configuration so that we will have a trusted **HTTPS** URL


Deploying Cert-Manager and managing TLS/SSL for Ingress
========================================================

Transport Layer Security (TLS), the successor of the now-deprecated Secure Sockets Layer (SSL), is a cryptographic protocol designed to provide communications security over a computer network.

The TLS protocol aims primarily to provide cryptography, including privacy (confidentiality), integrity, and authenticity through the use of certificates, between two or more communicating computer applications.

The certificates required to implement TLS must be issued by a trusted Certificate Authority (CA).

To see the list of trusted root Certification Authorities (CA) and their certificates used by Google Chrome, you need to use the Certificate Manager built inside Google Chrome as shown below:

1. Open the settings section of google chrome
   
2. Search for `security`
   
     <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/chrome-certificates-1.png" width="936px" height="550px">
3. Select `Manage Certificates` 
      <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/chrome-certificates-2.png" width="936px" height="550px">
4. View the installed certificates in your browser
   
<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/chrome-certificates-3.png" width="936px" height="550px">

## Certificate Management in Kubernetes

Ensuring that trusted certificates can be requested and issued from certificate authorities dynamically is a tedious process. Managing the certificates per application and keeping track of expiry is also a lot of overhead.

To do this, administrators will have to write complex scripts or programs to handle all the logic.

[Cert-Manager](https://cert-manager.io/) comes to the rescue! 

cert-manager adds certificates and certificate issuers as resource types in Kubernetes clusters, and simplifies the process of obtaining, renewing and using those certificates.

Similar to how Ingress Controllers are able to enable the creation of *Ingress* resource in the cluster, so also cert-manager enables the possibility to create certificate resource, and a few other resources that makes certificate management seamless.

It can issue certificates from a variety of supported sources, including [Let's Encrypt](https://letsencrypt.org/), [HashiCorp Vault](https://www.vaultproject.io/), and [Venafi](https://www.venafi.com/) as well as [private PKI](https://www.csoonline.com/article/3400836/what-is-pki-and-how-it-secures-just-about-everything-online.html). The issued certificates get stored as kubernetes secret which holds both the private key and public certificate.

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/cert-manager-high-level-overview.svg" width="936px" height="550px">
In this project, We will use Let's Encrypt with cert-manager. The certificates issued by Let's Encrypt will work with most browsers because the root certificate that validates all it's certificates is called **“ISRG Root X1”** which is already trusted by most browsers and servers.

You will find `ISRG Root X1` in the list of certificates already installed in your browser.

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/chrome-certificates-4.png" width="936px" height="550px">
[Read the official documentation here](https://letsencrypt.org/docs/certificate-compatibility/)

Cert-maanager will ensure certificates are valid and up to date, and attempt to renew certificates at a configured time before expiry.

## Cert-Manager high Level Architecture

Cert-manager works by having administrators create a resource in kubernetes called **certificate issuer** which will be configured to work with supported sources of certificates. This issuer can either be scoped **globally** in the cluster or only local to the namespace it is deployed to.

Whenever it is time to create a certificate for a specific host or website address, the process follows the pattern seen in the image below.

![](https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/cert-manager-1.png)
<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/cert-manager-1.png" width="936px" height="550px">
After we have deployed cert-manager, you will see all of this in action.

## Deploying Cert-manager 

- **Self Challenge Task** Find cert-manager helm chart in Artifact Hub, follow the installation guide and deploy into Kubernetes

You should see an output like this 

```
NAME: cert-manager
LAST DEPLOYED: Fri Mar 11 14:15:51 2022
NAMESPACE: cert-manager
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
cert-manager v1.7.1 has been deployed successfully!

In order to begin issuing certificates, you will need to set up a ClusterIssuer
or Issuer resource (for example, by creating a 'letsencrypt-staging' issuer).

More information on the different types of issuers and how to configure them
can be found in our documentation:

https://cert-manager.io/docs/configuration/

For information on how to configure cert-manager to automatically provision
Certificates for Ingress resources, take a look at the `ingress-shim`
documentation:

https://cert-manager.io/docs/usage/ingress/
```

### Certificate Issuer
Next, is to create an Issuer. We will use a **Cluster Issuer** so that it can be scoped globally. Assuming that we will be using **darey.io** domain. Simply update this yaml file and deploy with **kubectl**. In the section that follows, we will break down each part of the file.


```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  namespace: "cert-manager"
  name: "letsencrypt-prod"
spec:
  acme:
    server: "https://acme-v02.api.letsencrypt.org/directory"
    email: "infradev@oldcowboyshop.com"
    privateKeySecretRef:
      name: "letsencrypt-prod"
    solvers:
    - selector:
        dnsZones:
          - "darey.io"
      dns01:
        route53:
          region: "eu-west-2"
          hostedZoneID: "Z2CD4NTR2FDPZ"
```

Lets break down the content to undertsand all the sections

- Section 1 - The standard kubernetes section that defines the **apiVersion**, **Kind**, and **metadata**. The Kind here is a ClusterIssuer which means it is scoped globally.
    ```
    apiVersion: cert-manager.io/v1
    kind: ClusterIssuer
    metadata:
    namespace: "cert-manager"
    name: "letsencrypt-prod"
    ```

- Section 2 - In the spec section, an [**ACME**](https://cert-manager.io/docs/configuration/acme/) - Automated Certificate Management Environment issuer type is specified here. When you create a new ACME Issuer, cert-manager will generate a private key which is used to identify you with the ACME server. 
  
  Certificates issued by public ACME servers are typically trusted by client's computers by default. This means that, for example, visiting a website that is backed by an ACME certificate issued for that URL, will be trusted by default by most client's web browsers. ACME certificates are typically free. 
  
  Let’s Encrypt uses the ACME protocol to verify that you control a given domain name and to issue you a certificate. You can either use the let's encrypt **Production** server address `https://acme-v02.api.letsencrypt.org/directory` which can be used for all production websites. Or it can be replaced with the staging URL `https://acme-staging-v02.api.letsencrypt.org/directory` for all **Non-Production** sites.

    The `privateKeySecretRef` has configuration for the private key name you prefer to use to store the ACME account private key. This can be anything you specify, for example **letsencrypt-prod** 

    ```
    spec:
     acme:
        # The ACME server URL
        server: "https://acme-v02.api.letsencrypt.org/directory"
        email: "infradev@darey.io"
        # Name of a secret used to store the ACME account private key
        privateKeySecretRef:
        name: "letsencrypt-prod"
    ```

    - section 3 - This section is part of the `spec` that configures `solvers` which determines the domain address that the issued certificate will be registered with. `dns01` is one of the different challenges that cert-manager uses to verify domain ownership. [Read more on DNS01 Challenge here](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge). With the **DNS01** configuration, you will need to specify the Route53 DNS Hosted Zone ID and region. Since we are using EKS in AWS, the IAM permission of the worker nodes will be used to access Route53. Therefore if appropriate permissions is not set for EKS worker nodes, it is possible that certificate challenge with Route53 will fail, hence certificates will not get issued.
  
        The other possible option is the [HTTP01](https://cert-manager.io/docs/configuration/acme/http01/#configuring-the-http01-ingress-solver) challenge, but we won't be using that here.
  ```
      solvers:
        - selector:
            dnsZones:
            - "darey.io"
        dns01:
            route53:
            region: "eu-west-2"
            hostedZoneID: "Z2CD4NTR2FDPZ"
    ```

With the ClusterIssuer properlu configured, it is now time to start getting certificates issued. 

Lets see what that looks like in the next section.



Configuring Ingress for TLS
========================================================

To ensure that every created ingress also has TLS configured, we will need to update the ingress manifest with TLS specific configurations.

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    kubernetes.io/ingress.class: nginx
  name: artifactory
spec:
  rules:
  - host: "tooling.artifactory.sandbox.svc.darey.io"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: artifactory
            port:
              number: 8082
  tls:
  - hosts:
    - "tooling.artifactory.sandbox.svc.darey.io"
    secretName: "tooling.artifactory.sandbox.svc.darey.io"
```

The most significat updates to the ingress definition is the `annotations` and `tls` sections.

Lets quickly talk about Annotations. **Annotations** are used similar to `labels` in kubernetes. They are ways to attach metadata to objects.

## Differences between Annotations and Labels

**Labels** are used in conjunction with selectors to identify groups of related resources. Because selectors are used to query labels, this operation needs to be efficient. To ensure efficient queries, labels are constrained by RFC 1123. RFC 1123, among other constraints, restricts labels to a maximum 63 character length. Thus, labels should be used when you want Kubernetes to group a set of related resources.

**Annotations** are used for “non-identifying information” i.e., metadata that Kubernetes does not care about. As such, annotation keys and values have no constraints. Thus, if you want to add information for other humans about a given resource, then annotations are a better choice.

The Annotation added to the Ingress resource adds metadata to specify the issuer responsible for requesting certificates. The issuer here will be the same one we have created earlier with the name`letsencrypt-prod`. 
```
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
```

The other section is `tls` where the host name that will require `https` is specified. The `secretName` also holds the name of the secret that will be created which will store details of the certificate key-pair. i.e Private key and public certificate. 


```
  tls:
  - hosts:
    - "tooling.artifactory.sandbox.svc.darey.io"
    secretName: "tooling.artifactory.sandbox.svc.darey.io"
```

Redeploying the newly updated ingress will go through the process as shown below.

 <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/cert-manager-1.png" width="936px" height="550px">
Once deployed, you can run the following commands to see each resource at each phase.

- kubectl get certificaaterequest
- kubectl get order
- kubectl get challenge 
-  kubectl get certificate

At each stage you can run **describe** on each resource to get more information on what cert-manager is doing.

If all goes well, running `kubectl get certificate`,you should see an output like below.

```
NAME                                           READY                            SECRET                          AGE
tooling.artifactory.sandbox.svc.darey.io       True             tooling.artifactory.sandbox.svc.darey.io       108s
```

Notice the secret name there in the above output.  Executing the command `kubectl get secrettooling.artifactory.sandbox.svc.darey.io -o yaml`, you will see the `data` with encoded version of both the private key `tls.key` and the public certificate `tls.crt`. This is the actual certificate configuration that the ingress controller will use as part of Nginx configuration to terminate TLS/SSL on the ingress.

If you now head over to the browser, you should see the padlock sign without warnings of untrusted certificates.

 <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-tls-padlocked.png" width="936px" height="550px">
Finally, one more task for you to do is to ensure that the LoadBalancer created for artifactory is destroyed. If you run a get service kubectl command like below;

```
kubectl get service -n tools
```
 <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-nginx-service-output.png" width="936px" height="550px">
You will see that the load balancer is still there. 

A task for you is to update the helm values file for artifactory, and ensure that the `artifactory-artifactory-nginx` service uses `ClusterIP`

Your final output should look like this.

 <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-nginx-service-output2.png" width="936px" height="550px">
Finally, update the ingress to use `artifactory-artifactory-nginx` as the backend service instead of using `artifactory`. Remember to update the port number as well.

If everything goes well, you will be prompted at login to set the BASE URL. It will pick up the new `https` address. Simply click next 

 <img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-11.png" width="936px" height="550px">
Skip the `proxy` part of the setup.

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-12.png" width="936px" height="550px">
Skip repositories creation because you will do this in the next poject.

<img src="https://darey-io-nonprod-pbl-projects.s3.eu-west-2.amazonaws.com/project25/artifactory-get-started-13.png" width="936px" height="550px">
Then complete the setup.

Congratulations! for completing Project 25

With the knowledge you now have, see if you can deploy Grafana, Prometheus and Elasticsearch yourself. Do some research into these tools, and assume you are being tasked at work to work on tools you have never worked on before

In the next project, you will experience;


1. Configuring private container registry using Artifactory
2. Configuring private helm repository using Artifactory
