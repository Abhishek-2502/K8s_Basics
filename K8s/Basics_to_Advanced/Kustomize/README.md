# Kustomize

Kustomize is a Kubernetes configuration-management tool. It lets us compose and customize ordinary Kubernetes YAML without copying the same manifest for every environment. It is built into `kubectl`, so no template language or separate server is required.

This guide explains the important concepts and provides a practical demo. The demo deploys the same web application to `dev` and `prod` with different names, replicas, images, ConfigMaps, and resource settings.

### Kustomize in simple terms

Think of Kustomize as layers:

1. The **base** contains the common application YAML.
2. An **overlay** says what is different for one environment.
3. Kustomize combines both and produces the final Kubernetes YAML.
4. You inspect that YAML or apply it to a cluster.

For this demo, the base describes one web application. The dev overlay adds dev settings, and the prod overlay adds prod settings. The application YAML is reused instead of copied.

## 1. Why Kustomize?

A team usually has one application but several environments:

- Development needs fewer replicas and small resource requests.
- Production needs more replicas, stricter resources, and a different image tag.
- Namespaces, labels, hostnames, and configuration can vary by environment.

Copying complete YAML files causes drift. Kustomize keeps valid Kubernetes YAML as a base and applies declarative customizations through overlays.

### Kustomize versus Helm

| Kustomize | Helm |
| --- | --- |
| Uses native YAML and patches | Uses Go templates and values |
| No templating language required | Strong package and release-management features |
| Built into `kubectl` | Requires Helm CLI |
| Excellent for repository-local overlays | Excellent for reusable charts and third-party distribution |
| Changes are made using patches and transformers | Changes are made using templates and values |
| Usually easier to read because the output stays close to normal YAML | Can become harder to read when templates contain complex logic |
| Does not manage releases or release history by itself | Tracks releases, revisions, and installed chart versions |
| Rollback is normally handled with Git or `kubectl rollout undo` | Supports chart release rollback with `helm rollback` |
| Best when the application manifests already exist in your repository | Best when packaging and distributing an application is important |
| Overlays are commonly stored as folders such as `overlays/dev` and `overlays/prod` | Environments are commonly configured through separate values files |
| No central chart repository is required | Charts can be published to and installed from chart repositories or OCI registries |
| Debugging starts by inspecting rendered YAML with `kubectl kustomize` | Debugging often uses `helm template` or `helm install --dry-run --debug` |
| Secret generators create Kubernetes Secret manifests but do not encrypt them | Helm templates can create Secret manifests but also do not encrypt them automatically |
| Small focused customizations are straightforward | Large applications can benefit from Helm's reusable chart helpers |

They can also be used together. For example, Kustomize can customize YAML rendered by a Helm chart.

## 2. Important vocabulary

### Base

A base is reusable, environment-neutral configuration. It normally contains Deployments, Services, ConfigMaps, and a `kustomization.yaml` file.

The base should describe what the application needs, not where it is being deployed. In this demo, the base does not choose a dev or prod namespace.

### Overlay

An overlay references a base and adds environment-specific changes. An overlay should contain only the differences for that environment.

An overlay is the folder you normally build or apply for a particular environment, such as `demo/overlays/dev`.

### `kustomization.yaml`

This is the entry point. It lists resources and declares transformations such as `namePrefix`, `namespace`, `images`, `replicas`, generators, and patches.

When you run a command against a directory, Kustomize looks for this file in that directory and follows the resources listed inside it.

### Patch

A patch changes selected fields without repeating the entire resource. Kustomize supports strategic merge patches and JSON 6902 patches. Use a small strategic merge patch for normal Kubernetes resources and JSON 6902 when an exact operation or field path is needed.

## 3. Common features

| Feature | Example | Use |
| --- | --- | --- |
| `resources` | `- deployment.yaml` | Include manifests or another kustomization |
| `namePrefix` / `nameSuffix` | `dev-` | Prevent environment name collisions |
| `namespace` | `training-dev` | Set a namespace consistently |
| `commonLabels` | `app.kubernetes.io/part-of` | Add shared labels |
| `commonAnnotations` | `owner: platform` | Add metadata |
| `images` | `newTag: "1.27"` | Change image repositories or tags |
| `replicas` | `count: 3` | Change Deployment or StatefulSet scale |
| `configMapGenerator` | `behavior: merge` | Generate configuration |
| `secretGenerator` | `literals` or `envs` | Generate Secrets; never commit real credentials |
| `patches` | `path: patch.yaml` | Apply focused changes |
| `components` | reusable optional component | Share opt-in configuration |

Kustomize also supports replacements, transformers, and remote bases. Check the installed client version because fields and behavior can vary between releases.

### What happens when Kustomize builds?

