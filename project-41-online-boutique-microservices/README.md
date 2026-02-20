# Online Boutique Assignment

The CI-CD system of your organization is broken and you have been asked to deploy the latest release on the Production environment, but as a prerequisite you are supposed to first deploy the application on your a test environment (your local machine) and see if the application is ready to be promoted on the Production cluster or not.

The latest release has some critical bug fixes as well as some most anticipated features that you clients were asking for. So the release has to be taken on the Production as early as possible. Now you are left only with the Kubernetes YAML manifests files and the instructions to deploy/test the application on the local environment.

You are supposed to go through this document, understand the problem statement carefully, deploy the application by following the instructions, find and fix any issues and submit the solution. You are supposed to explain the RCA (Root Cause Analysis) of all the problems (write it down in file `SOLUTION.md` file).

## Problem Description:

The E-commerce website `Online Boutique` is a microservices-based application that has 11 microservices. These microservices are supposed to be deployed on a Kubernetes cluster using [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and their respective [Services](https://kubernetes.io/docs/concepts/services-networking/service/) to expose them internally in the cluster. There is one additional service (named `frontend-external` of type `NodePort`) used to expose the application outside of the cluster.


### Your goals are to

1. Create a multi-node Kubernetes cluster (using kind) and deploy the application on it.
2. Troubleshoot the Kubernetes resources, make sure that all the Kubernetes resources are in their desired state. (meaning Pods are `Running`, service-Deployment mapping are configured properly.)
3. Troubleshoot the application and check if it behaves normally by running a manual testing flow as well as running an automation script that generates load on the application.

## Prerequisites:
### Kubernetes concepts:

A basic understanding of the following Kubernetes concepts will be required to solve the assignment. If you are not familiar with these concepts, then you can explore the official documentation of Kubernetes by using the following links.

- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Pod Scheduling](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)
- [ServiceAccounts](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)

### System requirements: 
In order to attempt this assignment your workstation machine should match the following requirements.

Hardware requirements:

- At least 8GB of system memory
- At least 4 CPU cores

Installations:

- Docker: In order to create a local cluster on the developer's machine, Docker must be already installed, if not check [here](https://docs.docker.com/engine/install/) for the installation steps.
- `kubectl`: binary installed on your workstation to access the cluster. [Installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/).
- [KinD](https://kind.sigs.k8s.io/docs/user/quick-start/): kubernetes local cluster provisioning utility tool. You can install it from [here](https://kind.sigs.k8s.io/docs/user/quick-start/#installation).

## Steps

  - Clone this repository to your machine. (**Don't fork it**).
  - Create a new **private** repository on GitHub on your Github account.
  - Create a file named `SOLUTION.md` under the root directory of the repository. Write all the problems and their solutions (the root cause and the change required to solve the issue) in the `SOLUTION.md` file.
  
  Example:
  `Error 1`: The "XXX" service pod is going in "ImagePullBackOff" state.
  `Solution`: The "XXX" YAML manifest had a typo in `image` value, after updating the image repository the error disappeared.

### Please note
  - Any step from the assignment does **not** require you to modify the container image, or build your own container image at all.
  - Make sure all the files you create or modify have the exact same names as given.
  - Don't commit all of your work as a single commit, commit it as you finish each part, so we can see the work as you built it up.
  - Reading this document carefully is the key to solve this assignment. Feel free to go through the official documentation of Kubernetes.
  - If you need more time or are stuck at some point, don't hesitate to reach out to us.


## Guidelines:

1. This assignment is divided in 3 parts, Part-A, Part-B, and Part-C. 
2. For every part, you will have to perform certain task(s). Make sure whenever you make any changes in the YAML manifests to solve any problem, you should commit the changes. The Part-A won't need any changes in th kind-config file.
3. The `SOLUTION.md` file also needs to be updated with a small description of the exact problem/error and it's solution. You can also mention the commands that are required to perform any operation while solving any issue.
4. This assignment will require the changes to be made only in the Kubernetes manifests files. There is no need to make any changes in the application code, Docker images.
5. Try to find the minimal changes to fix any issue.
6. You need to use the `kind` cluster only and use the given kind config file(`kind-config/config.yaml`). Check the Assignment Part-A.

### Ideal State of the application services:

- The given table lists all the Services and their ideal port mappings with the respective containers.

    | serviceName           | servicePort | targetPort |
    |-----------------------|-------------|------------|
    | adservice             | 9555        | 9555       |
    | cartservice           | 7070        | 7070       |
    | checkoutservice       | 5050        | 5050       |
    | currencyservice       | 7000        | 7000       |
    | emailservice          | 5000        | 8080       |
    | frontend              | 80          | 8080       |
    | paymentservice        | 50051       | 50051      |
    | productcatalogservice | 3550        | 3550       |
    | recommendationservice | 8080        | 8080       |
    | redis-cart            | 6379        | 6379       |
    | shippingservice       | 50051       | 50051      |


- Now in order to the application work properly, all of the Kubernetes resources i.e. Deployments, Services, Pods need to be in their desired state.
- All the service Pods are supposed to use the `default` serviceAccount.
- These services can be accessed from within the same namespace using their DNS address in the format of `$SERVICE_NAME:$SERVICE_PORT`. 
- Some of the services communicates with other services using their DNS Address. If any service can not communicate with other service, then the application would fail to perform normally.
- The required DNS addresses are mounted as environment variables in the respective Pod containers.

## Assignment- Part-A - Setup the cluster

1. Let's first create the kind cluster, on your local environment. Use the following command to create the cluster from the root directory of the repo.

   ```shell
   kind create cluster --name qa-cluster --config kind-config/config.yaml
   ```
   It may take few minutes to the cluster to be ready. Once the cluster is ready you should be able able to see following output of the command `kubectl get nodes`

   ```shell
   NAME                       STATUS   ROLES                  AGE    VERSION
   qa-cluster-control-plane   Ready    control-plane,master   2m2s   v1.20.7
   qa-cluster-worker          Ready    <none>                 83s    v1.20.7

   ```

## Assignment- Part-B - Deployment Issues.

1. Let's deploy the boutique application using the YAML manifests present under `deploy/` directory.

   ```shell
   kubectl apply -f deploy/
   ```

   Once you run the above command, you will see that a bunch of Deployments, Services, Pods are getting created on the cluster in the `default` namespace. You can run the command `kubectl get all` to check the status of these resources.

2. Check if all the Deployments are in their desired state.
3. Make sure all the Pods are in running state. Check if any Pods are in `Pending` state. If yes, then try to fix them. Once there are no Pods in `Pending` state, see if all of the Pods enter in `ContainerCreating` state. If yes then wait for some time. Sit back and relax, it may take up to 20-25 min for all the necessary docker images to get downloaded. So feel free to grab a cup of tea/coffee.
4. Check if any pod is failing due to any other issue. Now once all the images are downloaded, see if the Pods are in `Running` state or not. If not then try to find the reason of their failure and fix them. You must see all the 11 service-Pods to be Running.

Once you solve the above issues, make sure you commit the changes in the respective YAML manifest files.

## Assignment- Part-C - Application Issues.

Once all the Pods are in running state, try to access the appication from your browser. To expose the `frontend-external` service you can use `kubectl port-forward`. (If you don't know about port-forwarding, then check the [link](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/).)

1. From the browser check if the application is working properly or not, if you face any issue then try to fix the issue, what could be a possible reason of the failure.
**Hint** Check the logs of the Pods, start from the `frontend` service. Check if the frontend service is able to communicate with other services or not.

   The home page must look as shown in the image.

   ![HomePage](media/home-page.png?raw=true "Online Boutique")


2. After making sure that the application is running and also accessible from the browser.
   As part of the sanity test you are supposed to  validate if the user is able to place orders or not.
   You can perform the following steps to perform sanity testing.

   **Go to home > Add Few Products to the Cart > Update the Payment details > and hit `Place Order`**. If the order is not being complete, then try to find the root cause of the issue, fix it and commit your changes.

   After placing a successful order you should see a success messge with some details about the order.

   ![OrderPlaced](media/order-placed.png?raw=true "Order Placed")

Once you solve the above issues, make sure you commit the changes in the respective YAML manifests and update the RCA in the `SOLUTION.md` file.

3. At last run the `loadgenerator` app by deploying it in the `qa` namespace. Use the following command.

   ```shell
   kubectl apply -f test/loadgenerator.yaml
   ```

   Collect the logs of the `loadgenerator` pod and save it into a text file `test/loadgenerator-output.txt`. Make sure there are no failures in the load-generator reports. To fix the failures, make the necessary changes in `test/loadgenerator.yaml`, commit the changes along with the `test/loadgenerator-output.txt` file which has no failures.


## Submitting the solution

You have to commit and push all the changes to your own private repository that you created earlier on Github. Once you have pushed all the commits,

- Add `anju-infracloud` as collaborators to the repository.
- Reply to the email with link to your repository / send an email to `anju [at] infracloud [dot] io`.


The files from the [`deploy`](./deploy) directory are from the [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo) application. It is developed and maintained by the *[The Google Cloud Platform Team](https://github.com/GoogleCloudPlatform)*, and is licensed under [Apache-2.0 License](https://github.com/GoogleCloudPlatform/microservices-demo/blob/master/LICENSE).
