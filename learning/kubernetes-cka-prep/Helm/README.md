<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DevCloudNinjas/Certified_Kubernetes_Administrator/tree/master/Helm">
    <img src="images/logo.svg" alt="Logo" width="150" height="150">
  </a>

<h3 align="center">Helm</h3>

  <p align="center">
    The Kubernetes Package Manager
  </p>
</div>
<br>
<div id="top">
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
  <li>
     Helm Chart
    <ul>
        <li><a href="#intro-What-is-helm">What is Helm?</a>
            <ul>
                <li><a href="#intro-Sharing-Helm-Charts">Sharing Helm Charts</a></li>
                <li><a href="#intro-Templating-Engine">Templating Engine</a></li>
                <li><a href="#intro-Different-Environments">Different Environments</a></li>
            </ul>
        </li>
        <li><a href="#intro-Helm-Chart-Structure">Helm Chart Structure</a></li>
        <li><a href="#intro-Value-injection">Value injection</a></li>
        <li><a href="#intro-Release-Management">Release Management</a></li>
        <li><a href="#intro-Differences-between-charts-and-packages">Differences between charts and packages</a></li>
        <li><a href="#intro-Charts-and-repositories">Charts and repositories</a>
          <ul>
            <li><a href="#intro-Managing-repositories">Managing repositories</a></li>
            <li><a href="#intro-Search-available-charts">Search available charts</a></li>
          </ul>
        </li>
        <li><a href="#intro-Checking-possible-values">Checking possible values</a></li>
    </ul>
  </li>
  <li>
     Demo: Install a Stateful App on K8s using Helm
    <ul>
        <li><a href="#Demo-Stateful-overview">Overview</a></li>
        <li><a href="#Demo-Stateful-Add-bitnami-repo">Add bitnami repo</a></li>
        <li><a href="#Demo-Stateful-Install-MongoDB">Install MongoDB</a></li>
        <li><a href="#Demo-Stateful-Install-MongoExpress">Install MongoExpress</a></li>
        <li><a href="#Demo-Stateful-Deploy-Ingress-controller-and-Create-Ingress-rule">Deploy Ingress controller and Create Ingress rule</a></li>
    </ul>
  </li>
  <li>
     Demo: Create Helm Chart for an Online Boutique
    <ul>
        <li><a href="#Demo-Online-Boutique-overview">Overview</a></li>
        <li><a href="#Online-Boutique-Basic-structure-of-Helm-Chart">Basic structure of Helm Chart</a></li>
        <li><a href="#Online-Boutique-Create-Basic-Template-File">Create Basic Template File</a></li>
        <li><a href="#Online-Boutique-Dynamic-Environment-Variables">Dynamic Environment Variables</a></li>
        <li><a href="#Online-Boutique-Dynamic-Set-Variables">Set Variables</a></li>
        <li><a href="#Online-Boutique-Test-the-Chart">Test the Chart</a></li>
        <li><a href="#Online-Boutique-Install-the-Chart">Install the Chart</a></li>
    </ul>
  </li>
  <li>
     Helmfile
    <ul>
        <li><a href="#Helmfile-What-is-a-Helmfile">What is a Helmfile?</a></li>
        <li><a href="#Helmfile-Uninstall-previous-Helm-Charts">Uninstall previous Helm Charts</a></li>
        <li><a href="#Helmfile-Create-helmfile">Create helmfile</a></li>
        <li><a href="#Helmfile-Install-helmfile">Install helmfile</a></li>
        <li><a href="#Helmfile-Deploy-Helm-Charts">Deploy Helm Charts</a></li>
        <li><a href="#Helmfile-Uninstall-Releases">Uninstall Releases</a></li>
        <li><a href="#Helmfile-Wrap-UP">Wrap UP</a></li>
    </ul>
  </li>
</ol>
</details>
</div>

---

# Helm Chart

## What is Helm?

<div id="intro-What-is-helm">