Kustomize reads the base resources, applies the overlay changes, generates ConfigMaps or Secrets, rewrites names where necessary, and prints one final set of Kubernetes resources. Kubernetes receives only this final output when you use `kubectl apply -k`.

## 4. Directory layout

```text
Kustomize/
|-- README.md
`-- demo/
    |-- base/
    |   |-- deployment.yaml
    |   |-- service.yaml
    |   |-- kustomization.yaml
    |   `-- app-config.env
    `-- overlays/
        |-- dev/
        |   |-- kustomization.yaml
        |   `-- resource-patch.yaml
        `-- prod/
            |-- kustomization.yaml
            `-- resource-patch.yaml
```

The `staging` overlay and CI workflow are created in the practice exercises below; they are not required for the initial demo.

## 5. Understand the demo

The base contains one Deployment and one Service. It uses `app-config.env` with `APP_ENV=base` to generate a ConfigMap named `web-config`.

The dev overlay adds the `dev-` prefix, uses namespace `training-dev`, sets one replica, uses `nginx:1.27-alpine`, merges `APP_ENV=development`, and applies small resource settings.

The prod overlay adds the `prod-` prefix, uses namespace `training-prod`, sets three replicas, uses `nginx:1.27`, merges `APP_ENV=production`, and applies larger resource settings.

Kustomize rewrites generated names in references. For example, the Deployment's ConfigMap reference continues to point to the hash-suffixed ConfigMap generated by the same overlay.

## 6. Run the practical demo

Prerequisites:

- A Kubernetes cluster, such as Minikube, KIND, or Docker Desktop Kubernetes.
- `kubectl` installed with Kustomize support.

Run these commands from this `Kustomize` directory:

Before applying the demo, create the namespaces used by the overlays. Kustomize can add a namespace field to a resource, but it does not create that namespace unless a `Namespace` resource is included.

```bash
# Create the namespaces once; do not fail if they already exist.
kubectl create namespace training-dev --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace training-prod --dry-run=client -o yaml | kubectl apply -f -

# Render the dev YAML without changing the cluster.
kubectl kustomize demo/overlays/dev
# Render the prod YAML without changing the cluster.
kubectl kustomize demo/overlays/prod

# Inspect key differences in the dev output.
kubectl kustomize demo/overlays/dev | grep -E '^(  name:|  namespace:|      replicas:|        image:|    APP_ENV:|          cpu:)'
# Inspect key differences in the prod output.
kubectl kustomize demo/overlays/prod | grep -E '^(  name:|  namespace:|      replicas:|        image:|    APP_ENV:|          cpu:)'

# Build and apply the dev resources.
kubectl apply -k demo/overlays/dev
# Build and apply the prod resources.
kubectl apply -k demo/overlays/prod

# List resources created in dev.
kubectl get all -n training-dev
# List resources created in prod.
kubectl get all -n training-prod

# List the generated dev ConfigMap.
kubectl get configmap -n training-dev


# Describe the dev Deployment.
kubectl describe deployment dev-web -n training-dev
# Describe the Prod Deployment.
kubectl describe deployment prod-web -n training-prod

# Preview changes after editing a base or overlay, without applying them.
kubectl diff -k demo/overlays/dev

# Delete the dev resources.
kubectl delete -k demo/overlays/dev
# Delete the prod resources.
kubectl delete -k demo/overlays/prod
```

`kubectl apply -k` builds the kustomization and applies the rendered resources. The `-k` flag is different from `-f`, which applies YAML files without Kustomize processing.

If you are learning, run the render command first. It lets you see exactly what will be sent to Kubernetes before you run the apply command.

### `kubectl kustomize` versus `kubectl apply -k`

Both commands process the same Kustomize directory, but they have different results:

```bash
# Build and print the final YAML only; the cluster is not changed.
kubectl kustomize demo/overlays/dev

# Build the final YAML and create or update those resources in the cluster.
kubectl apply -k demo/overlays/dev
```

In short:

```text
kubectl kustomize ...  = Generate YAML only
kubectl apply -k ...   = Generate YAML and apply it
```

Use `kubectl kustomize` to inspect or save the generated manifests. Use `kubectl apply -k` when you are ready to send them to the Kubernetes API server. Because this demo sets `namespace: training-dev` and `namespace: training-prod`, the namespaces must exist before applying. The setup command is already included above; it is repeated here to make the comparison complete:

```bash
# Create the namespaces once; do not fail if they already exist.
kubectl create namespace training-dev --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace training-prod --dry-run=client -o yaml | kubectl apply -f -

# Apply the overlays after their namespaces exist.
kubectl apply -k demo/overlays/dev
kubectl apply -k demo/overlays/prod
```

To preview changes without modifying the cluster, use:

