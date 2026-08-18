# RBAC in Kubernetes

Role-Based Access Control (RBAC) is Kubernetes' authorization model for deciding who can do what in the cluster.

It is based on the principle of least privilege: grant only the permissions a subject needs, and nothing more.

## Quick concept

A simple way to remember RBAC is:

- Subject: who is asking for access (user, group, ServiceAccount)
- Role: what actions are allowed
- Binding: where that role is attached

Examples:

- ServiceAccount: identity for workloads or users inside a namespace
- Role: permissions inside a namespace
- RoleBinding: binds a Role to a subject in the same namespace
- ClusterRole: permissions that can apply cluster-wide
- ClusterRoleBinding: binds a ClusterRole to a subject across the cluster

## How RBAC works

When a request reaches the Kubernetes API server, it checks:

1. Who is the caller?
2. Which resource is being accessed?
3. Which action is being performed?
4. Does a matching Role or ClusterRole allow it?

If the answer is yes, access is granted. If not, it is denied.

## Two main RBAC scopes

There are effectively two RBAC scopes in Kubernetes:

### 1. Namespace-scoped RBAC
This is used when permissions should be limited to a single namespace.

Common examples:
- app developers managing only their own namespace
- service accounts used by applications in one namespace

Objects involved:
- Role
- RoleBinding

### 2. Cluster-scoped RBAC
This is used when permissions are required across the entire cluster.

Common examples:
- cluster administrators
- monitoring tools
- dashboard tools
- tools that need to view or manage cluster-wide resources

Objects involved:
- ClusterRole
- ClusterRoleBinding

## Namespace Level

In this example, we will create a namespace, deploy an app, create a Role, and bind it to a ServiceAccount.

### 1. Check the current user

```bash
kubectl auth whoami
kubectl auth can-i get pods
```

This helps you understand what the current user can do before any RBAC binding is added.

### 2. Create the namespace

```bash
kubectl apply -f namespace.yml
kubectl get ns apache
kubectl auth can-i get pods -n apache
```

### 3. Deploy an application

```bash
kubectl apply -f deployment.yml
kubectl get deployment -n apache
```

Check permissions for the current user:

```bash
kubectl auth can-i get deployment -n apache
kubectl auth can-i delete deployment -n apache
```

These checks help show what is allowed before we add Role-based permissions.

### 4. Create a Role

```bash
kubectl apply -f role.yml
kubectl get role -n apache
kubectl describe role apache-manager -n apache
```

The Role is namespace-scoped and allows actions like:
- get
- list
- watch
- create
- update
- delete
- patch

### 5. Create a ServiceAccount

```bash
kubectl apply -f service-account.yml
kubectl get serviceaccount -n apache
```

The ServiceAccount is named `apache-user`.

### 6. Check access without binding

```bash
kubectl auth can-i get pods --as=apache-user -n apache
kubectl auth can-i get deployment --as=apache-user -n apache
kubectl auth can-i delete deployment --as=apache-user -n apache
```

Expected output:

```bash
no
```

This means the ServiceAccount has no permissions yet.

### 7. Bind the Role to the user

```bash
kubectl apply -f role-binding.yml
kubectl get rolebinding -n apache
kubectl describe rolebinding apache-manager-rolebinding -n apache
```

This binding connects the Role to the user `apache-user` inside the `apache` namespace.

### 8. Verify access after binding

```bash
kubectl auth can-i get pods --as=apache-user -n apache
kubectl auth can-i get deployment --as=apache-user -n apache
kubectl auth can-i delete deployment --as=apache-user -n apache
kubectl auth can-i get replicasets --as=apache-user -n apache
```

Expected result:

- `get pods` -> yes
- `get deployment` -> yes
- `delete deployment` -> yes
- `get replicasets` -> no

This proves that access is granted only to the resources and verbs defined in the Role.

## Why this matters

RBAC helps you follow the principle of least privilege:

- grant only the permissions needed
- keep permissions inside a namespace when possible
- avoid giving broad access by default
- reduce accidental or malicious cluster-wide damage

## Cluster Level

Cluster-level RBAC is used when permissions should apply across the whole cluster instead of just one namespace.

This is used for:
- cluster-admin tools
- monitoring systems
- operations utilities
- access to cluster-scoped resources such as nodes and persistent volumes

Unlike a `RoleBinding`, a `ClusterRoleBinding` is not limited to a single namespace.

A `ClusterRole` gives permissions cluster-wide, and a `ClusterRoleBinding` attaches that permission to a subject such as a user, group, or ServiceAccount.

### Example: Kubernetes Dashboard admin access

A common cluster RBAC example is the Kubernetes Dashboard admin setup. It creates a ServiceAccount and binds it to the built-in `cluster-admin` ClusterRole so the dashboard can manage the cluster.

This file is available at `K8s/KIND_Cluster_Install/dashboard-admin-user.yml`.

### What this means

- `admin-user` is created in the `kubernetes-dashboard` namespace
- it is bound to the `cluster-admin` ClusterRole
- `cluster-admin` is a built-in cluster-wide role with broad access
- the binding is cluster-wide, not namespaced

### Verification

```bash
kubectl get sa -n kubernetes-dashboard
kubectl get clusterrolebinding admin-user
kubectl describe clusterrolebinding admin-user
```

This shows that the service account is linked to a cluster-wide admin role.

> This is a good example of cluster-level RBAC because it is not restricted to one namespace.

### Example 2: Monitoring / read-only cluster access

Another common cluster RBAC example is a monitoring tool that needs to read cluster resources but should not change anything.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cluster-reader
  namespace: monitoring
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-only-cluster-role
rules:
- apiGroups: [""]
  resources: ["pods", "nodes", "services", "namespaces"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets", "daemonsets", "statefulsets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-reader-binding
subjects:
- kind: ServiceAccount
  name: cluster-reader
  namespace: monitoring
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: read-only-cluster-role
```

This is cluster-level RBAC because it gives a service account permission to read resources across the cluster without allowing modification.

It is useful for:
- Prometheus
- monitoring dashboards
- observability tools
- read-only auditing or health checks

## Cluster RBAC vs Namespace RBAC

| Scope | Objects | Typical use |
|---|---|---|
| Namespace | Role, RoleBinding | App-level access in one namespace |
| Cluster | ClusterRole, ClusterRoleBinding | Admin, monitoring, cluster-wide tools |

## Best practice

- Prefer `Role` and `RoleBinding` for normal application access.
- Use `ClusterRole` and `ClusterRoleBinding` only when the permission must apply cluster-wide.
- Avoid using `cluster-admin` unless you really need full cluster control.

## Cleanup

```bash
kubectl delete ns apache
```
