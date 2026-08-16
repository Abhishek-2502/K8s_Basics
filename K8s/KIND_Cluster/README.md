# KIND Cluster Setup Guide

## 1. Installing KIND and kubectl
Install KIND and kubectl using the provided [script](install.sh)

## 2. Setting Up the KIND Cluster
Create a kind-config.yaml file using the provided [file](kind-config.yaml)

Create the cluster using the configuration file:

```bash

kind create cluster --config kind-config.yaml --name abhi-kind-cluster
```
Verify the cluster:

```bash

kubectl get nodes
kubectl cluster-info
```
## 3. Changing the context
Temporary
```bash

kubectl cluster-info --context abhi-kind-cluster
```

Permanent
```bash

kubectl config use-context abhi-kind-cluster
```


## 4. Setting Up the Kubernetes Dashboard
Deploy the Dashboard
Apply the Kubernetes Dashboard manifest:
```bash

kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```
Create an Admin User

Create a dashboard-admin-user.yml file using the provided [file](dashboard-admin-user.yml)

Apply the configuration:

```bash

kubectl apply -f dashboard-admin-user.yml
```
Get the Access Token
Retrieve the token for the admin-user:

```bash

kubectl -n kubernetes-dashboard create token admin-user
```
Copy the token for use in the Dashboard login.

Access the Dashboard
Start the Dashboard using kubectl proxy:

```bash

kubectl proxy
```
Open the Dashboard in your browser:

```bash

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```
Use the token from the previous step to log in.

## KIND Commands

### Check KIND version

```bash
kind version
```

### Create a cluster

Default cluster:
```bash
kind create cluster
```

Using a configuration file:
```bash
kind create cluster --config filename.yaml
```

Specify a cluster name:
```bash
kind create cluster --name my-cluster
```

Using config + name:
```bash
kind create cluster --name my-cluster --config kind-config.yaml
```

### List your clusters

```bash
kind get clusters
```

### Get cluster nodes

```bash
kind get nodes
```

### Delete a cluster

Delete the default cluster:
```bash
kind delete cluster
```

Delete a specific cluster:
```bash
kind delete cluster --name <cluster-name>
```

For the default cluster:

```bash
kind delete cluster
```

### Export kubeconfig

Configure kubectl to use a KIND cluster:
```bash
kind export kubeconfig
```

For a specific cluster:
```bash
kind export kubeconfig --name <cluster-name>
```

### Load a Docker image into KIND

If you build a Docker image locally and want to use it inside the KIND cluster:

```bash
kind load docker-image <image-name>:<tag>
```

Example:
```bash
kind load docker-image my-app:1.0
```

For a specific cluster:
```bash
kind load docker-image my-app:1.0 --name my-cluster
```

### Load an image from a tar file
```bash
kind load image-archive my-image.tar
```

### Export KIND logs

Useful when troubleshooting:
```bash
kind export logs
```

Specify an output directory:
```bash
kind export logs ./kind-logs
```

For a specific cluster:
```bash
kind export logs ./kind-logs --name my-cluster
```


## 6. Notes

Multiple Clusters: KIND supports multiple clusters. Use unique --name for each cluster.

Custom Node Images: Specify Kubernetes versions by updating the image in the configuration file.

Ephemeral Clusters: KIND clusters are temporary and will be lost if Docker is restarted.