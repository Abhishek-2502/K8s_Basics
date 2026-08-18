# Node Affinity 

This README shows how Kubernetes schedules pods to nodes using node affinity.

Node affinity is used when you want a pod to run only on certain nodes based on labels such as:
- region
- node-type
- disktype
- kubernetes.io/hostname

## What we are demonstrating

- required node affinity (deployment-required.yml): pod must schedule only on matching nodes
- preferred node affinity (deployment-preferred.yml): pod prefers matching nodes but can run elsewhere if needed
- mismatch case (deployment-mismatch.yml): pod remains pending when the label does not match

## Required node affinity

### 1. Apply the namespace

```bash
kubectl apply -f namespace.yml
```

### 2. Apply the deployment with required node affinity

```bash
kubectl apply -f deployment-required.yml
```

This deployment requires the pod to run only on nodes with:

```yaml
key: disktype
operator: In
values:
- ssd
```

The pod should schedule only on the labeled node. But no node is labelled for now.

### 3. Check the pod status

```bash
kubectl get pods -n node-affinity-demo
```

It should display status as Pending.


### 4. Label the nodes

Pick one node and give it a label such as `disktype=ssd`.

```bash
kubectl get nodes
kubectl label nodes <node-name> disktype=ssd
kubectl get nodes --show-labels
```

Example:

```bash
kubectl label nodes abhi-kind-cluster-worker disktype=ssd
```

Expected output should include:

```bash
abhi-kind-cluster-worker     disktype=ssd
```

### 5. Check the pod status

```bash
kubectl get pods -n node-affinity-demo
kubectl describe pod -n node-affinity-demo
```

Look for the node name and the scheduled placement.

## Preferred node affinity

Apply the preferred version:

```bash
kubectl apply -f deployment-preferred.yml
```

This pod prefers nodes with `disktype=ssd`, but if none are available it can still run elsewhere.

## A mismatch case

Apply the mismatch deployment:

```bash
kubectl apply -f deployment-mismatch.yml
```

This deployment looks for:

```yaml
key: disktype
operator: In
values:
- hdd
```

Since no node has that label, the pod will remain Pending.

### 1. Verify pending pods

```bash
kubectl get pods -n node-affinity-demo
kubectl describe pod -n node-affinity-demo
```

You should see the pod in a Pending state because the required node match is not satisfied.

## Why use node affinity?

Node affinity is useful when:
- some nodes are faster or have more memory
- specific workloads must stay on SSD-backed nodes
- workloads should run only on GPU nodes or specific regions
- you want better control than plain nodeSelector

## Difference between labels, nodeSelector, and node affinity

### 1. Labels
Labels are key-value metadata attached to objects such as nodes, pods, and deployments.

Example:
```bash
kubectl label nodes <node-name> disktype=ssd
```

Labels are just metadata. They do not by themselves control scheduling.

### 2. nodeSelector
`nodeSelector` is a simple way to schedule a pod only on nodes that match one or more labels.

Example:
```yaml
spec:
  nodeSelector:
    disktype: ssd
```

This is easy to use, but it is limited. It supports only equality checks and is less flexible than node affinity.

### 3. Node Affinity
Node affinity is more powerful than `nodeSelector`.
It supports:
- required vs preferred rules
- `In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt`
- more complex scheduling expressions

Example:
```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: disktype
          operator: In
          values:
          - ssd
```

### Quick comparison

| Feature | Purpose | Complexity |
|---|---|---|
| Labels | Attach metadata to nodes/resources | Simple |
| nodeSelector | Match on exact labels for scheduling | Simple |
| Node Affinity | Advanced scheduling rules with soft/hard matching | Advanced |

### Summary
- Labels are used to identify nodes.
- `nodeSelector` is a basic filtering mechanism.
- Node affinity gives more control and is better for complex scheduling requirements.

## Important difference

- required node affinity: strict matching, pod will not run unless the node matches
- preferred node affinity: soft preference, Kubernetes tries to place on matching nodes but can still schedule elsewhere

## Remove the node label / undo the affinity setup

If you want to remove the scheduling restriction from the node, delete the label:

```bash
kubectl label nodes <node-name> disktype-
```

Example:

```bash
kubectl label nodes abhi-kind-cluster-worker disktype-
```

After removing the label, the node is no longer considered a match for the affinity rule. If the pod is already scheduled, it will keep running until it is recreated or rescheduled.

## Cleanup

```bash
kubectl delete ns node-affinity-demo
```
