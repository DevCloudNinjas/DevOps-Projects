# PERSISTING DATA IN KUBERNETES
## INTRODUCTION

The pods created in Kubernetes are ephemeral, they don't run for long. When a pod dies, any data that is not part of the container image will be lost when the container is restarted because Kubernetes is best at managing stateless applications which means it does not manage data persistence. To ensure data persistent, the PersistentVolume resource is implemented to acheive this.

The following outlines the steps:

## STEP 1: Setting Up AWS Elastic Kubernetes Service With EKSCTL

- Downloading and extracting the latest release of **eksctl** with the following command:`$ curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp`
- Moving the extracted binary to **/usr/local/bin**:`$ sudo mv /tmp/eksctl /usr/local/bin`
- Testing the installation was successful with the following command:`$ eksctl version`

![](./img/project22/11-installing%20eksctl.png)

- Setting up EKS cluster with a single commandline:
```
$ eksctl create cluster \
  --name my-eks-clusters \
  --version 1.21 \
  --region us-east-1 \
  --nodegroup-name worker-nodes \
  --node-type t2.medium \
  --nodes 2
 ```
 ![](./img/project22/12-setting%20up%20eks%20from%20cli.png)
 ![](./img/project22/12-setting%20up%20eks%20from%20cli-2.png)
 
## STEP 2: Creating Persistent Volume Manually For The Nginx Application

- Creating a deployment manifest file for the Nginx application and applying it:
```
sudo cat <<EOF | sudo tee ./nginx-pod.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
EOF
```
![](./img/project23/11-creating%20nginx%20deploy%20file.png)

![](./img/project23/12-creating%20nginx%20deployment.png)

- Verifying that the pod is running: `$ kubectl get pod`
- Exec into the pod and navigating to the nginx configuration file:

![](./img/project23/13-exec%20into%20one%20of%20the%20pods.png)

- When creating a volume it must exists in the same region and availability zone as the EC2 instance running the pod. To confirm which node is running the pod:`kubectl get po nginx-deployment-6fdcffd8fc-tbvfk -o wide`

![](./img/project23/14-knowing%20the%20location%20of%20one%20of%20the%20pod.png)

- To check the Availability Zone where the node is running:`kubectl describe node ip-10-0-8-60.us-west-1.compute.internal`

![](./img/project23/15-locating%20the%20az%20of%20the%20node.png)

- Creating a volume in the Elastic Block Storage section in AWS in the same AZ as the node running the nginx pod which will be used to mount volume into the Nginx pod.

![](./img/project23/16-creating%20volume.png)

- Updating the deployment configuration with the volume spec and volume mount:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: nginx-volume
          mountPath: /usr/share/nginx/
      volumes:
      - name: nginx-volume
        awsElasticBlockStore:
          volumeID: "vol-07b537651bbe68be0"
          fsType: ext4
```
![](./img/project23/17-persisting%20the%20nginx%20pod-2.png)

![](./img/project23/17-persisting%20the%20nginx%20pod.png)

- But the problem with this configuration is that when we port forward the service and try to reach the endpoint, we will get a 403 error. This is because mounting a volume on a filesystem that already contains data will automatically erase all the existing data. To solve this issue is by implementing Persistent Volume(PV) and Persistent Volume claims(PVCs) resource.

![](./img/project23/18-creating%20nginx%20service.png)

![](./img/project23/18-nginx%20data%20removed.png)

## STEP 3: Managing Volumes Dynamically With PV and PVCs

- PVs are resources in the cluster. PVCs are requests for those resources and also act as claim checks to the resource.By default in EKS, there is a default storageClass configured as part of EKS installation which allow us to dynamically create a PV which will create a volume that a Pod will use.
- Verifying that there is a storageClass in the cluster:`$ kubectl get storageclass`
- Creating a manifest file for a PVC, and based on the gp2 storageClass a PV will be dynamically created:
```
apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: nginx-volume-claim
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 2Gi
      storageClassName: gp2
