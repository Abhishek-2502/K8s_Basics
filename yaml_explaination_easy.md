# Kubernetes YAML - Commonly Used Key-Value Pairs

This is a simplified guide covering only the **commonly used** key-value pairs for Kubernetes resources. For advanced/rarely-used options, refer to `yaml_explaination.md`.

---

## Index

1. [Pod](#1-pod)
2. [Deployment](#2-deployment)
3. [Service](#3-service)
4. [ConfigMap](#4-configmap)
5. [Secret](#5-secret)
6. [PersistentVolume (PV)](#6-persistentvolume-pv)
7. [PersistentVolumeClaim (PVC)](#7-persistentvolumeclaim-pvc)
8. [StatefulSet](#8-statefulset)
9. [DaemonSet](#9-daemonset)
10. [Job](#10-job)
11. [CronJob](#11-cronjob)
12. [HorizontalPodAutoscaler (HPA)](#12-horizontalpodautoscaler-hpa)
13. [Ingress](#13-ingress)
14. [Namespace](#14-namespace)
15. [Role (RBAC)](#15-role-rbac)
16. [RoleBinding (RBAC)](#16-rolebinding-rbac)
17. [ClusterRole (RBAC)](#17-clusterrole-rbac)
18. [ClusterRoleBinding (RBAC)](#18-clusterrolebinding-rbac)
19. [ServiceAccount](#19-serviceaccount)
20. [ResourceQuota](#20-resourcequota)
21. [NetworkPolicy](#21-networkpolicy)
22. [ReplicaSet](#22-replicaset)
23. [StorageClass](#23-storageclass)
24. [PriorityClass](#24-priorityclass)
25. [PodDisruptionBudget (PDB)](#25-poddisruptionbudget-pdb)

## 1. Pod

A Pod is the smallest deployable unit in Kubernetes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  namespace: default
  labels:
    app: myapp
spec:
  containers:
  - name: app
    image: nginx:latest
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"
        cpu: "200m"
  nodeSelector:
    disktype: ssd
```

### Commonly Used Pod Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `Pod` | Resource type |
| **metadata.name** | `my-pod` | Pod name |
| **metadata.namespace** | `default` | Namespace |
| **metadata.labels** | `app: myapp` | Labels for identification |
| **spec.containers[].name** | `app` | Container name |
| **spec.containers[].image** | `nginx:latest` | Container image |
| **spec.containers[].ports[].containerPort** | `80` | Port inside container |
| **spec.containers[].resources.requests.memory** | `64Mi`, `512Mi`, `1Gi` | Minimum memory needed |
| **spec.containers[].resources.requests.cpu** | `100m`, `500m`, `1` | Minimum CPU needed |
| **spec.containers[].resources.limits.memory** | `128Mi`, `1Gi` | Maximum memory allowed |
| **spec.containers[].resources.limits.cpu** | `200m`, `1` | Maximum CPU allowed |
| **spec.nodeSelector** | `disktype: ssd` | Run Pod on specific node |

---

## 2. Deployment

Deployment manages replicas of Pods.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

### Commonly Used Deployment Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version |
| **kind** | `Deployment` | Resource type |
| **metadata.name** | `my-app` | Deployment name |
| **metadata.namespace** | `default` | Namespace |
| **spec.replicas** | `3` | Number of Pod copies |
| **spec.selector.matchLabels** | `app: myapp` | Select Pods to manage |
| **spec.template** | Pod spec | Template for Pods |
| **spec.template.metadata.labels** | `app: myapp` | Labels for Pods |
| **spec.template.spec.containers[]** | Container list | Containers inside Pod |

---

## 3. Service

Service exposes Pods with a stable network endpoint.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

### Commonly Used Service Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `Service` | Resource type |
| **metadata.name** | `my-service` | Service name |
| **metadata.namespace** | `default` | Namespace |
| **spec.type** | `ClusterIP`, `NodePort`, `LoadBalancer` | Service type |
| **spec.selector** | `app: myapp` | Select Pods to expose |
| **spec.ports[].port** | `80` | Port exposed by Service |
| **spec.ports[].targetPort** | `8080` | Port on Pod to forward to |
| **spec.ports[].protocol** | `TCP`, `UDP` | Protocol |

---

## 4. ConfigMap

ConfigMap stores configuration as key-value pairs.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  database_url: "postgres://db:5432"
  log_level: "info"
  config.ini: |
    [section]
    key=value
```

### Commonly Used ConfigMap Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `ConfigMap` | Resource type |
| **metadata.name** | `app-config` | ConfigMap name |
| **metadata.namespace** | `default` | Namespace |
| **data** | `key: value` pairs | Configuration data |

---

## 5. Secret

Secret stores sensitive data like passwords.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: default
type: Opaque
data:
  username: dXNlcm5hbWU=
  password: cGFzc3dvcmQ=
stringData:
  config-key: plain-text-value
```

### Commonly Used Secret Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `Secret` | Resource type |
| **metadata.name** | `app-secret` | Secret name |
| **metadata.namespace** | `default` | Namespace |
| **type** | `Opaque`, `kubernetes.io/basic-auth`, `kubernetes.io/dockercfg` | Secret type |
| **data** | Base64 encoded values | Sensitive data; Base64 is encoding, not encryption |
| **stringData** | Plain-text key-value pairs | Kubernetes converts these values to `data` automatically |

---

## 6. PersistentVolume (PV)

PersistentVolume is cluster-level storage.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  hostPath:
    path: /data
```

### Commonly Used PV Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `PersistentVolume` | Resource type |
| **metadata.name** | `my-pv` | PV name |
| **spec.capacity.storage** | `10Gi`, `100Gi` | Storage size |
| **spec.accessModes** | `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany` | Access mode |
| **spec.persistentVolumeReclaimPolicy** | `Retain`, `Delete` | What happens when PVC is deleted (`Recycle` is deprecated) |
| **spec.storageClassName** | `standard`, `fast` | Storage class |
| **spec.hostPath.path** | `/data` | Path on node; mainly for local development, not portable production storage |

---

## 7. PersistentVolumeClaim (PVC)

PVC requests storage from a PV.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
  namespace: default
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### Commonly Used PVC Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `PersistentVolumeClaim` | Resource type |
| **metadata.name** | `my-pvc` | PVC name |
| **metadata.namespace** | `default` | Namespace |
| **spec.accessModes** | `ReadWriteOnce` | Access mode |
| **spec.resources.requests.storage** | `5Gi` | Storage amount needed |
| **spec.storageClassName** | `standard` | Storage class to use |

---

## 8. StatefulSet

StatefulSet manages stateful Pods with stable network identity.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  namespace: default
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        ports:
        - containerPort: 3306
```

### Commonly Used StatefulSet Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version |
| **kind** | `StatefulSet` | Resource type |
| **metadata.name** | `mysql` | StatefulSet name |
| **spec.serviceName** | `mysql` | Headless Service name |
| **spec.replicas** | `3` | Number of replicas |
| **spec.selector.matchLabels** | `app: mysql` | Select Pods |
| **spec.template** | Pod spec | Pod template |

---

## 9. DaemonSet

DaemonSet runs one Pod per node.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: default
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluentd:latest
```

### Commonly Used DaemonSet Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version |
| **kind** | `DaemonSet` | Resource type |
| **metadata.name** | `fluentd` | DaemonSet name |
| **spec.selector.matchLabels** | `app: fluentd` | Select Pods |
| **spec.template** | Pod spec | Pod template |

---

## 10. Job

Job runs a batch task to completion.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: backup-job
  namespace: default
spec:
  backoffLimit: 3
  template:
    spec:
      containers:
      - name: backup
        image: backup-tool:latest
      restartPolicy: Never
```

### Commonly Used Job Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `batch/v1` | API version |
| **kind** | `Job` | Resource type |
| **metadata.name** | `backup-job` | Job name |
| **spec.backoffLimit** | `3` | Max retry attempts |
| **spec.template.spec.containers** | Container list | Containers |
| **spec.template.spec.restartPolicy** | `Never`, `OnFailure` | Restart policy |

---

## 11. CronJob

CronJob runs Jobs on a schedule.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-backup
  namespace: default
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:latest
          restartPolicy: OnFailure
```

### Commonly Used CronJob Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `batch/v1` | API version |
| **kind** | `CronJob` | Resource type |
| **metadata.name** | `daily-backup` | CronJob name |
| **spec.schedule** | `"0 2 * * *"` | Cron expression |
| **spec.jobTemplate.spec.template** | Job Pod spec | Job template |

---

## 12. HorizontalPodAutoscaler (HPA)

HPA automatically scales Pods based on CPU/memory.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Commonly Used HPA Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `autoscaling/v2` | API version |
| **kind** | `HorizontalPodAutoscaler` | Resource type |
| **metadata.name** | `app-hpa` | HPA name |
| **spec.scaleTargetRef.kind** | `Deployment`, `StatefulSet` | Target resource |
| **spec.scaleTargetRef.name** | `my-app` | Target resource name |
| **spec.minReplicas** | `2` | Minimum Pods |
| **spec.maxReplicas** | `10` | Maximum Pods |
| **spec.metrics[].resource.name** | `cpu`, `memory` | Metric to scale on |
| **spec.metrics[].resource.target.averageUtilization** | `70` | Threshold percentage |

---

## 13. Ingress

Ingress exposes HTTP/HTTPS routes to services.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: default
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

### Commonly Used Ingress Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `networking.k8s.io/v1` | API version |
| **kind** | `Ingress` | Resource type |
| **metadata.name** | `my-ingress` | Ingress name |
| **spec.rules[].host** | `example.com` | Domain name |
| **spec.rules[].http.paths[].path** | `/` | URL path |
| **spec.rules[].http.paths[].pathType** | `Prefix`, `Exact` | Path matching type |
| **spec.rules[].http.paths[].backend.service.name** | `my-service` | Service to route to |
| **spec.rules[].http.paths[].backend.service.port.number** | `80` | Service port |

---

## 14. Namespace

Namespace is a virtual cluster.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
  labels:
    environment: development
```

### Commonly Used Namespace Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `Namespace` | Resource type |
| **metadata.name** | `dev` | Namespace name |
| **metadata.labels** | `environment: development` | Labels |

---

## 15. Role (RBAC)

Role defines permissions within a namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

### Commonly Used Role Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version |
| **kind** | `Role` | Resource type |
| **metadata.name** | `pod-reader` | Role name |
| **metadata.namespace** | `default` | Namespace |
| **rules[].apiGroups** | `[""]`, `["apps"]` | API groups |
| **rules[].resources** | `["pods"]`, `["services"]` | Resources |
| **rules[].verbs** | `["get", "list", "create"]` | Allowed actions |

---

## 16. RoleBinding (RBAC)

RoleBinding connects a Role to a subject.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-reader
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
```

### Commonly Used RoleBinding Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version |
| **kind** | `RoleBinding` | Resource type |
| **metadata.name** | `read-pods` | RoleBinding name |
| **metadata.namespace** | `default` | Namespace |
| **roleRef.kind** | `Role`, `ClusterRole` | Role type |
| **roleRef.name** | `pod-reader` | Role name |
| **subjects[].kind** | `ServiceAccount`, `User`, `Group` | Subject type |
| **subjects[].name** | `default` | Subject name |
| **subjects[].namespace** | `default` | Subject namespace |

---

## 17. ClusterRole (RBAC)

ClusterRole defines permissions across the cluster.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]
```

### Commonly Used ClusterRole Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version |
| **kind** | `ClusterRole` | Resource type |
| **metadata.name** | `node-reader` | ClusterRole name |
| **rules[].apiGroups** | API groups | Which API groups |
| **rules[].resources** | Resources | Which resources |
| **rules[].verbs** | Allowed actions | Which actions |

---

## 18. ClusterRoleBinding (RBAC)

ClusterRoleBinding connects a ClusterRole to a subject cluster-wide.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

### Commonly Used ClusterRoleBinding Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version |
| **kind** | `ClusterRoleBinding` | Resource type |
| **metadata.name** | `admin-user` | ClusterRoleBinding name |
| **roleRef.kind** | `ClusterRole` | Role type |
| **roleRef.name** | `cluster-admin` | ClusterRole name |
| **subjects[].kind** | Subject type | ServiceAccount, User, Group |
| **subjects[].name** | Subject name | Account/user name |
| **subjects[].namespace** | Namespace | Namespace of subject |

---

## 19. ServiceAccount

ServiceAccount is an identity for Pods.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: default
```

### Commonly Used ServiceAccount Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `ServiceAccount` | Resource type |
| **metadata.name** | `my-app` | ServiceAccount name |
| **metadata.namespace** | `default` | Namespace |

---

## 20. ResourceQuota

ResourceQuota limits resource usage per namespace.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: default
spec:
  hard:
    pods: "10"
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
```

### Commonly Used ResourceQuota Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version |
| **kind** | `ResourceQuota` | Resource type |
| **metadata.name** | `compute-quota` | ResourceQuota name |
| **metadata.namespace** | `default` | Namespace |
| **spec.hard.pods** | `"10"` | Max pods |
| **spec.hard.requests.cpu** | `"10"` | Total CPU requests |
| **spec.hard.requests.memory** | `"20Gi"` | Total memory requests |
| **spec.hard.limits.cpu** | `"20"` | Total CPU limits |
| **spec.hard.limits.memory** | `"40Gi"` | Total memory limits |

---

## 21. NetworkPolicy

NetworkPolicy controls traffic flow between Pods.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Commonly Used NetworkPolicy Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `networking.k8s.io/v1` | API version |
| **kind** | `NetworkPolicy` | Resource type |
| **metadata.name** | `deny-all` | NetworkPolicy name |
| **metadata.namespace** | `default` | Namespace |
| **spec.podSelector** | Label selector | Which Pods this policy applies to |
| **spec.policyTypes** | `Ingress`, `Egress` | Policy direction |
| **spec.ingress[].from** | Selectors | Allowed incoming traffic |
| **spec.egress[].to** | Selectors | Allowed outgoing traffic |

---

## 22. ReplicaSet

ReplicaSet maintains a set of identical Pod replicas.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: nginx:latest
```

### Commonly Used ReplicaSet Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version |
| **kind** | `ReplicaSet` | Resource type |
| **metadata.name** | `my-replicaset` | ReplicaSet name |
| **spec.replicas** | `3` | Number of replicas |
| **spec.selector.matchLabels** | Label selector | Select Pods |
| **spec.template** | Pod spec | Pod template |

---

## 23. StorageClass

StorageClass defines how PVs are provisioned.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  iops: "3000"
```

### Commonly Used StorageClass Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `storage.k8s.io/v1` | API version |
| **kind** | `StorageClass` | Resource type |
| **metadata.name** | `fast` | StorageClass name |
| **provisioner** | `kubernetes.io/aws-ebs`, `pd.csi.storage.gke.io` | Storage provisioner |
| **parameters** | Key-value pairs | Provisioner options |

---

## 24. PriorityClass

PriorityClass sets pod priority for scheduling.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority for critical apps"
```

### Commonly Used PriorityClass Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `scheduling.k8s.io/v1` | API version |
| **kind** | `PriorityClass` | Resource type |
| **metadata.name** | `high-priority` | PriorityClass name |
| **value** | `1000` | Priority value |
| **globalDefault** | `true`, `false` | Use as default priority |
| **description** | String | Description |

---

## 25. PodDisruptionBudget (PDB)

PodDisruptionBudget ensures minimum Pod availability.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: pdb-app
  namespace: default
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

### Commonly Used PDB Key-Value Pairs

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `policy/v1` | API version |
| **kind** | `PodDisruptionBudget` | Resource type |
| **metadata.name** | `pdb-app` | PDB name |
| **metadata.namespace** | `default` | Namespace |
| **spec.minAvailable** | `2`, `"50%"` | Min Pods that must stay up |
| **spec.maxUnavailable** | `1`, `"10%"` | Max Pods that can be down |
| **spec.selector.matchLabels** | Label selector | Select Pods |

---

## Common Resource Units

| Unit | Meaning | Example |
|------|---------|---------|
| **m** | millicores (CPU) | `500m` = 0.5 CPU |
| **Gi** | Gibibyte | `1Gi` = 1024 Mi |
| **Mi** | Mebibyte | `512Mi` |
| **Ki** | Kibibyte | `1024Ki` |
| **G** | Gigabyte | `1G` ≈ 0.93 Gi |

---

## Quick Reference Summary

| Resource | Purpose | Common Use |
|----------|---------|------------|
| **Pod** | Single container(s) | Debug, testing |
| **Deployment** | Stateless app replicas | Web servers, APIs |
| **StatefulSet** | Stateful app replicas | Databases, caches |
| **DaemonSet** | One Pod per node | Monitoring, logging |
| **Job** | Run once, complete | Backup, processing |
| **CronJob** | Schedule jobs | Daily backups, cleanup |
| **Service** | Network endpoint | Expose Pods |
| **Ingress** | HTTP routing | Domain routing |
| **ConfigMap** | Configuration | App config |
| **Secret** | Passwords/tokens | Credentials |
| **PV/PVC** | Storage | Persistent data |
| **Namespace** | Virtual cluster | Multi-tenancy |
| **RBAC** | Access control | User permissions |
| **HPA** | Auto-scaling | Handle load |
| **NetworkPolicy** | Network security | Firewall rules |
| **ResourceQuota** | Limit usage | Budget control |
| **PriorityClass** | Pod priority | Critical apps |
| **PDB** | Availability | SLA guarantee |