According to the [official documentation](https://helm.sh), **Helm is a package manager for Kubernetes** to
package YAML files and distribute them in public and private repositories.

Helm charts:

* Bundle of YAML files
* Create your own Helm Charts with Helm
* Push them to Helm repository (Or any other repository out there)
* Download and use existing ones

Helm has some interesting features that makes it awesome, such as:

* Sharing Helm Charts
* Templating Engine
* Same application across different environments

### Sharing Helm Charts

<div id="intro-Sharing-Helm-Charts">

There is already alot of charts oot there (e.g. Database Apps, Monitoring Apps)

To search between those:

* `helm search <KEYWORD>`
    * Search provides the ability to search for Helm charts in the various places
      they can be stored including the **[Artifact Hub](https://artifacthub.io)** and **repositories you have added**.
* [Artifact Hub](https://artifacthub.io)
    * The [Artifact Hub](https://artifacthub.io) is a `CNCF` project to make discovering distributed cloud native
      artifacts easy. This includes Helm charts.

* There is two types of registries:
    1) Public Registries (e.g. [Artifact Hub](https://artifacthub.io))
    2) Private Registries (Share in organization)

</div> <!-- Sharing Helm Charts -->

### Templating Engine

<div id="intro-Templating-Engine">

Let's say we have a bunch of microservices, so here in our scenario:

* Deployment and Service configuration almost the same!
* Most values are the same!
* Wouldn't be nice if we could define one file for deployment and another for service and just replace the values?!
* [x] Helm does that!

---

1) Define a common blueprint
2) Dynamic values are replaced by placeholders (this syntax: `{{ .Values.XXX }}`)

* values.yaml
    ```yaml
    name: nginx-app
    container:
      name: nginx-app-container
      image: nginx
      port: 80
    ```
* Template YAML config
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata: 
      name: {{ .Values.name }}
    spec:
      containers:
        - name: {{ .Values.container.name }}
          image: {{ .Values.container.image }}
          port: {{ .Values.container.port }}
    ```

* Values defined either by `yaml file` or with `--set` flag
* Now instead of **many YAML files** we have **just 1 YAML file**
* This is extremely powerful! e.g. for **CI/CD**
    * In your build you can replace the values on the fly

</div> <!-- Templating Engine -->

### Different Environments

<div id="intro-Different-Environments">

This Helm features (<a href="#intro-Sharing-Helm-Charts">Sharing Helm Charts</a> & <a href="#intro-Templating-Engine">
Templating Engine</a>) are super helpful for CI/CD pipelines or DevOps Best-Practices

Let's say you have 3 environments:

* Development
* Staging
* Production

Now you can manage all those three environments by one single Chart!

</div> <!-- Different Environments -->
</div> <!-- What is Helm -->

## Helm Chart Structure

<div id="intro-Helm-Chart-Structure">

* Directory structure:
    ```text
    mychart
    |-- Chart.yaml
    |-- charts
    |-- templates
    |   |-- NOTES.txt # Optionally files
    |   |-- _helpers.tpl # Optionally files
    |   |-- deployment.yaml
    |   |-- ingress.yaml
    |   `-- service.yaml
    `-- values.yaml
    ```
* Top level `mychart` folder: Name of the chart
* `Chart.yaml`: Meta information about the chart
* `charts`: folder: Chart dependencies
* `templates` folder: The actual templater files
* `values.yaml`: The actual template files

#### README and NOTES.txt

* At the top-level of the chart, it's a good idea to have a `README`
* It will be viewable with e.g. `helm show readme bitnami/mongodb`
* In the `templates/` directory, we can also have a `NOTES.txt` file
* When the template is installed (or upgraded), `NOTES.txt` is processed too (i.e. its `{{ ... }}` tags are evaluated)
* It gets displayed after the **installation** or **upgrades**
* It's a great place to generate messages to tell the user:
  * how to connect to the release they just deployed
  * any passwords or other thing that we generated for them

---

* `helm install <CHARTNAME>`
    * Template files will be filled with the values from `values.yaml`

</div> <!-- Helm Chart Structure -->

## Value injection

<div id="intro-Value-injection">

Let's say we have a

* `values.yaml`
    ```yaml
    imageName: nginx
    port: 80
    version: 1.0.0
    ```
* `my-values.yaml`
    ```yaml
    version: 2.0.0
    ```
* Install the chart
    ```shell
    helm install --values=my-values.yaml <CHARTNAME>
    ```
* Result would be:
    ```yaml
    imageName: nginx # From `values.yaml`
    port: 80 # From `values.yaml`
    version: 2.0.0 # From `my-values.yaml` -- Override value
    ```
* You can achieve the exact same goal without having `my-values.yaml` file:
    ```shell
    helm install --set version=2.0.0 <CHARTNAME>
    ```

</div> <!-- Value injection -->

## Release Management

<div id="intro-Release-Management">

### Helm version 2 vs. 3

* Helm 3 was released [November 13, 2019](https://helm.sh/blog/helm-3-released)
* Charts remaster compatible between Helm 2 and Helm 3
* The CLI is very similar (with minor changes to some commands)
* The master difference is that Helm 2 uses `tiller`, a server-side component
* Helm 3 doesn't use `tiller` at all, making it simpler (yay!)

* Helm version 2 comes in two parts:
    * CLIENT (Helm CLI)
    * SERVER (Tiller -- should be deployed on Kubernetes cluster already)
* CLIENT (Helm CLI) send requests to SERVER (Tiller)
* Then Tiler stores a copy of configuration
    * Keeping track of all chart execution
      ```text
      | Revision | Request            |
      |----------|--------------------|
      | 1        | Installed Chart    | -- `helm install <CHART-NAME>`
      | 2        | Upgrade to v 1.0.0 | -- `helm upgrade <CHART-NAME>`
      | 3        | Rolled back to 1   | -- `helm rollback <CHART-NAME>`
      ```

    * Changes are applied to existing Deployment instead of creating a new one
    * Handling rollbacks

---

### Downside of Tillers

* Tiller has too much power inside K8s cluster
    * Create
    * Update
    * Delete
* Security Issues

---

### Helm version 3

* Helm solves the security concerns by deleting Tiller in Helm 3
* Removal of Tiller:
    * Replaces `client/server` with `client/library` architecture (Helm binary only)
    * Security is now on per-user basis (delegated to Kubernetes user cluster security)
    * Releases are now stored as in-cluster secrets and the release object metadata has changed
    * Releases are persisted on a release namespace basis and not in the Tiller namespace anymore
* [And so many more!](https://helm.sh/docs/topics/v2_v3_migration)

---

### With or without tiller

With Helm 3:

* The helm CLI communicates directly with the Kubernetes API
* It creates resources (deployments, services...) with our credentials

With Helm 2:

* The helm CLI communicates with tiller, telling tiller what to do
* Tiller then communicates with the Kubernetes API, using its own credentials

</div> <!-- Release Management -->

## Differences between charts and packages

<div id="intro-Differences-between-charts-and-packages">

* A package (`deb`, `rpm`, etc.) contains binaries, libraries, etc.
* A chart contains YAML manifests
  (the binaries, libraries, etc. are in the images referenced by the chart)
* On most distributions, a package can only be installed **once**
  (installing another version replaces the installed one)
* A chart can be installed **multiple times**
* Each installation is called a **release**
* This allows to install e.g. 10 instances of MongoDB
  (with potentially different versions and configurations)

---

Wait a minute ...

But, on my Debian system, I have Python `2` and Python `3`.

Also, I have multiple versions of the Postgres database engine!

Yes!

But they have different package names:

* `python2.7`, `python3.8`
* `postgresql-10`, `postgresql-11`

</div> <!-- Differences between charts and packages -->

## Charts and repositories

<div id="intro-Charts-and-repositories">

* A repository (or `repo` in short) is a **collection of charts**
* It's just a bunch of files
  (they can be hosted by a static HTTP server, or on a local directory)
* We can add "repos" to Helm, giving them a nickname
* The nickname is used when referring to charts on that repo
  (for instance, if we try to install hello/world, that means the chart world on the repo hello; and that repo hello
  might be something like `https://blahblah.hello.io/charts`)

### Managing repositories

<div id="intro-Managing-repositories">

* Let's check what repositories we have, and add the `bitnami` repo (the `bitnami` repo (By VMWare) contains a set of
  useful charts)

* List our repos:
  ```shell
  helm repo list
  ```

* Add the `bitnami` repo:
  ```shell
  helm repo add bitnami https://charts.bitnami.com/bitnami
  ```

* Adding a repo can take a few seconds (it downloads the list of charts from the repo).

</div> <!-- Managing repositories -->

### Search available charts

<div id="intro-Search-available-charts">

* We can search available charts with `helm search` command
* We need to specify where to search (`hub` or `repo`)
    * `hub`: Search for charts in the Artifact Hub or your own hub instance
    * `repo`: Search repositories for a keyword in charts
* Search all charts in the repo that we added earlier:
  ```shell
  helm search repo bitnami
  ```
* Search for a specific chart (`mongodb` chart in our case)
  ```shell
  helm search repo bitnami/mongodb
  ```

</div> <!-- Search available charts -->
</div> <!-- Charts and repositories -->

## Checking possible values

<div id="intro-Checking-possible-values">

* We can inspect a chart with `helm show`
* Look at the README for `mongodb`
  ```shell
  helm show readme bitnami/mongodb
  ```
* Look at the values and their defaults:
  ```shell
  helm show readme bitnami/mongodb
  ```

</div> <!-- Checking possible values -->

<p align="right">(<a href="#top">back to top</a>)</p>

# Demo: Install a Stateful App on K8s using Helm

## Overview

<div id="Demo-Stateful-overview">

In this Demo project, we will deploy a MongoDB application with its visualizer called MongoExpress

Then we install an Ingress Controller and Create an Ingress Rule to reaching our MongoExpress through the browser...

2 ways to deploy StatefulSet:

1) Create all the configuration files yourself
    * StatefulSet Config File
    * Other configuration files