```bash
# Show the difference between the rendered overlay and live resources.
kubectl diff -k demo/overlays/dev
```

To render and validate without a live cluster:

```bash
# Render the dev overlay into a temporary YAML file.
kubectl kustomize demo/overlays/dev > /tmp/kustomize-dev.yaml
# Validate the rendered YAML on the client.
kubectl create --dry-run=client -f /tmp/kustomize-dev.yaml -o yaml
```

On Windows PowerShell:

```powershell
# Render the dev overlay into a local file.
kubectl kustomize demo/overlays/dev | Out-File kustomize-dev.yaml
# Validate the rendered file on the client.
kubectl create --dry-run=client -f kustomize-dev.yaml -o yaml
```

The `grep` commands in the examples are Unix-style filtering commands. In PowerShell, use `Select-String` instead:

```powershell
# Show image lines from the rendered dev YAML.
kubectl kustomize demo/overlays/dev | Select-String 'image:'
# Show replica lines from the rendered dev YAML.
kubectl kustomize demo/overlays/dev | Select-String 'replicas:'
```

## 7. Useful commands

```bash
# Build and print one overlay.
kubectl kustomize demo/overlays/dev
# Validate against the API server without persisting changes.
kubectl apply --dry-run=server -k demo/overlays/dev
# List the resources selected by the rendered overlay.
kubectl kustomize demo/overlays/dev | kubectl apply --dry-run=client -f - -o name
# Use the standalone Kustomize binary, if installed.
kustomize build demo/overlays/dev
# View the installed kubectl client version.
kubectl version --client
```

`--dry-run=server` needs a reachable cluster. `--dry-run=client` checks client-side processing but cannot catch every API validation issue.

## 8. Good practices

1. Keep the base deployable and environment-neutral.
2. Put only differences in overlays; avoid copying the base.
3. Pin image tags or digests instead of using `latest`.
4. Keep patches small and named after their purpose.
5. Never commit real passwords, tokens, or private keys. `secretGenerator` creates a Secret manifest but does not encrypt it.
6. Render and review with `kubectl kustomize` or `kubectl diff -k` in CI before applying.
7. Test overlays independently. A valid base does not guarantee that every overlay is valid.
8. Remember that generated ConfigMap and Secret names include a content hash by default.
9. Keep Kustomize and Kubernetes client versions current and document version-sensitive behavior.

## 9. Common problems

### `no matches for OriginalId`

A patch does not identify an existing resource. Check `apiVersion`, `kind`, and the resource `metadata.name` used by the patch.

### A generated ConfigMap has an unexpected name

Generators append a content hash by default. This is useful because a changed ConfigMap can cause a rollout when referenced by a Pod. Use `generatorOptions.disableNameSuffixHash: true` only when you understand the rollout trade-off.

### An image did not change

The `images.name` value must match the image name in the base. Render the overlay and inspect the final `image:` field.

### Namespace is missing

A namespace set in an overlay applies to namespaced resources. Cluster-scoped resources, such as `Namespace` and `ClusterRole`, do not belong to a namespace.

## 10. What to practise next

### 1. Change the dev replica count

Edit `demo/overlays/dev/kustomization.yaml` and change `count` from `1` to `2`:

```bash
# Render the dev overlay and inspect the configured replica count.
kubectl kustomize demo/overlays/dev | grep -A20 'kind: Deployment' | grep 'replicas:'

# Apply the updated dev overlay to the cluster.
kubectl apply -k demo/overlays/dev
# Read the desired replica count from the live Deployment.
kubectl get deployment dev-web -n training-dev -o jsonpath='{.spec.replicas}{" desired replicas\n"}'
```

### 2. Change the prod image and review the diff

Edit `demo/overlays/prod/kustomization.yaml` and change `newTag`, for example from `"1.27"` to `"1.27.1"`:

```bash
# Render the prod overlay and confirm the new image tag.
kubectl kustomize demo/overlays/prod | grep 'image:'

# Preview the changes without applying them.
kubectl diff -k demo/overlays/prod
# Apply the reviewed prod changes.
kubectl apply -k demo/overlays/prod
# Wait until the new prod Pods are ready.
kubectl rollout status deployment/prod-web -n training-prod
```

### 3. Add and override a ConfigMap value

Add this value to `demo/base/app-config.env`:

```text
APP_MESSAGE=hello-from-base
```

Add the environment-specific value under the existing `literals` list in `demo/overlays/dev/kustomization.yaml`:

```yaml
configMapGenerator:
  - name: web-config
    behavior: merge
    literals:
      - APP_ENV=development
      - APP_MESSAGE=hello-from-dev
```

Render and verify that the overlay value wins:

```bash
# Render the dev ConfigMap and confirm the overlay value is present.
kubectl kustomize demo/overlays/dev | grep -A5 'kind: ConfigMap'


# Apply the updated ConfigMap to dev.
kubectl apply -k demo/overlays/dev
# Read APP_MESSAGE from the generated ConfigMap.
kubectl get configmap -n training-dev -o yaml | grep -A2 'APP_MESSAGE'
```

### 4. Add a NetworkPolicy only to prod

Create `demo/overlays/prod/network-policy.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-ingress
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: web
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: training-prod
      ports:
        - protocol: TCP
          port: 80
```

Add the file to the prod `resources` list:

```yaml
resources:
  - ../../base
  - network-policy.yaml
```

Check that only prod contains the policy:

```bash
# Confirm the NetworkPolicy is rendered for prod.
kubectl kustomize demo/overlays/prod | grep -A3 'kind: NetworkPolicy'
# Confirm that dev does not contain the prod-only policy.
kubectl kustomize demo/overlays/dev | grep 'kind: NetworkPolicy' || echo 'No NetworkPolicy in dev'

# Apply the policy to prod.
kubectl apply -k demo/overlays/prod
# List NetworkPolicies installed in prod.
kubectl get networkpolicy -n training-prod
```

The cluster CNI must support NetworkPolicy enforcement; rendering alone does not guarantee enforcement.

### 5. Add an environment variable with a JSON 6902 patch

Create `demo/overlays/dev/add-environment.yaml`:

```yaml
- op: add
  path: /spec/template/spec/containers/0/env
  value:
    - name: FEATURE_FLAG
      value: "true"
```

Add this patch to the dev `patches` list while keeping the existing resource patch:

```yaml
patches:
  - path: resource-patch.yaml
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: web
    path: add-environment.yaml
```

Render and inspect the result:

```bash
# Render the dev overlay and confirm FEATURE_FLAG is present.
kubectl kustomize demo/overlays/dev | grep -A3 'FEATURE_FLAG'
# Render the prod overlay and confirm FEATURE_FLAG is not present.
kubectl kustomize demo/overlays/prod | grep -A3 'FEATURE_FLAG' || echo 'Not present in prod'

# Apply the environment variable to the dev Deployment.
kubectl apply -k demo/overlays/dev
# Read FEATURE_FLAG from the live Deployment.
kubectl get deployment dev-web -n training-dev -o yaml | grep -A2 FEATURE_FLAG
```

### 6. Create a staging overlay

Create the directory and copy the dev resource patch:

```bash
# Create the staging overlay directory.
mkdir -p demo/overlays/staging
# Reuse the dev resource settings as a starting point.
cp demo/overlays/dev/resource-patch.yaml demo/overlays/staging/resource-patch.yaml
```

Create `demo/overlays/staging/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: training-staging
namePrefix: staging-

resources:
  - ../../base

images:
  - name: nginx
    newName: nginx
    newTag: "1.27-alpine"

replicas:
  - name: web
    count: 2

configMapGenerator:
  - name: web-config
    behavior: merge
    literals:
      - APP_ENV=staging

patches:
  - path: resource-patch.yaml
```

Build and apply the new environment:

```bash
# Create the staging namespace; the generated YAML is applied to the cluster.
kubectl create namespace training-staging --dry-run=client -o yaml | kubectl apply -f -
# Render staging without changing the cluster.
kubectl kustomize demo/overlays/staging
# Apply the staging resources.
kubectl apply -k demo/overlays/staging
# Verify the staging resources.
kubectl get all -n training-staging
# Remove staging when the exercise is complete.
kubectl delete -k demo/overlays/staging
```

On Windows PowerShell, use `New-Item -ItemType Directory demo/overlays/staging` and `Copy-Item` instead of `mkdir -p` and `cp`.

### 7. Generate a Secret with a fake value

Add this generator to `demo/overlays/dev/kustomization.yaml`:

```yaml
secretGenerator:
  - name: web-secret
    literals:
      - DEMO_TOKEN=not-a-real-secret
```

Render and inspect it:

```bash
# Render the Secret and note its hash-suffixed name.
kubectl kustomize demo/overlays/dev | grep -A8 'kind: Secret'
# Apply the generated Secret to dev.
kubectl apply -k demo/overlays/dev
# List Secrets so you can copy the generated name.
kubectl get secret -n training-dev
# Decode the demo value after replacing <hash> with the displayed suffix.
kubectl get secret dev-web-secret-<hash> -n training-dev -o jsonpath='{.data.DEMO_TOKEN}' | base64 --decode
```

Replace `<hash>` with the suffix shown by `kubectl get secret`. The value is base64 encoded, not encrypted. Never commit real credentials; use an external solution such as a cloud secret manager, External Secrets Operator, or Sealed Secrets for real workloads.