```
- Checking the setup:`$ kubectl get pvc`

![](./img/project23/19-creating%20pvc.png)

- Checking for the volume binding section:`$ kubectl describe storageclass gp2`

![](./img/project23/20-troubleshooting-2.png)

![](./img/project23/20-troubleshooting.png)

- The PVC created is in pending state because PV is not created yet. Editing the nginx-pod.yaml file to create the PV:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: nginx-volume-claim
          mountPath: /tmp/somexdir
      volumes:
      - name: nginx-volume-claim
        persistentVolumeClaim:
          claimName: nginx-volume-claim
```
-  The '/tmp/somexdir' directory will be persisted, and any data written in there will be stored permanetly on the volume, which can be used by another Pod if the current one gets replaced.
- Checking the dynamically created PV:`$ kubectl get pv`

![](./img/project23/21-creating%20pvc%20automatically.png)

![](./img/project23/22-pvc%20created%20in%20the%20console.png)

- Another approach is creating a **volumeClaimTemplate** within the Pod spec of nginx-pod.yaml file so rather than having 2 manifest files, everything will be defined within a single manifest:
```
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx-statefulset
spec:
  selector:
    matchLabels:
      tier: frontend
  serviceName: nginx-service
  replicas: 1  
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80 
        volumeMounts:
        - name: nginx-volume
          mountPath: /tmp/somex
  volumeClaimTemplates:
  - metadata:
      name: mginx-volume
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 5Gi
      storageClassName: standard
```

![](./img/project23/creating%20nginx-pod.png)

## STEP 4: Use Of ConfigMap As A Persistent Storage

- ConfigMap is an API object used to store non-confidential data in key-value pairs. It is a way to manage configuration files and ensure they are not lost as a result of Pod replacement.
- To demonstrate this, the HTML file that came with Nginx will be used.
- Exec into the container and copying the HTML file:
```
$ kubectl exec nginx-deployment-6fdcffd8fc-77rfh -i -t -- bash

$ cat /usr/share/nginx/html/index.html 
```

![](./img/project23/24-reconfiguring%20for%20configmap.png)

- Creating the ConfigMap manifest file and customizing the HTML file and applying the change:
```
cat <<EOF | tee ./nginx-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: website-index-file
data:
  # file to be mounted inside a volume
  index-file: |
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to Nginx!</title>
    <style>
    html { color-scheme: light dark; }
    body { width: 35em; margin: 0 auto;
    font-family: Tahoma, Verdana, Arial, sans-serif; }
    </style>
    </head>
    <body>
    <h1>Welcome to Nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
EOF
```
![](./img/project23/25-creating%20configmap%20file.png)

- Updating the deployment file to use the configmap in the volumeMounts section
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    tier: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
          - name: config
            mountPath: /usr/share/nginx/html
            readOnly: true
      volumes:
      - name: config
        configMap:
          name: website-index-file
          items:
          - key: index-file
            path: index.html
```
- Now the **index.html** file is no longer ephemeral because it is using a configMap that has been mounted onto the filesystem. This is now evident when you exec into the pod and list the **/usr/share/nginx/html** directory

![](./img/project23/26-to%20show%20that%20configmap%20worked.png)

- To see the configmap created:`$ kubectl get configmap`
- To see the change in effect, updating the configmap manifest:`$ kubectl edit cm website-index-file`
```
 <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to ChassTech Services!</title>
    <style>
    html { color-scheme: light dark; }
    body { width: 35em; margin: 0 auto;
    font-family: Tahoma, Verdana, Arial, sans-serif; }
    </style>
    </head>
    <body>
    <h1>Welcome to ChassyTech Services!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
```

![](./img/project23/editing%20the%20config%20map-1.png)

![](./img/project23/editing%20the%20configmap.png)

- Without restarting the pod, the site should be loaded automatically.
- Performing the Port forwarding command and accessing it through the browser:

![](./img/project23/accessing%20the%20browser%20to%20view%20the%20change.png)

- To perform a restart:`$ kubectl rollout restart deploy nginx-deployment`



