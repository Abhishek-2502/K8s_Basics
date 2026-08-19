# CustomResourceDefinition (CRD) and Custom Resource (CR)

Kubernetes has built-in resources such as `Pod`, `Deployment`, and `Service`.
A **CustomResourceDefinition (CRD)** lets you add your own resource type to the
Kubernetes API. A **Custom Resource (CR)** is an object created from that new
type.

This folder uses a `DevOpsBatch` resource as its example.

## CRD vs CR

| Term | Meaning | Example in this folder |
|------|---------|------------------------|
| **CRD** | Defines a new resource type, its API group, versions, scope, and schema | `devops-crd.yml` |
| **CR** | An instance of the resource type defined by a CRD | `devops-cr.yml`, `devops-cr2.yml` |

The relationship is:

```text
CRD: defines the DevOpsBatch type
CR:  creates one DevOpsBatch object
```

Creating a CRD makes Kubernetes understand the new API object. It does not
automatically create Pods, Deployments, or other workloads. A controller or
operator is needed if the custom resource should cause Kubernetes to perform
additional actions.

## API group and version

Built-in resources use API groups such as `apps/v1` for Deployments. Core
resources such as Pods use `v1` and do not have a named API group.

This custom resource uses:

```yaml
apiVersion: trainwithshubham.com/v1
kind: DevOpsBatch
```

- `trainwithshubham.com` is the custom API group.
- `v1` is the version of the custom API.
- `DevOpsBatch` is the kind defined by the CRD.

## CRD used in this folder

| Key | Value | Explanation |
|-----|-------|-------------|
| `apiVersion` | `apiextensions.k8s.io/v1` | API used to define a CRD |
| `kind` | `CustomResourceDefinition` | Declares that this object defines a resource type |
| `metadata.name` | `devopsbatches.trainwithshubham.com` | Must be `<plural>.<group>` |
| `spec.group` | `trainwithshubham.com` | API group for the custom resource |
| `spec.names.plural` | `devopsbatches` | Collection name used by `kubectl get` |
| `spec.names.singular` | `devopsbatch` | Singular resource name |
| `spec.names.kind` | `DevOpsBatch` | Kind used in a CR's `kind` field |
| `spec.names.shortNames` | `junoon`, `batches`, `tws` | Optional aliases for kubectl commands |
| `spec.scope` | `Namespaced` | Each CR belongs to a namespace |
| `spec.versions[].name` | `v1` | Version exposed by the CRD |
| `spec.versions[].served` | `true` | Makes the version available through the API |
| `spec.versions[].storage` | `true` | Stores objects using this version |
| `spec.versions[].schema` | OpenAPI v3 schema | Validates the shape and types of CR fields |

The CRD schema defines these `spec` fields:

| Field | Type | Purpose |
|-------|------|---------|
| `spec.name` | `string` | Name or title of the batch |
| `spec.duration` | `string` | Duration description |
| `spec.platform` | `string` | Platform providing the batch |
| `spec.mode` | `string` | Batch mode, such as Live or Recorded |

## Custom Resources in this folder

`devops-cr.yml` and `devops-cr2.yml` are two instances of the same custom type.

Because the CRD scope is `Namespaced`, these objects are created in the
`default` namespace when no namespace is specified.

## Apply and verify

Run these commands from this folder or provide the file paths explicitly:

```bash
# Register the custom resource type.
kubectl apply -f devops-crd.yml

# Confirm that the CRD exists.
kubectl get crd devopsbatches.trainwithshubham.com
kubectl describe crd devopsbatches.trainwithshubham.com

# Create two DevOpsBatch custom resources.
kubectl apply -f devops-cr.yml
kubectl apply -f devops-cr2.yml

# List the custom resources.
kubectl get devopsbatches
kubectl get devopsbatch
kubectl get junoon

# Inspect one custom resource.
kubectl describe devopsbatch junoon-batch-9
kubectl get devopsbatch junoon-batch-9 -o yaml
```

The plural name, singular name, and short names all refer to the same custom
resource type. For example, `devopsbatches`, `devopsbatch`, and `junoon` can be
used with `kubectl get` after the CRD is installed.

## Useful cleanup commands

Delete the custom resources first, then delete the CRD if it is no longer
needed:

```bash
kubectl delete -f devops-cr.yml
kubectl delete -f devops-cr2.yml
kubectl delete -f devops-crd.yml
```

Deleting a CRD also deletes the custom resources stored under that CRD. Use
the final command carefully.

## Summary

- A **CRD** defines a new type in the Kubernetes API.
- A **CR** is an instance of that type.
- `spec.names` defines the plural, singular, kind, and short names.
- `spec.group` and the version form the CR's `apiVersion`.
- `spec.scope: Namespaced` means each CR belongs to a namespace.
- The schema validates the fields allowed under `spec`.
- A CRD alone stores and serves custom objects; a controller is needed for custom behavior.
