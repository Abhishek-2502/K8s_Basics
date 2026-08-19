# Helm - Package Manager of K8s

Helm is the package manager for Kubernetes. Similar to how `apt` installs and
manages packages on Linux, Helm installs and manages applications on a
Kubernetes cluster.

Helm uses packages called **charts**. A chart contains Kubernetes templates,
configuration, and related resources needed to deploy an application.

Helm is written in Go.

## Install Helm on Linux

Run the following commands to download and install Helm on a Linux machine.
After installation, check the Helm version to confirm that it is working.

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm version
helm
```

## Apache Helm Chart

### Create the Chart

The `helm create` command generates a sample chart with the standard files and
folders required for a Kubernetes application.

```bash
helm create apache-helm
cd apache-helm/
ls
sudo apt install tree
tree
```

```text
apache-helm/
|-- Chart.yaml
|-- charts/
|-- templates/
|   |-- NOTES.txt
|   |-- _helpers.tpl
|   |-- deployment.yaml
|   |-- hpa.yaml
|   |-- ingress.yaml
|   |-- service.yaml
|   |-- serviceaccount.yaml
|   `-- tests/
|       `-- test-connection.yaml
`-- values.yaml
```

### Chart Files and Folders

These files work together to create and configure the Kubernetes resources for
the application.

- `Chart.yaml`: Contains chart information such as the chart name and version.
- `charts/`: Stores chart dependencies.
- `templates/`: Contains the Kubernetes resource templates.
- `NOTES.txt`: Displays helpful notes after the chart is installed.
- `_helpers.tpl`: Contains reusable template helpers.
- `deployment.yaml`: Defines the application deployment.
- `hpa.yaml`: Defines horizontal pod autoscaling settings.
- `ingress.yaml`: Defines external access rules for the application.
- `service.yaml`: Defines how the application is accessed inside the cluster.
- `serviceaccount.yaml`: Defines the service account used by the application.
- `tests/`: Contains Helm test files.
- `values.yaml`: Contains the variables passed into the templates.

### Update the Chart

Update the service template and the values file to use the Apache image and the
required service port.

```text
vim templates/service.yaml
spec.ports.tagetPort: {{ .Values.service.targetPort }} (from http)

vim values.yaml
image.repository: httpd (from nginx)
service.targetPort: 80
```

### Package and Install

Move to the parent directory, package the chart, and install it as two separate
Helm releases in different Kubernetes namespaces.

```bash
cd ..
helm package apache-helm
helm install dev-apache apache-helm -n dev-apache-ns --create-namespace
helm install prd-apache apache-helm -n prd-apache-ns --create-namespace
```

### Verify Apache Deployments

Use `kubectl` to confirm that the pods, deployments, and services are running
in both namespaces.

```bash
kubectl get pods -n dev-apache-ns
kubectl get deployment -n dev-apache-ns
kubectl get svc -n dev-apache-ns
kubectl get pods -n prd-apache-ns
kubectl get deployment -n prd-apache-ns
kubectl get svc -n prd-apache-ns
```

## Upgrade a Helm Release

A Helm upgrade applies the latest chart or configuration changes to an existing
release.

### Update the Values

Increase the replica count and update the application version before creating
the new chart package.

```bash
vim apache-helm/values.yaml
replicaCount: 3 (from 1)
vim apache-helm/Charts.yaml
Increment appVersion (like 1.16.0 to 1.16.1)
```

### Apply the Upgrade

Package the updated chart and apply it to the production release.

```bash
helm package apache-helm
helm upgrade prd-apache apache-helm -n prd-apache-ns
```

### Verify the Upgrade

Check the pods to make sure the upgraded release is running successfully.

```bash
kubectl get pods -n dev-apache-ns
kubectl get pods -n prd-apache-ns
```

## Roll Back a Helm Release

If an upgrade causes a problem, restore the release to a previous revision.

### Roll Back to a Revision

```bash
helm rollback prd-apache revision_number -n prd-apache-ns
helm rollback prd-apache 1 -n prd-apache-ns
```

### Verify the Rollback

Confirm that the Kubernetes resources are available after the rollback.

```bash
kubectl get pods
kubectl get deployment
kubectl get svc
```

## Deploy a Node.js Image

This example creates a Helm chart for an application that uses a Node.js image.

### Create and Configure the Chart

```text
helm create node-js-app

cd node-js-app

vim templates/service.yaml
spec.ports.tagetPort: {{ .Values.service.targetPort }} (from http)

vim values.yaml
image.repository: trainwithshubham/node-app
image.tag: "latest"
service.port: 8000
service.targetPort: 8000
```

### Package and Install

Package the Node.js chart and install it in the development namespace.

```bash
cd ..
helm package node-js -app
helm install dev-node-js-app node-js-app -n dev-node-ns --create-namespace
```

### Verify the Node.js Deployment

Check the pods and service, then forward the service port so the application can
be opened from a browser.

```bash
kubectl get pods -n dev-node-ns
kubectl get svc -n dev-node-ns
kubectl port-forward svc/dev-node-js-app 8000:8000 -n dev-node-ns --address=0.0.0.0
```

### Access the Application

After port forwarding is active, open port `8000` in the cloud firewall and
access the application using the virtual machine IP address.

Open 8000 port on Cloud
Access VM_IP:8000 on browser

## Search Helm Charts

Use these commands to search for charts that are available in your configured
Helm repositories.

```text
helm package .-> Make Package when inside the folder
helm search repo repo_name
helm search repo nginx
helm repo list
```

## Helm Repositories

### Add and Update Repositories

Add a chart repository and update its local chart index before searching or
installing charts from it.

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo update

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

## OCI Charts

### Install OCI Charts

OCI charts are stored in container registries and can be installed directly
using an `oci://` chart reference.

```bash
helm install my-release oci://registry-1.docker.io/bitnamicharts/nginx
helm install nginx-helm oci://registry-1.docker.io/bitnamicharts/nginx
kubectl get pods

helm install my-release oci://registry-1.docker.io/bitnamicharts/mongodb
helm install mongodb-helm oci://registry-1.docker.io/bitnamicharts/mongodb -n mongodb-ns --create-namespace
kubectl get pods -n mongodb-ns
kubectl exec -it mongodb_pod_name -n mongodb-ns -- bash
ls
mongosh
exit
helm list -n mongodb-ns
```

## Uninstall Releases

Uninstalling a release removes the Kubernetes resources created by that Helm
release.

```bash
helm uninstall nginx-helm
helm uninstall mongodb-helm -n mongodb-ns
helm uninstall prd-apache -n prd-apache-ns
helm uninstall dev-apache -n dev-apache-ns
```
