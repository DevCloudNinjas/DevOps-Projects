###Create a namespace 
```bash
kubectl create namespace webapps
```

###service account

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins
  namespace: webapps
```

###Role
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: webapps
  name: role
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["get", "list", "create", "delete", "patch", "watch"]
```

###Rolebinding
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rolebinding
  namespace: webapps
subjects:
- kind: ServiceAccount
  name: jenkins # The service account created earlier
  namespace: webapps
roleRef:
  kind: Role
  name: role  # The role created earlier
  apiGroup: rbac.authorization.k8s.io
```

####Token for Service Account secret

```yaml 
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: mysecretname
  namespace: webapps  # Make sure to specify the correct namespace
  annotations:
    kubernetes.io/service-account.name: jenkins  # The service account name
```

###Apply all the yaml files, 
```bash
kubectl apply -f serviceaccount.yaml
kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml
kubectl apply -f sa-token.yaml
```

###Imagepullscret
```bash
kubectl create secret docker-registry regcred \
--docker-server=https://index.docker.io/v1/ \
--docker-username=<your-username> \
--docker-password=<your-password>
--namespace=webapps
```