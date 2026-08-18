# RBAC 

This explains how Role-Based Access Control (RBAC) works in Kubernetes.

## Quick concept

RBAC in Kubernetes is the mechanism that decides who is allowed to do what inside the cluster.

A simple way to remember it is:

- Subject: who is asking for access (user, ServiceAccount, group)
- Role: what are the allowed actions
- Binding: where that permission is applied

Examples:

- ServiceAccount: identity for workloads or users inside a namespace
- Role: permissions inside a namespace
- RoleBinding: binds a Role to a user or ServiceAccount in the same namespace
- ClusterRole / ClusterRoleBinding: cluster-wide permissions (not added in this demo yet)

### RBAC in Kubernetes

Kubernetes does not allow access by default just because a user exists. Every request goes through an authorization check.

The API server checks:

1. who the user is
2. what resource is being accessed
3. which action is requested
4. whether a matching Role or ClusterRole grants that permission

If a matching rule exists, access is allowed. If not, the request is denied.

This is why RBAC is commonly used to follow the principle of least privilege.

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

Role-based access control helps you follow the principle of least privilege:

- grant only the permissions needed
- keep permissions inside a namespace when possible
- avoid giving broad access by default

## Cluster Level (Coming Soon)

This demo stops at the namespace level for now.

Cluster-level RBAC uses:
- ClusterRole
- ClusterRoleBinding

These are used when access is needed across all namespaces or for cluster-scoped resources such as nodes, persistent volumes, and cluster-wide APIs.

This section will be added later.

## Cleanup

```bash
kubectl delete ns apache
```
