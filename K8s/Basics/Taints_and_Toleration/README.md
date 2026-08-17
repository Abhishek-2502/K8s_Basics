# Taints and Tolerations

This example demonstrates how taints and tolerations work in Kubernetes.

## What is a taint?
A taint is applied to a node to prevent pods from scheduling on it unless the pod has a matching toleration.

Example taint:
```yaml
- key: "dedicated"
  value: "backend"
  effect: "NoSchedule"
```

This means:
- the node is reserved for a specific workload type
- only pods with a matching toleration can be scheduled on that node


### 1. Apply the namespace
```bash
kubectl apply -f namespace.yml
```

### 2. Apply the taint to a node
```bash
kubectl taint nodes <node-name> dedicated=backend:NoSchedule
```

Example:
```bash
kubectl taint nodes abhi-kind-cluster-worker dedicated=backend:NoSchedule

kubectl taint nodes abhi-kind-cluster-worker2 dedicated=backend:NoSchedule

kubectl taint nodes abhi-kind-cluster-worker3 dedicated=backend:NoSchedule
```

### 3. Apply the Pod
```bash
kubectl apply -f pod.yml
```

### 4. Verify
```bash
kubectl get pods -n taints-demo
kubectl describe pod -n taints-demo
```
It will be in a pending state as all worker nodes are tainted.

### 5. Remove taint
```bash
kubectl taint nodes <node-name> dedicated=backend:NoSchedule- 
```

Example:
```bash
kubectl taint nodes abhi-kind-cluster-worker dedicated=backend:NoSchedule-
```

### 6. Verify
```bash
kubectl get pods -n taints-demo
```

## What is a toleration?
A toleration allows a pod to schedule on a tainted node.

Example:
```yaml
tolerations:
- key: "dedicated"
  operator: "Equal"
  value: "backend"
  effect: "NoSchedule"
```

### 1. Apply the namespace
```bash
kubectl apply -f namespace.yml
```

### 2. Apply the taint to all nodes if not applied
```bash
kubectl taint nodes abhi-kind-cluster-worker dedicated=backend:NoSchedule

kubectl taint nodes abhi-kind-cluster-worker2 dedicated=backend:NoSchedule

kubectl taint nodes abhi-kind-cluster-worker3 dedicated=backend:NoSchedule
```

### 3. Apply the Pod with Toleration
```bash
kubectl apply -f pod_toleration.yml
```

## 4. Verify
```bash
kubectl get pods -n taints-demo
kubectl describe pod -n taints-demo
```

If the pod has the matching toleration, it will schedule on the tainted node.
If it does not have the toleration, it will remain Pending.


## Why use taints and tolerations?
Taints and tolerations are used to:
- reserve nodes for specific workloads
- separate system workloads from app workloads
- control where certain pods can be scheduled

## Important note about taint-node.yml
`taint-node.yml` is mainly a reference/example file to show how a tainted node looks in YAML.
In real Kubernetes workflows, taints are usually applied directly with the CLI:

```bash
kubectl taint nodes <node-name> dedicated=backend:NoSchedule
```

This is because nodes are cluster objects, and taints are commonly managed using `kubectl` rather than by creating a full node manifest in a normal deployment flow.

## Important behavior to remember
If a pod is already running on a node and you taint that node later, the existing pod will continue to run normally.
The taint affects only scheduling decisions for new pods.

So, to observe the effect of a taint on a pod, you must:
1. delete the pod
2. recreate it
3. then check whether it can schedule on the tainted node

This is because taints do not evict already-running workloads immediately; they prevent new workloads from being scheduled without a matching toleration.

**Note:** Taints are applied to nodes, while tolerations are added to pods. They work together to control scheduling behavior.