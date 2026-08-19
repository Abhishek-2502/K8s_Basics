# Helm Detailed Guide

This guide explains the main Helm concepts and commands in more detail. Use
[README.md](README.md) for the short command-based version.

## Before you begin

Make sure a Kubernetes cluster is running and that `kubectl` is connected to
the correct cluster. Helm uses the same kubeconfig and current context as
`kubectl`.

```bash
kubectl config current-context
kubectl get nodes
```

## 1. What is Helm?

Helm is a package manager for Kubernetes. A Helm package is called a **chart**.
A chart contains templates for Kubernetes resources and default values.

Helm creates a **release** whenever a chart is installed. The same chart can be
installed many times with different release names, namespaces, or values.

The chart is the package you install. The release is the running instance of
that chart in a Kubernetes cluster.

```text
Chart: apache-helm
  Release: dev-apache in dev-apache-ns
  Release: prd-apache in prd-apache-ns
```

Helm uses the same kubeconfig and current context as `kubectl`.

```bash
kubectl config current-context
kubectl get nodes
helm version
```

## 2. Chart structure

Create a starter chart:

```bash
helm create my-app
```

Typical structure:

```text
my-app/
|-- Chart.yaml
|-- values.yaml
|-- charts/
|-- templates/
|   |-- _helpers.tpl
|   |-- deployment.yaml
|   |-- service.yaml
|   |-- ingress.yaml
|   |-- hpa.yaml
|   |-- serviceaccount.yaml
|   |-- NOTES.txt
|   `-- tests/
`-- .helmignore
```

### Chart.yaml

`Chart.yaml` contains chart metadata:

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
```

- `version` is the chart version and should change when the chart changes.
- `appVersion` is the application version.
- `type` is normally `application`; reusable helper charts use `library`.

### values.yaml

`values.yaml` contains default configuration. Templates read values using
`.Values`.

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: "1.27"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 80
```

### templates/

Files in `templates/` are rendered into Kubernetes YAML. Files beginning with
an underscore, such as `_helpers.tpl`, are helper files and are not rendered
as resources.

## 3. Install Helm

### Linux

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm version
```

### Windows

```powershell
winget install Helm.Helm
helm version
```

Helm 3 does not require Tiller. It communicates with the Kubernetes API using
the current kubeconfig context.

## 4. Templates and values

A template uses Go template syntax:

```yaml
spec:
  replicas: {{ .Values.replicaCount }}
```

Nested values use dot notation:

```yaml
port: {{ .Values.service.port }}
targetPort: {{ .Values.service.targetPort }}
```

### Values files

Create separate files for different environments:

```yaml
# values-prod.yaml
replicaCount: 3
image:
  tag: "1.27"
service:
  type: LoadBalancer
```

Use the file during installation or upgrade:

```bash
helm upgrade --install my-app ./my-app \
  -n production \
  --create-namespace \
  -f values-prod.yaml
```

The values file path is relative to your current directory. Run the command
from the directory that contains both `my-app/` and `values-prod.yaml`, or use
the full path to the values file.

### `--set`

Use `--set` for a small temporary override:

```bash
helm install my-app ./my-app \
  -n dev \
  --set replicaCount=1 \
  --set image.tag=latest
```

A common precedence order is:

```text
values.yaml < values-dev.yaml < values-prod.yaml < --set
```

Later values override earlier values.

When using multiple files, specify them in the same order as the precedence
shown above. Values supplied with `--set` override values from the files.

### Conditionals

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "my-app.fullname" . }}
{{- end }}
```

### Loops

```yaml
{{- range .Values.extraEnv }}
- name: {{ .name | quote }}
  value: {{ .value | quote }}
{{- end }}
```

### Defaults and required values

```yaml
environment: {{ .Values.environment | default "dev" | quote }}
repository: {{ required "image.repository is required" .Values.image.repository }}
```

### Helpers

Define reusable template code in `_helpers.tpl`:

```gotemplate
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
```

Use it in a resource:

```yaml
metadata:
  name: {{ include "my-app.name" . }}
```

Use `nindent` when inserting multi-line YAML:

```yaml
metadata:
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
```

Most template errors are caused by incorrect YAML indentation. Always render
the chart locally before installing it.

## 5. Validate and render a chart

Lint the chart:

```bash
helm lint ./my-app
```

Render templates without installing anything:

```bash
helm template my-app ./my-app
helm template my-app ./my-app -f values-prod.yaml
helm template my-app ./my-app --debug
```

Validate the rendered YAML with a client-side Kubernetes dry run:

```bash
helm template my-app ./my-app -f values-prod.yaml > rendered.yaml
kubectl apply --dry-run=client -f rendered.yaml
```

This checks the rendered resource format locally. It does not create resources
and does not replace a real cluster-side validation.

## 6. Install and inspect releases

Use a unique release name in each namespace. The release name is used later
with commands such as `helm status`, `helm upgrade`, and `helm uninstall`.

Install a chart from a directory:

```bash
helm install my-app ./my-app \
  --namespace my-app-ns \
  --create-namespace
```

Install or upgrade with one command:

