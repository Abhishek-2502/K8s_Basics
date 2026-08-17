## StatefulSets

1. Apply Manifest
```bash
kubectl apply -f namespace.yml -f resource-quota.yml -f service.yml -f statefulset.yml 
```

2. Verify
```bash
kubectl get pods -n mysql
```
It should display name like mysql-statefulset-0, mysql-statefulset-1,...

3. Get Inside Pod to see Database `Devops` created or not
```bash
kubectl exec -it mysql-statefulset-0 -n mysql -- bash
mysql -u root -p
show databases;
exit
exit
```
Password: root

4. Delete a Pod to verify it is mainting state or not
```bash
kubectl delete pod mysql-statefulset-0 -n mysql
kubectl get pods -n mysql
```
>**Note:** StatefulSets have headless service (clusterIP: None in service.yml) that means it is not a external service and cannot be accessed be external world.


## Resource Requests and Limits

In the StatefulSet, each MySQL container has resource requests and limits defined:

```yaml
resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 500m
    memory: 1Gi
```

### What does this mean?
- `requests`: The minimum amount of CPU and memory Kubernetes guarantees for the container.
- `limits`: The maximum amount of CPU and memory the container is allowed to use.

Example:
- CPU request: `250m` = 0.25 CPU core
- CPU limit: `500m` = 0.5 CPU core
- Memory request: `512Mi`
- Memory limit: `1Gi`

These values help the scheduler place pods efficiently and prevent a single pod from consuming too many cluster resources.

## ResourceQuota

A `ResourceQuota` is used at the namespace level to limit the total CPU, memory, storage, and other resources used by all workloads in that namespace.

Example:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: mysql-quota
  namespace: mysql
spec:
  hard:
    requests.cpu: "2"
    requests.memory: "2Gi"
    limits.cpu: "4"
    limits.memory: "4Gi"
```

This ensures that the MySQL namespace cannot exceed the configured limits even if multiple workloads are running there.

