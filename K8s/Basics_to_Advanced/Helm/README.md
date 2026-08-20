# Helm - Package Manager of K8s

Helm is the package manager for Kubernetes. Similar to how `apt` installs and
manages packages on Linux, Helm installs and manages applications on a
Kubernetes cluster.

Helm uses packages called **charts**. A chart contains Kubernetes templates,
configuration, and related resources needed to deploy an application.

Helm is written in Go.

Before using Helm, make sure `kubectl` is installed and connected to a running
Kubernetes cluster. Helm uses the same Kubernetes context as `kubectl`.

```bash
kubectl config current-context
kubectl get nodes
```

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
```

`tree` is optional and only displays the chart folders in a readable format.
Install it on Linux if it is not already available:

```bash
sudo apt install tree
tree
```

An Apache Helm chart packages the Kubernetes resources required to run Apache.
The same chart can be installed multiple times with different release names or
namespaces.

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

Helm combines these templates with the values from `values.yaml` and produces
the final Kubernetes YAML files during installation.

### Update the Chart

Update the service template and the values file to use the Apache image and the
required service port.

```bash
vim templates/service.yaml
```
```text
spec.ports.tagetPort: {{ .Values.service.targetPort }} (from http)
```

```bash
vim values.yaml
```
```text
image.repository: httpd (from nginx)
image.tag: "latest"
service.targetPort: 80
```

The service template reads the target port from `values.yaml`. This allows the
configuration to be changed without editing the Kubernetes resource directly.

### Package and Install

Move to the parent directory, package the chart, and install it as two separate
Helm releases in different Kubernetes namespaces.

```bash
cd ..
helm package apache-helm
ls
helm install dev-apache apache-helm -n dev-apache-ns --create-namespace
helm install prd-apache apache-helm -n prd-apache-ns --create-namespace
```

`dev-apache` and `prd-apache` are release names. The namespaces keep the two
installations separate.

If you are inside the chart directory, use `helm package .` to package the
current chart. Run this instead of `helm package apache-helm` when you are
already inside `apache-helm`:

```text
helm package .
```

The commands above use `helm package apache-helm` from the parent directory.
Both commands package the same chart.

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
```

```text
replicaCount: 3 (from 1)
vim apache-helm/Chart.yaml
Increment appVersion (like 1.16.0 to 1.16.1)
```

Increase `replicaCount` to run more Apache pods. Update the chart or application
version when preparing a new chart package.

### Apply the Upgrade

Package the updated chart and apply it to the production release.

```bash
helm package apache-helm
helm upgrade prd-apache apache-helm -n prd-apache-ns
```

Helm keeps a revision history for every release. Each upgrade creates a new
revision that can be inspected or restored later.

### Verify the Upgrade

Check the pods to make sure the upgraded release is running successfully.

```bash
kubectl get pods -n dev-apache-ns
kubectl get pods -n prd-apache-ns
```

After the upgrade, three pods should be running in `prd-apache-ns`.

## Roll Back a Helm Release

If an upgrade causes a problem, restore the release to a previous revision.

### Roll Back to a Revision

Replace `1` with the revision number you want to restore. This example rolls
the release back to revision `1`:

```bash
helm rollback prd-apache 1 -n prd-apache-ns
```

### Verify the Rollback

Confirm that the Kubernetes resources are available after the rollback.

```bash
kubectl get pods -n prd-apache-ns
```

## Deploy a Node.js Image

This example creates a Helm chart for an application that uses a Node.js image.

### Create and Configure the Chart

```bash
helm create node-js-app

cd node-js-app
```

The image, service port, and target port are configured in the chart values.

```bash
vim templates/service.yaml
```

```text
spec.ports.tagetPort: {{ .Values.service.targetPort }} (from http)
```

```bash
vim values.yaml
```

```text
image.repository: trainwithshubham/node-app
image.tag: "latest"
service.port: 8000
service.targetPort: 8000
```

### Package and Install

Package the Node.js chart and install it in the development namespace.

```bash
cd ..
helm package node-js-app
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

After port forwarding is active, open port `8000` in the cloud firewall and access the application using the virtual machine IP address.

Open port `8000` in the cloud firewall and access `VM_IP:8000` in a browser.

## Helm Repositories

### Add and Update Repositories

Add a chart repository and update its local chart index before searching or
installing charts from it.

The commands below show how to add repositories, refresh their chart indexes,
and search for available charts.

The `stable` repository is kept here as a legacy example. For new projects,
use a maintained repository such as `prometheus-community`.

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm repo list
```

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm repo list
```

```bash
helm search repo repo_name
helm search repo nginx
```

A repository stores packaged Helm charts. `helm repo update` downloads the
latest chart information from the configured repositories.

## OCI Charts

### Install OCI Charts

OCI charts are stored in container registries and can be installed directly
using an `oci://` chart reference.

helm install my-release oci://registry-1.docker.io/bitnamicharts/nginx
```bash
helm install nginx-helm oci://registry-1.docker.io/bitnamicharts/nginx
kubectl get pods
```

helm install my-release oci://registry-1.docker.io/bitnamicharts/mongodb
```bash
helm install mongodb-helm oci://registry-1.docker.io/bitnamicharts/mongodb -n mongodb-ns --create-namespace
kubectl get pods -n mongodb-ns
kubectl exec -it mongodb_pod_name -n mongodb-ns -- bash
ls
mongosh
exit
exit
helm list -n mongodb-ns
```

The release name is the name used to manage the installation after it is deployed.

## Uninstall Releases

Uninstalling a release removes the Kubernetes resources created by that Helm
release.

```bash
helm uninstall prd-apache -n prd-apache-ns
helm uninstall dev-apache -n dev-apache-ns
helm uninstall nginx-helm
helm uninstall mongodb-helm -n mongodb-ns
helm uninstall dev-node-js-app -n dev-node-ns
```

Use the same release name and namespace used during installation. Uninstalling
a release does not delete the chart package from the local machine or registry.

## Cleanup
```bash
kubectl delete ns prd-apache-ns
kubectl delete ns dev-apache-ns
kubectl delete ns dev-node-ns
kubectl delete ns mongodb-ns
```