```bash
helm upgrade --install my-app ./my-app \
  -n my-app-ns \
  --create-namespace \
  --wait \
  --timeout 5m
```

List releases:

```bash
helm list -n my-app-ns
helm list -A
helm status my-app -n my-app-ns
```

Inspect an installed release:

```bash
helm get values my-app -n my-app-ns
helm get values my-app -n my-app-ns --all
helm get manifest my-app -n my-app-ns
helm get notes my-app -n my-app-ns
helm get all my-app -n my-app-ns
```

## 7. Upgrade, history, and rollback

Upgrade after changing values or templates:

```bash
helm lint ./my-app
helm upgrade my-app ./my-app -n my-app-ns -f values-prod.yaml --wait
```

View revisions:

```bash
helm history my-app -n my-app-ns
```

Rollback to revision `1`:

```bash
helm rollback my-app 1 -n my-app-ns --wait
```

Uninstall a release:

```bash
helm uninstall my-app -n my-app-ns
```

Keep release history after uninstalling:

```bash
helm uninstall my-app -n my-app-ns --keep-history
```

## 8. Repositories and existing charts

Add and update an HTTP chart repository:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm repo list
helm search repo prometheus
helm search repo prometheus --versions
```

Inspect a chart before installing:

```bash
helm show chart prometheus-community/prometheus
helm show values prometheus-community/prometheus
helm show readme prometheus-community/prometheus
```

Install a chart from the repository:

```bash
helm install prometheus prometheus-community/prometheus \
  -n monitoring \
  --create-namespace
```

Download a chart locally:

```bash
helm pull prometheus-community/prometheus --untar
```

## 9. OCI charts

Helm can install charts from OCI registries. OCI references begin with
`oci://`:

```bash
helm install nginx-helm \
  oci://registry-1.docker.io/bitnamicharts/nginx
```

Install MongoDB in its own namespace:

```bash
helm install mongodb-helm \
  oci://registry-1.docker.io/bitnamicharts/mongodb \
  -n mongodb-ns \
  --create-namespace
kubectl get pods -n mongodb-ns
helm list -n mongodb-ns
```

## 10. Dependencies

Declare a dependency in `Chart.yaml`:

```yaml
dependencies:
  - name: redis
    version: "19.x.x"
    repository: "https://charts.bitnami.com/bitnami"
```

Download dependencies:

```bash
helm dependency update ./my-app
helm dependency build ./my-app
helm dependency list ./my-app
```

Dependencies are stored under the chart's `charts/` directory. Read the
subchart's values documentation before configuring it.

## 11. Package and publish charts

Increase the chart `version` in `Chart.yaml` before packaging a changed chart.
The package filename includes that version.

Package a chart:

```bash
helm lint ./my-app
helm package ./my-app
helm package ./my-app --destination ./packages
```

Inspect or render a package:

```bash
helm show chart ./packages/my-app-0.1.0.tgz
helm template my-app ./packages/my-app-0.1.0.tgz
```

Push a package to an OCI registry:

```bash
helm registry login registry.example.com
helm push ./packages/my-app-0.1.0.tgz oci://registry.example.com/helm
```

Replace `registry.example.com` with your registry address. The registry must
support OCI artifacts, and you must have permission to push to it.

## 12. Hooks and tests

Hooks run at specific points in a release lifecycle. For example, a Job can
run before an upgrade:

```yaml
metadata:
  annotations:
    helm.sh/hook: pre-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
```

Common hooks include `pre-install`, `post-install`, `pre-upgrade`,
`post-upgrade`, `pre-rollback`, and `post-rollback`.

Charts can include test resources under `templates/tests/`:

```bash
helm test my-app -n my-app-ns
```

Keep hooks small and repeatable because a failed hook can make a release fail.

## 13. Troubleshooting

Check release status and Kubernetes events:

```bash
helm status my-app -n my-app-ns
kubectl get events -n my-app-ns --sort-by=.lastTimestamp
kubectl get pods -n my-app-ns
```

Inspect a failing pod:

```bash
kubectl describe pod <pod-name> -n my-app-ns
kubectl logs <pod-name> -n my-app-ns
```

For template errors, render locally:

```bash
helm lint ./my-app
helm template my-app ./my-app --debug
```

For failed upgrades, inspect history and roll back to a known-good revision:

```bash
helm history my-app -n my-app-ns
helm get manifest my-app -n my-app-ns
helm rollback my-app <revision> -n my-app-ns
```

Common causes include incorrect indentation, missing values, wrong image names,
namespace mistakes, insufficient RBAC permissions, and resources already owned
by another Helm release.

## 14. Production checklist

- Pin chart versions and container image tags.
- Keep secrets out of Git and chart packages.
- Use separate values files for each environment.
- Set resource requests, limits, and health probes.
- Run `helm lint` and `helm template` in CI.
- Review rendered manifests before production deployment.
- Use `--wait` and a suitable `--timeout` in automation.
- Test upgrades and rollbacks before production.
- Keep `Chart.yaml` `version` and `appVersion` accurate.
- Review RBAC resources carefully.