2) Use bundle of those config files
    * Helm

</div> <!-- Overview -->

## Add bitnami repo

<div id="Demo-Stateful-Add-bitnami-repo">

First we need to add [bitnami](https://github.com/bitnami/charts) repository to our cluster via Helm...

Bitnami: Popular applications, provided by [Bitnami](https://bitnami.com), ready to launch on Kubernetes
using [Kubernetes Helm](https://github.com/helm/helm).

* Add the bitnami repo
  ```shell
  helm repo add bitnami https://charts.bitnami.com/bitnami
  ```
* Update the helm repos
  ```shell
  helm repo update
  ```
* See all the charts in this repo
  ```shell
  helm search repo bitnami
  ```
* See the mongoDB charts
  ```shell
  helm search repo bitnami/mongo
  ```

</div> <!-- Add bitnami repo -->

## Install MongoDB

<div id="Demo-Stateful-Install-MongoDB">

* See the [MongoDB chart page](https://github.com/bitnami/charts/tree/master/bitnami/mongodb)

* Based on [the docs](https://github.com/bitnami/charts/tree/master/bitnami/mongodb), create a `mobgo-values.yaml`:
  ```yaml
  architecture: replicaset # MongoDB's architecture (standalone or replicaset)
  replicaCount: 3 # Number of MongoDB nodes (only when architecture=replicaset)
  persistence:
    storageClass: "aws-ebs" # PVC Storage Class for MongoDB data volume
  auth: 
    rootPassword: secret-key-pwd # MongoDB root password
  ```
* Install the chart
  ```shell
  helm install <OUR-NAME> --values <CUSTOM-VALUES-FILE-NAME> <CHART-NAME]
  ```
  ```shell
  helm install mongodb --values mobgo-values.yaml bitnami/mongodb
  ```

And now everything is good to go!

</div> <!-- Install MongoDB -->

## Install MongoExpress

<div id="Demo-Stateful-Install-MongoExpress">

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo-express
  labels:
    app: mongo-express
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongo-express
  template:
    metadata:
      labels:
        app: mongo-express
    spec:
      containers:
        - name: mongo-express
          image: mongo-express
          ports:
            - containerPort: 8081
          env:
            - name: ME_CONFIG_MONGODB_ADMINUSERNAME
              value: root
            - name: ME_CONFIG_MONGODB_SERVER
              value: mongodb-0.mongodb-headless
            - name: ME_CONFIG_MONGODB_ADMINPASSWORD
              valueFrom:
                secretKeyRef:
                  name: mongodb
                  key: mongodb-root-password # It comes from here: `kubectl get secret mongodb -o yaml | grep mongodb-root-password`
---
# Internal Service - Only accessible within the cluster
apiVersion: v1
kind: Service
metadata:
  name: mongo-express-service
spec:
  selector:
    app: mongo-express
  ports:
    - protocol: TCP
      port: 8081
      targetPort: 8081
```

Apply it...

</div> <!-- Install MongoExpress -->

## Deploy Ingress controller and Create Ingress rule

<div id="Demo-Stateful-Deploy-Ingress-controller-and-Create-Ingress-rule">

1) Deploy Ingress Controller
    * nginx-ingress controller
2) Create Ingress Rule

---

### Deploy Ingress Controller

As [documentation](https://github.com/kubernetes/ingress-nginx/tree/master/charts/ingress-nginx) mentioned:

* Add the repo
  ```shell
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  ```
* Update the repos
  ```shell
  helm repo update
  ```
* Installing the Chart
  ```shell
  helm install nginx-ingress ingress-nginx/ingress-nginx --set controller.publishService.enabled=true 
  ```

---

### Create Ingress Rule

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
  name: mongo-express
spec:
  rules:
    - host: CLOUD-LOADBALANCER-ADDRESS
      http:
        paths:
          - path: /
            backend:
              serviceName: mongo-express-service
              servicePort: 8081
```

Apply it and everything should be fine...

---

### What happening right now?!

1) Browser: hostname configured in ingress rule
2) Hostname gets resolved to external IP of LoadBalancer
3) Ingress Controller resolved rule and forwards to internal Service of MongoExpress

</div> <!-- Deploy Ingress controller and Create Ingress rule -->
<p align="right">(<a href="#top">back to top</a>)</p>

# Demo: Create Helm Chart for an Online Boutique

## Overview

<div id="Demo-Online-Boutique-overview">

This chapter teaches a lot about Creating, managing, and more about Helm.

For this demo, we use an example from google
cloud: [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo).

Online Boutique is a Sample cloud-native application with ten microservices, each with
its [YAML file](https://github.com/GoogleCloudPlatform/microservices-demo/tree/master/kubernetes-manifests), but we will
create one shared helm chart for this application.

<img src="images/helm-demo-1.png">

This the complete YAML file

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: emailservice
spec:
  selector:
    matchLabels:
      app: emailservice
  template:
    metadata:
      labels:
        app: emailservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/emailservice:v0.2.3
          ports:
            - containerPort: 8080
          env:
            - name: PORT
              value: "8080"
            - name: DISABLE_TRACING
              value: "1"
            - name: DISABLE_PROFILER
              value: "1"
          readinessProbe:
            periodSeconds: 5
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:8080" ]
          livenessProbe:
            periodSeconds: 5
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:8080" ]
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: emailservice
spec:
  type: ClusterIP
  selector:
    app: emailservice
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 8080

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recommendationservice
spec:
  selector:
    matchLabels:
      app: recommendationservice
  template:
    metadata:
      labels:
        app: recommendationservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/recommendationservice:v0.2.3
          ports:
            - containerPort: 8080
          readinessProbe:
            periodSeconds: 5
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:8080" ]
          livenessProbe:
            periodSeconds: 5
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:8080" ]
          env:
            - name: PORT
              value: "8080"
            - name: PRODUCT_CATALOG_SERVICE_ADDR
              value: "productcatalogservice:3550"
            - name: DISABLE_TRACING
              value: "1"
            - name: DISABLE_PROFILER
              value: "1"
            - name: DISABLE_DEBUGGER
              value: "1"
          resources:
            requests:
              cpu: 100m
              memory: 220Mi
            limits:
              cpu: 200m
              memory: 450Mi
---
apiVersion: v1
kind: Service
metadata:
  name: recommendationservice
spec:
  type: ClusterIP
  selector:
    app: recommendationservice
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: paymentservice
spec:
  selector:
    matchLabels:
      app: paymentservice
  template:
    metadata:
      labels:
        app: paymentservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/paymentservice:v0.2.3
          ports:
            - containerPort: 50051
          env:
            - name: PORT
              value: "50051"
          readinessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:50051" ]
          livenessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:50051" ]
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: paymentservice
spec:
  type: ClusterIP
  selector:
    app: paymentservice
  ports:
    - protocol: TCP
      port: 50051
      targetPort: 50051

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: productcatalogservice
spec:
  selector:
    matchLabels:
      app: productcatalogservice
  template:
    metadata:
      labels:
        app: productcatalogservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/productcatalogservice:v0.2.3
          ports:
            - containerPort: 3550
          env:
            - name: PORT
              value: "3550"
          readinessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:3550" ]
          livenessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:3550" ]
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: productcatalogservice
spec:
  type: ClusterIP
  selector:
    app: productcatalogservice
  ports:
    - protocol: TCP
      port: 3550
      targetPort: 3550

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: currencyservice
spec:
  selector:
    matchLabels:
      app: currencyservice
  template:
    metadata:
      labels:
        app: currencyservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/currencyservice:v0.2.3
          ports:
            - containerPort: 7000
          env:
            - name: PORT
              value: "7000"
          readinessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:7000" ]
          livenessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:7000" ]
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: currencyservice
spec:
  type: ClusterIP
  selector:
    app: currencyservice
  ports:
    - protocol: TCP
      port: 7000
      targetPort: 7000

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shippingservice
spec:
  selector:
    matchLabels:
      app: shippingservice
  template:
    metadata:
      labels:
        app: shippingservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/shippingservice:v0.2.3
          ports:
            - containerPort: 50051
          env:
            - name: PORT
              value: "50051"
          readinessProbe:
            periodSeconds: 5
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:50051" ]
          livenessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:50051" ]
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: shippingservice
spec:
  type: ClusterIP
  selector:
    app: shippingservice
  ports:
    - protocol: TCP
      port: 50051
      targetPort: 50051

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adservice
spec:
  selector:
    matchLabels:
      app: adservice
  template:
    metadata:
      labels:
        app: adservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/adservice:v0.2.3
          ports:
            - containerPort: 9555
          env:
            - name: PORT
              value: "9555"
          resources:
            requests:
              cpu: 200m
              memory: 180Mi
            limits:
              cpu: 300m
              memory: 300Mi
          readinessProbe:
            initialDelaySeconds: 20
            periodSeconds: 15
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:9555" ]
          livenessProbe:
            initialDelaySeconds: 20
            periodSeconds: 15
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:9555" ]
---
apiVersion: v1
kind: Service
metadata:
  name: adservice
spec:
  type: ClusterIP
  selector:
    app: adservice
  ports:
    - protocol: TCP
      port: 9555
      targetPort: 9555

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cartservice
spec:
  selector:
    matchLabels:
      app: cartservice
  template:
    metadata:
      labels:
        app: cartservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/cartservice:v0.2.3
          ports:
            - containerPort: 7070
          env:
            - name: REDIS_ADDR
              value: "redis-cart:6379"
          resources:
            requests:
              cpu: 200m
              memory: 64Mi
            limits:
              cpu: 300m
              memory: 128Mi
          readinessProbe:
            initialDelaySeconds: 15
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:7070", "-rpc-timeout=5s" ]
          livenessProbe:
            initialDelaySeconds: 15
            periodSeconds: 10
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:7070", "-rpc-timeout=5s" ]
---
apiVersion: v1
kind: Service
metadata:
  name: cartservice
spec:
  type: ClusterIP
  selector:
    app: cartservice
  ports:
    - protocol: TCP
      port: 7070
      targetPort: 7070

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkoutservice
spec:
  selector:
    matchLabels:
      app: checkoutservice
  template:
    metadata:
      labels:
        app: checkoutservice
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/checkoutservice:v0.2.3
          ports:
            - containerPort: 5050
          readinessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:5050" ]
          livenessProbe:
            exec:
              command: [ "/bin/grpc_health_probe", "-addr=:5050" ]
          env:
            - name: PORT
              value: "5050"
            - name: PRODUCT_CATALOG_SERVICE_ADDR
              value: "productcatalogservice:3550"
            - name: SHIPPING_SERVICE_ADDR
              value: "shippingservice:50051"
            - name: PAYMENT_SERVICE_ADDR
              value: "paymentservice:50051"
            - name: EMAIL_SERVICE_ADDR
              value: "emailservice:5000"
            - name: CURRENCY_SERVICE_ADDR
              value: "currencyservice:7000"
            - name: CART_SERVICE_ADDR
              value: "cartservice:7070"
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: checkoutservice
spec:
  type: ClusterIP
  selector:
    app: checkoutservice
  ports:
    - protocol: TCP
      port: 5050
      targetPort: 5050

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: server
          image: gcr.io/google-samples/microservices-demo/frontend:v0.2.3
          ports:
            - containerPort: 8080
          readinessProbe:
            initialDelaySeconds: 10
            httpGet:
              path: "/_healthz"
              port: 8080
              httpHeaders:
                - name: "Cookie"
                  value: "shop_session-id=x-readiness-probe"
          livenessProbe:
            initialDelaySeconds: 10
            httpGet:
              path: "/_healthz"
              port: 8080
              httpHeaders:
                - name: "Cookie"
                  value: "shop_session-id=x-liveness-probe"
          env:
            - name: PORT
              value: "8080"
            - name: PRODUCT_CATALOG_SERVICE_ADDR
              value: "productcatalogservice:3550"
            - name: CURRENCY_SERVICE_ADDR
              value: "currencyservice:7000"
            - name: CART_SERVICE_ADDR
              value: "cartservice:7070"
            - name: RECOMMENDATION_SERVICE_ADDR
              value: "recommendationservice:8080"
            - name: SHIPPING_SERVICE_ADDR
              value: "shippingservice:50051"
            - name: CHECKOUT_SERVICE_ADDR
              value: "checkoutservice:5050"
            - name: AD_SERVICE_ADDR
              value: "adservice:9555"
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: ClusterIP
  selector:
    app: frontend
  ports:
    - name: http
      port: 80
      targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-external
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
    - name: http
      port: 80
      targetPort: 8080

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cart
spec:
  selector:
    matchLabels:
      app: redis-cart
  template:
    metadata:
      labels:
        app: redis-cart
    spec:
      containers:
        - name: redis
          image: redis:alpine
          ports:
            - containerPort: 6379
          readinessProbe:
            periodSeconds: 5
            tcpSocket:
              port: 6379
          livenessProbe:
            periodSeconds: 5
            tcpSocket:
              port: 6379
          volumeMounts:
            - mountPath: /data
              name: redis-data
          resources:
            requests:
              cpu: 70m
              memory: 200Mi
            limits:
              cpu: 125m
              memory: 256Mi
      volumes:
        - name: redis-data
          emptyDir: { }
---
apiVersion: v1
kind: Service
metadata:
  name: redis-cart
spec:
  type: ClusterIP
  selector:
    app: redis-cart
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
```

</div> <!-- Overview -->

## Basic structure of Helm Chart

<div id="Online-Boutique-Basic-structure-of-Helm-Chart">

* We are going to show a way to create a very simplified chart
* Create a sample chart with the name of `boutique`:
  ```shell
  helm create boutique
  ```
* This will create a folder (`boutique`):
  ```shell
  boutique
  ├── charts # Chart dependencies
  ├── Chart.yaml # Metadata info about chart
  ├── .helmignore # Files that you don't want to include in your helm chart
  ├── templates # Where the actual K8s YAML files (template files) are created 
  │   ├── deployment.yaml
  │   ├── _helpers.tpl
  │   ├── hpa.yaml
  │   ├── ingress.yaml
  │   ├── NOTES.txt
  │   ├── serviceaccount.yaml
  │   ├── service.yaml
  │   └── tests
  │       └── test-connection.yaml
  └── values.yaml # Actual values for the templates files
  
  3 directories, 11 files
  ```
* Let's delete everything in `templates`, then create two empty YAML files called `deployment.yaml` and `service.yaml`.
  After this you should have something like this:
  ```text
  boutique
  ├── charts
  ├── Chart.yaml
  ├── .helmignore
  ├── templates
  │   ├── deployment.yaml
  │   └── service.yaml
  └── values.yaml
  ```

</div> <!-- Basic structure of Helm Chart -->

## Create Basic Template File

<div id="Online-Boutique-Create-Basic-Template-File">

* `deployment.yaml`:
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: {{ .Values.appName }}
  spec:
    replicas: {{ .Values.appReplicas }}
    selector:
      matchLabels:
        app: {{ .Values.appName }}
    template:
      metadata:
        labels:
          app: {{ .Values.appName }}
      spec:
        containers:
        - name: {{ .Values.appName }}
          image: "{{ .Values.appImage }}:{{ .Values.appVersion }}"
          resources:
            limits:
              memory: "128Mi"
              cpu: "500m"
          ports:
          - containerPort: {{ .Values.containerPort }}
  ```

* `service.yaml`
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    name: {{ .Values.appName }}
  spec:
    type: {{ .Values.serviceType }}
    selector:
      app: {{ .Values.appName }}
    ports:
    - protocol: TCP
      port: {{ .Values.servicePort }}
      targetPort: {{ .Values.containerPort }}
  ```

---

### Some notes

#### `{{ .Values.xxx }}`

* `Values` Object
    * It is a built-in object
    * By default, Values is empty
    * `Values` are passed into template, from 3 sources
        * The `values.yaml` file in the chart
        * User specified file passed with `-f` flag
        * Parameters passed with `--set` flag
* Built-in Objects
    * Several objects are passed into a template from the template engine
    * Examples: `Release`, `Files`, `Values`, etc.
    * Check [this](https://helm.sh/docs/chart_template_guide/builtin_objects) out

#### Variable Naming Convention

* Names should begin with a lowercase letter
* Separated with camelcase
* Two ways of naming: `Flat` and `Nested`

---

##### Flat

* `deployment.yaml`
  ```yaml
  [...]
    spec:
      containers:
      - name: {{ .Values.containerName }}
        image: {{ .Values.containerImage }}
  [...]
  ```
* `values.yaml`
  ```yaml
  containerName: xxx
  containerImage: yyy
  ```

##### Nested

* `deployment.yaml`
  ```yaml
  [...]
    spec:
      containers:
      - name: {{ .Values.container.name }}
        image: {{ .Values.container.image }}
  [...]
  ```
* `values.yaml`
  ```yaml
  container:
    name: xxx
    image: yyy
  ```

##### **Flat** or **Nested** Values

* Values may be flat or nested deeply
* Best practice is to use flat structure, which is simpler

</div> <!-- Create Basic Template File -->

## Dynamic Environment Variables

<div id="Online-Boutique-Dynamic-Environment-Variables">

Till now, we have 2 YAML files: `deployment.yaml` and `service.yaml`.

But notice the `deployment.yaml` file is not complete yet! Each deployment has its environment variables, and we have to
add them to complete the chart, but the problem is we can't hardcode the `env` section like we used to because each
deployment has a different range of env! How can we achieve that?

The answer is `range`!

* Range:
    * Provides a "for"-style loop
    * To iterate through or "range over" a list
    * Check the [Docs](https://helm.sh/docs/chart_template_guide/control_structures/#looping-with-the-range-action)

---

* Add the env to the existing `deployment.yaml` file:
  ```yaml
  [...]
  env:
  {{- range .Values.containerEnvVars}}
  - name: {{ .key }}
    value: {{ .value | quote }}
  {{- end}}
  ```

What is this `|` symbol? --> It is Pipeline

* Pipeline
    * Same concept as UNIX
    * Tool for changing together template commands
    * [Docs](https://helm.sh/docs/chart_template_guide/functions_and_pipelines/#pipelines)

</div> <!-- Dynamic Environment Variables -->

## Set Variables

<div id="Online-Boutique-Dynamic-Set-Variables">

* Example value file for our `servicename`:
  ```yaml
  appName: servicename
  appImage: gcr.io/google-samples/microservices-demo/servicename:v0.3.6
  appVersion: v.0.0.0
  appReplicas: 1
  containerPort: 8080
  containerEnvVars:
  - key: ENV_VAR_ONE
    value: "valueone"
  - key: ENV_VAR_TWO
    value: "valuetwo"
  servicePort: 8080
  serviceType: ClusterIP
  ```

* You must create a `xxx-values.yaml` file for each deployment!

</div> <!-- Set Variables -->

## Test the Chart

<div id="Online-Boutique-Test-the-Chart">

Now everything **seems** right.

But still, it is nice to test our chart (template) before installing it.

---

* Render chart templates locally and display the output
  ```shell
  helm template boutique
  ```

---

* Examines a chart for possible issues
  ```shell
  helm lint boutique
  ```
* `helm lint` command:
    * Examines a chart for possible issues
    * `ERROR`: Issues that will cause chart to fal installation
    * `WARNING`: Issues that break with convention or recommandations

</div> <!-- Test the Chart -->

## Install the Chart

<div id="Online-Boutique-Install-the-Chart">

`helm install` command

```shell
helm install -f <VALUES.YAML-FILE> <RELEASE-NAME> <CHART-NAME>
```

---

* `helm install --dry-run`: Check generated manifest without installing the chart
* Difference of `--dry-run` and `template`:
    * `--dry-run` send files to K8s cluster, while `template` only validates it locally

---

Now we have ten values.yaml file

We have to type the `helm install ...` command ten times, or

* install.sh
  ```shell
  helm install -f values/email-service-values.yaml emailservice boutique
  helm install -f values/cart-service-values.yaml cartservice boutique
  helm install -f values/currency-service-values.yaml currencyservice boutique
  helm install -f values/payment-service-values.yaml paymentservice boutique
  helm install -f values/recommendation-service-values.yaml recommendationservice boutique
  helm install -f values/productcatalog-service-values.yaml productcatalogservice boutique
  helm install -f values/shipping-service-values.yaml shippingservice boutique
  helm install -f values/ad-service-values.yaml adservice boutique
  helm install -f values/checkout-service-values.yaml checkoutservice boutique
  helm install -f values/frontend-values.yaml frontendservice boutique
  ```
* Change the mode to executable
  ```shell
  sudo chmod u+x install.sh
  ```
* Run the script
  ```shell
  bash install.sh
  ```

* I know it sounds not entirely professional, but it considers two things
    1) It is still better than option one (Everything in a long YAML file)
    2) We will learn something called `helmfile` in the next section that makes this process easier (Instead of a bash
       script)

</div> <!-- Install the Chart -->
<p align="right">(<a href="#top">back to top</a>)</p>

# Helmfile

Please, before this section, review the <a href="#Demo-Online-Boutique-overview">Demo: Create Helm Chart for an Online
Boutique</a>. This section is a Continuation of the previous section

## What is a Helmfile?

<div id="Helmfile-What-is-a-Helmfile">

Helmfile is a **declarative** specification for deploying Helm charts that adds functionality to Helm.

* Declarative: Define the **desired** state!
* Declare a definition of an entire K8s cluster
* Change specification depending on application or type of environment
* Example of a `helmfile.yaml`:
  ```yaml
  releases:
    - chart: emailservice
      name: boutique
      values:
        - ./values/emailservice.yaml
  ```

</div> <!-- What is a Helmfile? -->

## Uninstall previous Helm Charts

<div id="Helmfile-Uninstall-previous-Helm-Charts">

Let's uninstall the previously deployed chart from our cluster

* uninstall.sh
  ```shell
  helm uninstall emailservice
  helm uninstall cartservice
  helm uninstall currencyservice
  helm uninstall paymentservice
  helm uninstall recommendationservice
  helm uninstall productcatalogservice
  helm uninstall shippingservice
  helm uninstall adservice
  helm uninstall checkoutservice
  helm uninstall frontendservice
  ```
* Change the mode to executable
  ```shell
  sudo chmod u+x uninstall.sh
  ```
* Run the script
  ```shell
  bash uninstall.sh
  ```

</div> <!-- Uninstall previous Helm Charts -->

## Create helmfile

<div id="Helmfile-Create-helmfile">

* helmfile.yaml
  ```yaml
  releases:
    - name: <RELEASE-NAME>
      chart: <CHART-NAME>
      values:
        - <VALUES.YAML-FILE>
  ```

---

So now, instead of a bash script (`install.sh`), we write everything in the `helmfile.yaml` file.

```yaml
releases:
  - name: shippingservice
    chart: boutique
    values:
      - values/shipping-service-values.yaml

  - name: adservice
    chart: boutique
    values:
      - values/ad-service-values.yaml
  - [ ... ]
```

</div> <!-- Create helmfile -->

## Install helmfile

<div id="Helmfile-Install-helmfile">

To interact with this helmfile, we have first to [install](https://github.com/roboll/helmfile#installation) `helmfile`
CLI

* Verify installation
  ```shell
  helmfile --version
  ```

</div> <!-- Install helmfile -->

## Deploy Helm Charts

<div id="Helmfile-Deploy-Helm-Charts">

* Install Helm Charts via Helnfile
  ```shell
  helmfile sync
  ```
* See the results
  ```shell
  helmfile list
  ```

</div> <!-- Deploy Helm Charts -->

## Uninstall Releases

<div id="Helmfile-Uninstall-Releases">

* To uninstall the chart
  ```shell
  helmfile destroy
  ```

</div> <!-- Uninstall Releases -->

## Wrap UP

<div id="Helmfile-Wrap-UP">

Now you learned:

1) 1 Shared Helm Chart for all microservices
2) Deploy declaratively using helmfile

There is only one final question: Where to host the Helm charts?

---

Where to host the Helm charts?

✅ Host it in a Git Repository

2 Options:

1) **WITH** your application code
2) **SEPARATE** Git Repository for Helm Charts

</div> <!-- Wrap UP -->
<p align="right">(<a href="#top">back to top</a>)</p>
