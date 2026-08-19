# Kubernetes YAML Explanation - All Key-Value Pairs

This guide explains every key-value pair used in Kubernetes YAML manifests across different resource types.

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
21. [LimitRange](#21-limitrange)
22. [NetworkPolicy](#22-networkpolicy)
23. [ReplicaSet](#23-replicaset)
24. [StorageClass](#24-storageclass)
25. [PodDisruptionBudget (PDB)](#25-poddisruptionbudget-pdb)
26. [PriorityClass](#26-priorityclass)
27. [ValidatingWebhook](#27-validatingwebhook)
28. [MutatingWebhook](#28-mutatingwebhook)

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
    version: v1
  annotations:
    description: "This is a sample pod"
spec:
  restartPolicy: Always
  nodeSelector:
    disktype: ssd
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: database
        topologyKey: kubernetes.io/hostname
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: cache
          topologyKey: kubernetes.io/hostname
  tolerations:
  - key: node-type
    operator: Equal
    value: "worker"
    effect: NoSchedule
  priorityClassName: high-priority
  schedulerName: default-scheduler
  dnsPolicy: ClusterFirst
  hostNetwork: false
  hostPID: false
  imagePullSecrets:
  - name: docker-secret
  serviceAccountName: my-service-account
  automountServiceAccountToken: true
  terminationGracePeriodSeconds: 30
  initContainers:
  - name: init-container
    image: busybox:1.28
    command: ["sh", "-c", "echo initializing"]
  containers:
  - name: my-container
    image: nginx:1.19
    imagePullPolicy: IfNotPresent
    command: ["nginx"]
    args: ["-g", "daemon off;"]
    ports:
    - containerPort: 80
      protocol: TCP
      name: http
    env:
    - name: ENV_VAR
      value: "hello"
    - name: POD_NAME
      valueFrom:
        fieldRef:
          fieldPath: metadata.name
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /
        port: 80
        scheme: HTTP
      initialDelaySeconds: 15
      periodSeconds: 20
      failureThreshold: 3
      timeoutSeconds: 5
      successThreshold: 1
    readinessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
      failureThreshold: 3
      timeoutSeconds: 2
    startupProbe:
      exec:
        command: ["/bin/sh", "-c", "curl -f http://localhost/health || exit 1"]
      failureThreshold: 30
      periodSeconds: 10
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "echo 'Pod started'"]
      preStop:
        exec:
          command: ["/bin/sh", "-c", "echo 'Pod stopping'"]
    securityContext:
      runAsUser: 1000
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: config
      mountPath: /etc/config
      readOnly: true
      subPath: app.conf
      subPathExpr: $(POD_NAMESPACE)
      mountPropagation: None
  securityContext:
    runAsUser: 1000
    fsGroup: 2000
    seLinuxOptions:
      level: "s0:c123,c456"
  volumes:
  - name: config
    configMap:
      name: app-config
      defaultMode: 0644
      items:
      - key: app.conf
        path: application.conf
        mode: 0600
  - name: secrets
    secret:
      secretName: app-secret
      defaultMode: 0400
  - name: cache
    emptyDir: {}
  - name: data
    persistentVolumeClaim:
      claimName: my-pvc
  - name: downward
    downwardAPI:
      items:
      - path: "labels"
        fieldRef:
          fieldPath: metadata.labels

```

### Pod Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for this resource type (Pod uses v1) |
| **kind** | `Pod` | Type of Kubernetes resource |
| **metadata.name** | `my-pod` | Name of the Pod; must be unique within the namespace |
| **metadata.namespace** | `default` | Namespace where the Pod is created; if not specified, uses `default` |
| **metadata.labels** | key-value pairs | Tags to identify and organize resources; used for selecting/filtering |
| **metadata.annotations** | key-value pairs | Additional metadata; not used for selection, mainly for documentation |
| **spec.restartPolicy** | `Always`, `OnFailure`, `Never` | Policy for restarting the container if it exits |
| **spec.nodeSelector** | key-value pairs | Simple node selection based on labels |
| **spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution** | Node selector terms | Pod must be scheduled on nodes matching these terms |
| **spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[].matchExpressions[].key** | `disktype` | Node label key to match |
| **spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[].matchExpressions[].operator** | `In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt` | Label matching operator |
| **spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution.nodeSelectorTerms[].matchExpressions[].values** | `["ssd"]` | Allowed values for the label (not used with Exists/DoesNotExist) |
| **spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution** | Weighted terms | Prefer nodes matching these terms; still schedules if no match |
| **spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[].weight** | `100` | Weight for preference scoring (1-100; higher = stronger preference) |
| **spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution[].preference.matchExpressions** | Match expressions | Node label expressions to prefer |
| **spec.affinity.podAffinity** | Pod affinity rules | Schedule Pod on nodes with other Pods matching labels |
| **spec.affinity.podAntiAffinity** | Pod anti-affinity rules | Schedule Pod on nodes without other Pods matching labels |
| **spec.tolerations[].key** | `node-type` | Taint key that this Pod tolerates |
| **spec.tolerations[].operator** | `Equal`, `Exists` | Comparison operator for taint matching |
| **spec.tolerations[].value** | `"worker"` | Taint value to tolerate |
| **spec.tolerations[].effect** | `NoSchedule`, `NoExecute`, `PreferNoSchedule` | Taint effect to tolerate |
| **spec.priorityClassName** | `high-priority` | PriorityClass name for Pod scheduling priority |
| **spec.schedulerName** | `default-scheduler` | Custom scheduler name; uses default if not specified |
| **spec.dnsPolicy** | `ClusterFirst`, `None`, `Default`, `ClusterFirstWithHostNet` | DNS resolution policy for the Pod |
| **spec.hostNetwork** | `true`, `false` | If true, Pod uses host network namespace |
| **spec.hostPID** | `true`, `false` | If true, Pod uses host PID namespace |
| **spec.imagePullSecrets[].name** | `docker-secret` | Secret containing registry credentials |
| **spec.automountServiceAccountToken** | `true`, `false` | Auto-mount service account token into containers |
| **spec.serviceAccountName** | `my-service-account` | ServiceAccount for RBAC and authentication |
| **spec.terminationGracePeriodSeconds** | `30` | Time to wait for graceful shutdown before force killing |
| **spec.initContainers** | Container array | Init containers run before app containers start |
| **spec.initContainers[].name** | `init-container` | Name of the init container |
| **spec.initContainers[].image** | `busybox:1.28` | Image for init container |
| **spec.initContainers[].command** | `["sh", "-c"]` | Command to override image ENTRYPOINT |
| **spec.initContainers[].args** | Command arguments | Arguments for the command |
| **spec.containers[].name** | `my-container` | Unique name for the container within the Pod |
| **spec.containers[].image** | `nginx:1.19` | Container image to run; format is `image:tag` |
| **spec.containers[].imagePullPolicy** | `IfNotPresent`, `Always`, `Never` | When to pull the image; `IfNotPresent` = use cached image if available |
| **spec.containers[].command** | `["nginx"]` | Overrides container's ENTRYPOINT |
| **spec.containers[].args** | `["-g", "daemon off;"]` | Arguments for the command (overrides CMD) |
| **spec.containers[].ports[].containerPort** | `80` | Port that the container listens on |
| **spec.containers[].ports[].protocol** | `TCP`, `UDP` | Protocol used for the port (default: TCP) |
| **spec.containers[].ports[].name** | `http` | Friendly name for the port |
| **spec.containers[].env[].name** | `ENV_VAR` | Name of the environment variable |
| **spec.containers[].env[].value** | `"hello"` | Static value for the environment variable |
| **spec.containers[].env[].valueFrom** | Source object | Dynamic value from ConfigMap, Secret, or Pod metadata |
| **spec.containers[].env[].valueFrom.fieldRef** | Field reference | Reference to Pod metadata fields (e.g., pod name, namespace) |
| **spec.containers[].env[].valueFrom.fieldRef.fieldPath** | `metadata.name` | Path to the metadata field to reference |
| **spec.containers[].resources.requests.memory** | `"64Mi"` | Minimum memory guaranteed to the container |
| **spec.containers[].resources.requests.cpu** | `"250m"` | Minimum CPU guaranteed to the container (m = millicores) |
| **spec.containers[].resources.limits.memory** | `"128Mi"` | Maximum memory allowed for the container |
| **spec.containers[].resources.limits.cpu** | `"500m"` | Maximum CPU allowed for the container |
| **spec.containers[].livenessProbe.httpGet.path** | `/` | HTTP path to call for liveness check |
| **spec.containers[].livenessProbe.httpGet.port** | `80` | Port to call for liveness check |
| **spec.containers[].livenessProbe.httpGet.scheme** | `HTTP`, `HTTPS` | HTTP or HTTPS scheme for the probe |
| **spec.containers[].livenessProbe.tcpSocket.port** | `8080` | TCP port to check for connectivity |
| **spec.containers[].livenessProbe.exec.command** | Command array | Command to execute for the probe |
| **spec.containers[].livenessProbe.initialDelaySeconds** | `15` | Wait time before first liveness check |
| **spec.containers[].livenessProbe.periodSeconds** | `20` | Time between liveness checks |
| **spec.containers[].livenessProbe.failureThreshold** | `3` | Number of failed checks before killing container |
| **spec.containers[].livenessProbe.successThreshold** | `1` | Number of successful checks needed to mark as alive |
| **spec.containers[].livenessProbe.timeoutSeconds** | `5` | Time limit for each probe request |
| **spec.containers[].readinessProbe** | Probe config | Check if container is ready to receive traffic |
| **spec.containers[].readinessProbe.tcpSocket.port** | `8080` | TCP port for readiness check |
| **spec.containers[].readinessProbe.initialDelaySeconds** | `5` | Wait before first readiness check |
| **spec.containers[].readinessProbe.failureThreshold** | `3` | Failed checks before marking as not ready |
| **spec.containers[].startupProbe** | Probe config | Check if application has started; runs until success or max failures |
| **spec.containers[].startupProbe.exec.command** | Command array | Command to check if startup is complete |
| **spec.containers[].startupProbe.failureThreshold** | `30` | Max failures before giving up on startup |
| **spec.containers[].startupProbe.periodSeconds** | `10` | Time between startup checks |
| **spec.containers[].lifecycle.postStart** | Lifecycle hook | Commands to run after container starts |
| **spec.containers[].lifecycle.preStop** | Lifecycle hook | Commands to run before container stops |
| **spec.containers[].securityContext.runAsUser** | `1000` | UID to run container process as |
| **spec.containers[].securityContext.runAsNonRoot** | `true`, `false` | Container must not run as root |
| **spec.containers[].securityContext.allowPrivilegeEscalation** | `true`, `false` | Allow privilege escalation inside container |
| **spec.containers[].securityContext.capabilities.drop** | `["ALL"]` | Linux capabilities to drop from container |
| **spec.containers[].volumeMounts[].name** | `config` | Name of the volume to mount (must match volume definition) |
| **spec.containers[].volumeMounts[].mountPath** | `/etc/config` | Path in container where volume is mounted |
| **spec.containers[].volumeMounts[].readOnly** | `true`, `false` | If true, volume is read-only inside container |
| **spec.containers[].volumeMounts[].subPath** | `app.conf` | Mounts only a subpath of the volume (specific file/directory) |
| **spec.containers[].volumeMounts[].subPathExpr** | `$(POD_NAMESPACE)` | Dynamic subPath using environment variables |
| **spec.containers[].volumeMounts[].mountPropagation** | `None`, `HostToContainer`, `Bidirectional` | How mount propagates to/from the container |
| **spec.securityContext.runAsUser** | `1000` | UID to run all containers as (can be overridden per container) |
| **spec.securityContext.fsGroup** | `2000` | Special supplemental group for volume ownership |
| **spec.securityContext.seLinuxOptions.level** | `"s0:c123,c456"` | SELinux level label |
| **spec.volumes[].name** | `config` | Name of the volume |
| **spec.volumes[].configMap.name** | `app-config` | Name of the ConfigMap to mount as volume |
| **spec.volumes[].configMap.defaultMode** | `0644` | File permissions (octal format) for ConfigMap files |
| **spec.volumes[].configMap.items[].key** | `app.conf` | ConfigMap key to mount |
| **spec.volumes[].configMap.items[].path** | `application.conf` | File path inside the mounted volume |
| **spec.volumes[].configMap.items[].mode** | `0600` | Specific file permissions for individual keys |
| **spec.volumes[].secret.secretName** | `app-secret` | Name of the Secret to mount as volume |
| **spec.volumes[].secret.defaultMode** | `0400` | File permissions (octal format) for Secret files |
| **spec.volumes[].secret.items[].key** | Secret key name | Which secret keys to mount |
| **spec.volumes[].secret.items[].path** | File path | Where to mount the secret file |
| **spec.volumes[].secret.items[].mode** | `0600` | Specific file permissions for individual secrets |
| **spec.volumes[].emptyDir** | `{}` | Empty directory volume (ephemeral, cleared on Pod deletion) |
| **spec.volumes[].persistentVolumeClaim.claimName** | `my-pvc` | Name of the PersistentVolumeClaim to mount |
| **spec.volumes[].downwardAPI.items[].path** | `"labels"` | File path for downward API data |
| **spec.volumes[].downwardAPI.items[].fieldRef.fieldPath** | `metadata.labels` | Pod metadata field to expose (labels, annotations, name, namespace, etc.) |
| **spec.volumes[].hostPath.path** | `/data` | Host node path to mount (dangerous, use with caution) |
| **spec.volumes[].nfs.server** | `nfs-server.example.com` | NFS server address |
| **spec.volumes[].nfs.path** | `/exports/data` | NFS export path |

---

## 2. Deployment

A Deployment manages replicas of Pods.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
  namespace: default
  labels:
    app: myapp
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
      - name: myapp-container
        image: myapp:1.0
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  progressDeadlineSeconds: 600
  revisionHistoryLimit: 10
```

### Deployment Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version for Deployment |
| **kind** | `Deployment` | Type of resource |
| **metadata.name** | `my-deployment` | Unique name for the Deployment |
| **metadata.namespace** | `default` | Namespace for the Deployment |
| **metadata.labels** | key-value pairs | Labels to identify the Deployment |
| **spec.replicas** | `3` | Number of desired Pod replicas |
| **spec.selector.matchLabels** | key-value pairs | Labels to select Pods managed by this Deployment |
| **spec.template.metadata.labels** | key-value pairs | Labels for Pods created by this Deployment |
| **spec.template.spec** | Pod spec | Pod specification (same as Pod spec above) |
| **spec.strategy.type** | `RollingUpdate`, `Recreate` | How to update Pods (RollingUpdate = gradual replacement) |
| **spec.strategy.rollingUpdate.maxSurge** | `1` | Number of Pods above desired count during update |
| **spec.strategy.rollingUpdate.maxUnavailable** | `0` | Number of Pods that can be unavailable during update |
| **spec.progressDeadlineSeconds** | `600` | Time to wait for deployment to progress before marking as failed |
| **spec.revisionHistoryLimit** | `10` | Number of old ReplicaSets to keep for rollback |

---

## 3. Service

A Service exposes Pods with a stable network endpoint.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: default
  labels:
    app: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  sessionAffinity: None
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

Fields such as `nodePort`, `loadBalancerIP`, and `externalTrafficPolicy` apply to
`NodePort` or `LoadBalancer` Services. `externalName` is used instead of a
selector for an `ExternalName` Service.

### Service Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for Service |
| **kind** | `Service` | Type of resource |
| **metadata.name** | `my-service` | Name of the Service |
| **metadata.namespace** | `default` | Namespace for the Service |
| **metadata.labels** | key-value pairs | Labels for the Service |
| **spec.type** | `ClusterIP`, `NodePort`, `LoadBalancer`, `ExternalName` | Type of Service exposure |
| **spec.selector** | key-value pairs | Labels to select Pods to expose |
| **spec.ports[].name** | `http` | Name of the port mapping |
| **spec.ports[].port** | `80` | Port exposed by the Service |
| **spec.ports[].targetPort** | `8080` | Port on the Pod to forward traffic to |
| **spec.ports[].protocol** | `TCP`, `UDP` | Protocol for the port |
| **spec.ports[].nodePort** | `30080` | Port on each Node (only for NodePort/LoadBalancer) |
| **spec.sessionAffinity** | `None`, `ClientIP` | Session persistence; ClientIP = route same client to same Pod |
| **spec.sessionAffinityConfig.clientIP.timeoutSeconds** | `10800` | Time to remember client IP for session affinity |
| **spec.loadBalancerIP** | `"192.168.1.100"` | Static IP for LoadBalancer Service |
| **spec.clusterIP** | `"10.0.0.10"` | Virtual IP assigned to the Service (auto-assigned if not specified) |
| **spec.clusterIPs** | `["10.0.0.10"]` | List of cluster IPs (for dual-stack) |
| **spec.ipFamilies** | `["IPv4"]`, `["IPv6"]`, `["IPv4", "IPv6"]` | IP family preference (IPv4, IPv6, or both) |
| **spec.externalIPs** | `["203.0.113.10"]` | External IPs to route traffic from (must be manually configured) |
| **spec.externalName** | `api.example.com` | External hostname for ExternalName service type |
| **spec.externalTrafficPolicy** | `Cluster`, `Local` | How external traffic is handled; Local = no forwarding outside local node |

---

## 4. ConfigMap

A ConfigMap stores configuration data as key-value pairs.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
  labels:
    app: myapp
data:
  DATABASE_HOST: "localhost"
  DATABASE_PORT: "5432"
  app.properties: |
    server.port=8080
    server.servlet.context-path=/api
```

### ConfigMap Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for ConfigMap |
| **kind** | `ConfigMap` | Type of resource |
| **metadata.name** | `app-config` | Name of the ConfigMap |
| **metadata.namespace** | `default` | Namespace for the ConfigMap |
| **metadata.labels** | key-value pairs | Labels to organize ConfigMaps |
| **data** | key-value pairs | Configuration data; values are strings (can be multiline with \|) |

---

## 5. Secret

A Secret stores sensitive data like passwords and API keys.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: default
type: Opaque
data:
  username: dXNlcm5hbWU=  # base64 encoded "username"
  password: cGFzc3dvcmQ=  # base64 encoded "password"
stringData:
  api-key: my-secret-key  # automatically base64 encoded
```

### Secret Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for Secret |
| **kind** | `Secret` | Type of resource |
| **metadata.name** | `app-secret` | Name of the Secret |
| **metadata.namespace** | `default` | Namespace for the Secret |
| **type** | `Opaque`, `kubernetes.io/basic-auth`, `kubernetes.io/dockercfg` | Type of Secret data |
| **data** | base64 encoded key-value pairs | Sensitive data (must be base64 encoded) |
| **stringData** | plain text key-value pairs | Sensitive data (automatically base64 encoded by Kubernetes) |

---

## 6. PersistentVolume (PV)

A PersistentVolume is a storage resource in the cluster.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
  labels:
    type: local
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /data
```

### PersistentVolume Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for PersistentVolume |
| **kind** | `PersistentVolume` | Type of resource |
| **metadata.name** | `my-pv` | Name of the PersistentVolume |
| **metadata.labels** | key-value pairs | Labels to organize PVs |
| **spec.capacity.storage** | `10Gi` | Total storage capacity |
| **spec.accessModes** | `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany` | How the volume can be accessed |
| **spec.storageClassName** | `standard` | Storage class for dynamic provisioning |
| **spec.persistentVolumeReclaimPolicy** | `Retain`, `Delete` | What happens to the volume after release (`Recycle` is deprecated) |
| **spec.hostPath.path** | `/data` | Path on the host node (for hostPath volumes) |

---

## 7. PersistentVolumeClaim (PVC)

A PersistentVolumeClaim requests storage from a PersistentVolume.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 5Gi
  selector:
    matchLabels:
      type: local
```

### PersistentVolumeClaim Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for PersistentVolumeClaim |
| **kind** | `PersistentVolumeClaim` | Type of resource |
| **metadata.name** | `my-pvc` | Name of the PersistentVolumeClaim |
| **metadata.namespace** | `default` | Namespace for the PVC |
| **spec.accessModes** | `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany` | Requested access mode |
| **spec.storageClassName** | `standard` | Storage class to use |
| **spec.resources.requests.storage** | `5Gi` | Amount of storage requested |
| **spec.selector.matchLabels** | key-value pairs | Labels to select a specific PV |

---

## 8. StatefulSet

A StatefulSet manages stateful applications with persistent identities.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-statefulset
  namespace: default
spec:
  serviceName: my-service
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
      - name: myapp-container
        image: myapp:1.0
        volumeMounts:
        - name: data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 10Gi
```

### StatefulSet Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version for StatefulSet |
| **kind** | `StatefulSet` | Type of resource |
| **metadata.name** | `my-statefulset` | Name of the StatefulSet |
| **metadata.namespace** | `default` | Namespace for the StatefulSet |
| **spec.serviceName** | `my-service` | Headless Service name for network identity |
| **spec.replicas** | `3` | Number of Pod replicas |
| **spec.selector.matchLabels** | key-value pairs | Labels to select Pods |
| **spec.template** | Pod template | Pod specification (same as Deployment) |
| **spec.volumeClaimTemplates** | PVC template | Template to create PVCs for each Pod |

---

## 9. DaemonSet

A DaemonSet runs a Pod on every node in the cluster.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-daemonset
  namespace: default
spec:
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      nodeSelector:
        disktype: ssd
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Equal
        value: "true"
        effect: NoSchedule
      containers:
      - name: myapp-container
        image: myapp:1.0
```

### DaemonSet Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version for DaemonSet |
| **kind** | `DaemonSet` | Type of resource |
| **metadata.name** | `my-daemonset` | Name of the DaemonSet |
| **metadata.namespace** | `default` | Namespace for the DaemonSet |
| **spec.selector.matchLabels** | key-value pairs | Labels to select Pods |
| **spec.template** | Pod template | Pod specification |
| **spec.template.spec.nodeSelector** | key-value pairs | Node labels to select nodes for Pod placement |
| **spec.template.spec.tolerations[].key** | `node-role.kubernetes.io/master` | Taint key to tolerate |
| **spec.template.spec.tolerations[].operator** | `Equal`, `Exists` | Comparison operator for taint matching |
| **spec.template.spec.tolerations[].value** | `"true"` | Taint value to tolerate |
| **spec.template.spec.tolerations[].effect** | `NoSchedule`, `NoExecute`, `PreferNoSchedule` | Taint effect to tolerate |

---

## 10. Job

A Job runs a Pod to completion.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
  namespace: default
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 3
  ttlSecondsAfterFinished: 3600
  template:
    spec:
      containers:
      - name: job-container
        image: busybox:latest
        command: ["echo", "Hello from Job"]
      restartPolicy: Never
```

### Job Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `batch/v1` | API version for Job |
| **kind** | `Job` | Type of resource |
| **metadata.name** | `my-job` | Name of the Job |
| **metadata.namespace** | `default` | Namespace for the Job |
| **spec.completions** | `1` | Number of times the Pod must complete successfully |
| **spec.parallelism** | `1` | Number of Pods to run in parallel |
| **spec.backoffLimit** | `3` | Number of retries before marking Job as failed |
| **spec.ttlSecondsAfterFinished** | `3600` | Time in seconds to keep Job after completion |
| **spec.template.spec.restartPolicy** | `Never`, `OnFailure` | Restart policy for the Pod |

---

## 11. CronJob

A CronJob runs a Job on a schedule.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: my-cronjob
  namespace: default
spec:
  schedule: "0 2 * * *"
  timezone: UTC
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 10
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: job-container
            image: busybox:latest
            command: ["echo", "Hello from CronJob"]
          restartPolicy: OnFailure
```

### CronJob Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `batch/v1` | API version for CronJob |
| **kind** | `CronJob` | Type of resource |
| **metadata.name** | `my-cronjob` | Name of the CronJob |
| **metadata.namespace** | `default` | Namespace for the CronJob |
| **spec.schedule** | `"0 2 * * *"` | Cron expression for job schedule (minute hour day month dayofweek) |
| **spec.timezone** | `UTC` | Timezone for interpreting the schedule |
| **spec.concurrencyPolicy** | `Allow`, `Forbid`, `Replace` | What to do if Job is still running when next schedule is due |
| **spec.successfulJobsHistoryLimit** | `3` | Number of successful Jobs to keep |
| **spec.failedJobsHistoryLimit** | `1` | Number of failed Jobs to keep |
| **spec.startingDeadlineSeconds** | `10` | Deadline in seconds to start a Job if it misses its schedule |
| **spec.jobTemplate.spec** | Job spec | Job specification |

---

## 12. HorizontalPodAutoscaler (HPA)

An HPA automatically scales Pods based on metrics.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

### HorizontalPodAutoscaler Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `autoscaling/v2` | API version for HPA (v2 for advanced metrics) |
| **kind** | `HorizontalPodAutoscaler` | Type of resource |
| **metadata.name** | `my-hpa` | Name of the HPA |
| **metadata.namespace** | `default` | Namespace for the HPA |
| **spec.scaleTargetRef.apiVersion** | `apps/v1` | API version of target resource |
| **spec.scaleTargetRef.kind** | `Deployment` | Kind of target resource (Deployment, StatefulSet, etc.) |
| **spec.scaleTargetRef.name** | `my-deployment` | Name of target resource to scale |
| **spec.minReplicas** | `1` | Minimum number of replicas |
| **spec.maxReplicas** | `10` | Maximum number of replicas |
| **spec.metrics[].type** | `Resource`, `Pods`, `Object` | Type of metric |
| **spec.metrics[].resource.name** | `cpu`, `memory` | Resource metric name |
| **spec.metrics[].resource.target.type** | `Utilization`, `AverageValue` | Metric type for threshold |
| **spec.metrics[].resource.target.averageUtilization** | `70` | Target CPU/memory utilization percentage |
| **spec.behavior.scaleDown.stabilizationWindowSeconds** | `300` | Time to wait before scaling down again |
| **spec.behavior.scaleDown.policies[].type** | `Percent`, `Pods` | Type of scaling policy |
| **spec.behavior.scaleDown.policies[].value** | `50` | Scale down by this percentage or pod count |
| **spec.behavior.scaleDown.policies[].periodSeconds** | `60` | Policy evaluation period |

---

## 13. Ingress

An Ingress manages external HTTP/HTTPS access to Services.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - example.com
    secretName: example-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /app1
        pathType: Prefix
        backend:
          service:
            name: service-1
            port:
              number: 80
      - path: /app2
        pathType: Exact
        backend:
          service:
            name: service-2
            port:
              number: 8080
```

### Ingress Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `networking.k8s.io/v1` | API version for Ingress |
| **kind** | `Ingress` | Type of resource |
| **metadata.name** | `my-ingress` | Name of the Ingress |
| **metadata.namespace** | `default` | Namespace for the Ingress |
| **metadata.annotations** | key-value pairs | Controller-specific configuration |
| **spec.ingressClassName** | `nginx` | Ingress controller class |
| **spec.tls[].hosts** | Array of hostnames | Hostnames for TLS certificate |
| **spec.tls[].secretName** | `example-tls` | Secret containing TLS certificate |
| **spec.rules[].host** | `example.com` | Hostname to route traffic for |
| **spec.rules[].http.paths[].path** | `/app1` | URL path to match |
| **spec.rules[].http.paths[].pathType** | `Prefix`, `Exact`, `ImplementationSpecific` | Path matching type |
| **spec.rules[].http.paths[].backend.service.name** | `service-1` | Service to forward traffic to |
| **spec.rules[].http.paths[].backend.service.port.number** | `80` | Service port to forward to |

---

## 14. Namespace

A Namespace is a virtual cluster for isolating resources.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace
  labels:
    environment: development
  annotations:
    description: "Development namespace"
```

### Namespace Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for Namespace |
| **kind** | `Namespace` | Type of resource |
| **metadata.name** | `my-namespace` | Name of the Namespace |
| **metadata.labels** | key-value pairs | Labels for organizing namespaces |
| **metadata.annotations** | key-value pairs | Additional metadata and documentation |

---

## 15. Role (RBAC)

A Role defines permissions within a namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
```

### Role Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version for Role |
| **kind** | `Role` | Type of resource |
| **metadata.name** | `pod-reader` | Name of the Role |
| **metadata.namespace** | `default` | Namespace for the Role |
| **rules[].apiGroups** | `[""]`, `["apps"]` | API groups the rule applies to ("" = core API) |
| **rules[].resources** | `["pods"]`, `["deployments"]` | Resources the rule applies to |
| **rules[].verbs** | `["get", "list", "watch"]` | Actions allowed (get, list, create, delete, etc.) |

---

## 16. RoleBinding (RBAC)

A RoleBinding binds a Role to a subject within a namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: default
- kind: User
  name: john@example.com
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### RoleBinding Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version for RoleBinding |
| **kind** | `RoleBinding` | Type of resource |
| **metadata.name** | `read-pods` | Name of the RoleBinding |
| **metadata.namespace** | `default` | Namespace for the RoleBinding |
| **subjects[].kind** | `ServiceAccount`, `User`, `Group` | Type of subject |
| **subjects[].name** | `my-app` | Name of the subject |
| **subjects[].namespace** | `default` | Namespace of the subject (for ServiceAccount) |
| **roleRef.kind** | `Role` | Kind of role to bind |
| **roleRef.name** | `pod-reader` | Name of the role to bind |
| **roleRef.apiGroup** | `rbac.authorization.k8s.io` | API group of the role |

---

## 17. ClusterRole (RBAC)

A ClusterRole defines permissions across the entire cluster.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-custom
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get", "list"]
```

### ClusterRole Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version for ClusterRole |
| **kind** | `ClusterRole` | Type of resource |
| **metadata.name** | `cluster-admin-custom` | Name of the ClusterRole |
| **rules[].apiGroups** | API group list | API groups for the rule |
| **rules[].resources** | Resource list | Resources for the rule |
| **rules[].verbs** | Verb list | Actions allowed (get, list, create, delete, etc.) |

---

## 18. ClusterRoleBinding (RBAC)

A ClusterRoleBinding binds a ClusterRole to a subject cluster-wide.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-binding
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRoleBinding Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `rbac.authorization.k8s.io/v1` | API version for ClusterRoleBinding |
| **kind** | `ClusterRoleBinding` | Type of resource |
| **metadata.name** | `cluster-admin-binding` | Name of the ClusterRoleBinding |
| **subjects[].kind** | Subject type (ServiceAccount, User, Group) | Type of subject |
| **subjects[].name** | Subject name | Name of the subject |
| **subjects[].namespace** | Namespace | Namespace of the subject |
| **roleRef.kind** | `ClusterRole` | Kind of cluster role |
| **roleRef.name** | `cluster-admin` | Name of the cluster role |
| **roleRef.apiGroup** | `rbac.authorization.k8s.io` | API group |

---

## 19. ServiceAccount

A ServiceAccount is an identity for Pods to interact with the API server.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: default
  labels:
    app: myapp
```

### ServiceAccount Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for ServiceAccount |
| **kind** | `ServiceAccount` | Type of resource |
| **metadata.name** | `my-app` | Name of the ServiceAccount |
| **metadata.namespace** | `default` | Namespace for the ServiceAccount |
| **metadata.labels** | key-value pairs | Labels for organization |

---

## 20. ResourceQuota

A ResourceQuota limits total resources in a namespace.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: default
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "100"
    services.nodeports: "10"
  scopes:
    - BestEffort
```

### ResourceQuota Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for ResourceQuota |
| **kind** | `ResourceQuota` | Type of resource |
| **metadata.name** | `compute-quota` | Name of the ResourceQuota |
| **metadata.namespace** | `default` | Namespace for the ResourceQuota |
| **spec.hard.requests.cpu** | `"10"` | Total CPU request limit in namespace |
| **spec.hard.requests.memory** | `"20Gi"` | Total memory request limit in namespace |
| **spec.hard.limits.cpu** | `"20"` | Total CPU limit in namespace |
| **spec.hard.limits.memory** | `"40Gi"` | Total memory limit in namespace |
| **spec.hard.pods** | `"100"` | Maximum number of Pods in namespace |
| **spec.hard.services.nodeports** | `"10"` | Maximum NodePort services in namespace |
| **spec.scopes** | `BestEffort`, `NotBestEffort` | Quality of Service scope for quota |

---

## 21. LimitRange

A LimitRange sets default CPU/memory limits and requests for Pods.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-cpu-limit
  namespace: default
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "2Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
    type: Container
  - max:
      cpu: "4"
      memory: "4Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    type: Pod
```

### LimitRange Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `v1` | API version for LimitRange |
| **kind** | `LimitRange` | Type of resource |
| **metadata.name** | `mem-cpu-limit` | Name of the LimitRange |
| **metadata.namespace** | `default` | Namespace for the LimitRange |
| **spec.limits[].default** | Resource limits | Default limits if not specified |
| **spec.limits[].defaultRequest** | Resource requests | Default requests if not specified |
| **spec.limits[].max** | Maximum resources | Maximum resources allowed |
| **spec.limits[].min** | Minimum resources | Minimum resources required |
| **spec.limits[].type** | `Container`, `Pod` | Resource type this limit applies to |

---

## 22. NetworkPolicy

A NetworkPolicy restricts network traffic to and from Pods.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-traffic
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    - podSelector:
        matchLabels:
          tier: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: database
    ports:
    - protocol: TCP
      port: 5432
```

### NetworkPolicy Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `networking.k8s.io/v1` | API version for NetworkPolicy |
| **kind** | `NetworkPolicy` | Type of resource |
| **metadata.name** | `allow-traffic` | Name of the NetworkPolicy |
| **metadata.namespace** | `default` | Namespace for the NetworkPolicy |
| **spec.podSelector.matchLabels** | key-value pairs | Pods to apply this policy to |
| **spec.policyTypes** | `Ingress`, `Egress` | Types of traffic to control |
| **spec.ingress[].from[].namespaceSelector.matchLabels** | Labels | Namespaces allowed to send traffic |
| **spec.ingress[].from[].podSelector.matchLabels** | Labels | Pods allowed to send traffic |
| **spec.ingress[].ports[].protocol** | `TCP`, `UDP` | Protocol for allowed traffic |
| **spec.ingress[].ports[].port** | Port number | Port for allowed traffic |
| **spec.egress[].to[].podSelector.matchLabels** | Labels | Pods this Pod can send traffic to |
| **spec.egress[].ports[].protocol** | `TCP`, `UDP` | Protocol for outgoing traffic |
| **spec.egress[].ports[].port** | Port number | Port for outgoing traffic |

## 23. ReplicaSet

A ReplicaSet maintains a stable set of replicated Pods. (Deployments manage ReplicaSets)

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
      - name: myapp-container
        image: myapp:1.0
```

### ReplicaSet Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `apps/v1` | API version for ReplicaSet |
| **kind** | `ReplicaSet` | Type of resource |
| **metadata.name** | `my-replicaset` | Name of the ReplicaSet |
| **metadata.namespace** | `default` | Namespace for the ReplicaSet |
| **spec.replicas** | `3` | Number of desired Pod replicas |
| **spec.selector.matchLabels** | key-value pairs | Labels to select Pods managed by this ReplicaSet |
| **spec.template** | Pod template | Pod specification |

---

## 24. StorageClass

A StorageClass describes storage types and provisioning for PersistentVolumes.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

### StorageClass Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `storage.k8s.io/v1` | API version for StorageClass |
| **kind** | `StorageClass` | Type of resource |
| **metadata.name** | `fast-storage` | Name of the StorageClass |
| **provisioner** | `kubernetes.io/aws-ebs`, `kubernetes.io/gce-pd` | Storage provisioner plugin |
| **parameters** | Provider-specific key-value pairs | Parameters for the provisioner (e.g., volume type, iops) |
| **allowVolumeExpansion** | `true`, `false` | Allow PVCs to request more storage |
| **reclaimPolicy** | `Delete`, `Retain` | What happens to PV after PVC deletion |
| **volumeBindingMode** | `Immediate`, `WaitForFirstConsumer` | When to bind PV to PVC |

---

## 25. PodDisruptionBudget (PDB)

A PodDisruptionBudget limits voluntary disruptions to Pods (for safe deployments/upgrades).

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-pdb
  namespace: default
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: myapp
  maxUnavailable: 1
  unhealthyPodEvictionPolicy: AlwaysAllow
```

### PodDisruptionBudget Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `policy/v1` | API version for PodDisruptionBudget |
| **kind** | `PodDisruptionBudget` | Type of resource |
| **metadata.name** | `my-pdb` | Name of the PodDisruptionBudget |
| **metadata.namespace** | `default` | Namespace for the PDB |
| **spec.minAvailable** | `1` | Minimum number of Pods that must remain available |
| **spec.maxUnavailable** | `1` | Maximum number of Pods that can be unavailable |
| **spec.selector.matchLabels** | key-value pairs | Labels to select Pods covered by this PDB |
| **spec.unhealthyPodEvictionPolicy** | `AlwaysAllow`, `IfHealthyBudget` | Policy for evicting unhealthy Pods |

---

## 26. PriorityClass

A PriorityClass defines the relative importance of Pods for scheduling.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority class for critical workloads"
preemptionPolicy: PreemptLowerPriority
```

### PriorityClass Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `scheduling.k8s.io/v1` | API version for PriorityClass |
| **kind** | `PriorityClass` | Type of resource |
| **metadata.name** | `high-priority` | Name of the PriorityClass |
| **value** | `1000` | Priority value (higher = more important; used for scheduling order) |
| **globalDefault** | `true`, `false` | If true, this class is default for Pods without priorityClassName |
| **description** | Description string | Explanation of when to use this priority |
| **preemptionPolicy** | `PreemptLowerPriority`, `Never` | Whether higher priority Pods can evict lower priority ones |

---

## Probe Types Reference

Kubernetes supports three probe types with three handler types each:

### Handler Types

| Handler | Example | Usage |
|---------|---------|-------|
| **httpGet** | `httpGet: { path: /, port: 8080 }` | Call HTTP endpoint; expect 200-399 status |
| **tcpSocket** | `tcpSocket: { port: 5432 }` | Check TCP port is open/listening |
| **exec** | `exec: { command: ["curl", "-f", "http://localhost"] }` | Execute command; expect exit code 0 |
| **grpc** | `grpc: { port: 50051 }` | Call gRPC service; added in Kubernetes 1.24+ |

### Probe Types

| Probe | Purpose | When it Fails |
|-------|---------|---------------|
| **livenessProbe** | Checks if Pod is alive/healthy | Kubernetes restarts the container |
| **readinessProbe** | Checks if Pod is ready for traffic | Kubernetes removes Pod from Service |
| **startupProbe** | Checks if app initialization is complete | Kubernetes restarts the container if it fails max times |

### Example with all three probes:

```yaml
spec:
  containers:
  - name: app
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 15
      periodSeconds: 20
      failureThreshold: 3
    readinessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
      failureThreshold: 2
    startupProbe:
      exec:
        command: ["curl", "-f", "http://localhost:8080/startup"]
      failureThreshold: 30
      periodSeconds: 10
```

---

## Volume Types Reference

Kubernetes supports many volume types for different storage needs:

| Volume Type | Purpose | Persistence | Use Case |
|-------------|---------|-------------|----------|
| **emptyDir** | Temporary storage | No (cleared on Pod deletion) | Caching, temporary files, inter-container communication |
| **configMap** | Config files | Depends on ConfigMap | Application configuration |
| **secret** | Sensitive data | Depends on Secret | Passwords, API keys, certificates |
| **hostPath** | Node filesystem | No (local to node) | Logs, system monitoring ⚠️ (avoid in production) |
| **persistentVolumeClaim** | External storage | Yes (PV survives Pod) | Databases, persistent data, multi-Pod access |
| **nfs** | Network File System | Yes (external NFS server) | Shared storage, multi-node access |
| **downwardAPI** | Pod metadata | No (ephemeral) | Expose Pod info as files (labels, annotations, etc.) |
| **awsElasticBlockStore** | AWS EBS volume | Yes (AWS account) | AWS cloud deployments |
| **gcePersistentDisk** | Google Compute persistent disk | Yes (GCP account) | Google Cloud deployments |
| **azureDisk** | Azure disk | Yes (Azure account) | Microsoft Azure deployments |

### Common Volume Type Examples:

```yaml
volumes:
# Temporary storage
- name: cache
  emptyDir: {}

# Configuration
- name: config
  configMap:
    name: app-config

# Secrets
- name: credentials
  secret:
    secretName: db-credentials

# Persistent storage
- name: data
  persistentVolumeClaim:
    claimName: my-pvc

# NFS (network storage)
- name: shared
  nfs:
    server: nfs.example.com
    path: /exports/data

# Pod metadata
- name: podinfo
  downwardAPI:
    items:
    - path: "name"
      fieldRef:
        fieldPath: metadata.name
    - path: "namespace"
      fieldRef:
        fieldPath: metadata.namespace
    - path: "labels"
      fieldRef:
        fieldPath: metadata.labels
```

---

## Environment Variable Sources Reference

Kubernetes allows environment variables to be populated from multiple sources using `valueFrom`:

| Source | Purpose | Example |
|--------|---------|---------|
| **fieldRef** | Pod metadata fields | `metadata.name`, `metadata.namespace`, `status.podIP` |
| **resourceFieldRef** | Container resource limits/requests | `limits.memory`, `requests.cpu` |
| **configMapKeyRef** | ConfigMap value | Reference a key from a ConfigMap |
| **secretKeyRef** | Secret value | Reference a key from a Secret |

### Examples:

```yaml
spec:
  containers:
  - name: app
    env:
    # Static value
    - name: ENVIRONMENT
      value: "production"
    
    # From Pod metadata
    - name: POD_NAME
      valueFrom:
        fieldRef:
          fieldPath: metadata.name
    
    - name: POD_NAMESPACE
      valueFrom:
        fieldRef:
          fieldPath: metadata.namespace
    
    - name: POD_IP
      valueFrom:
        fieldRef:
          fieldPath: status.podIP
    
    - name: NODE_NAME
      valueFrom:
        fieldRef:
          fieldPath: spec.nodeName
    
    # From container resources
    - name: MEMORY_LIMIT
      valueFrom:
        resourceFieldRef:
          containerName: app
          resource: limits.memory
    
    - name: CPU_REQUEST
      valueFrom:
        resourceFieldRef:
          containerName: app
          resource: requests.cpu
    
    # From ConfigMap
    - name: DB_HOST
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database.host
    
    # From Secret
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
```

---

## 27. ValidatingWebhook

A ValidatingWebhook intercepts API requests and validates them before they're stored in etcd.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: validate-pod
webhooks:
- name: validate.example.com
  clientConfig:
    service:
      name: webhook-service
      namespace: default
      path: "/validate"
    caBundle: LS0tLS1CRUdJTi... # base64 encoded CA certificate
  rules:
  - operations: ["CREATE", "UPDATE"]
    apiGroups: [""]
    apiVersions: ["v1"]
    resources: ["pods"]
  namespaceSelector:
    matchLabels:
      validate: "true"
  failurePolicy: Fail
  sideEffects: None
  admissionReviewVersions: ["v1"]
```

### ValidatingWebhook Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `admissionregistration.k8s.io/v1` | API version for ValidatingWebhook |
| **kind** | `ValidatingWebhookConfiguration` | Type of resource |
| **metadata.name** | `validate-pod` | Name of the webhook configuration |
| **webhooks[].name** | `validate.example.com` | Unique name for this webhook |
| **webhooks[].clientConfig.service.name** | `webhook-service` | Service name hosting the webhook |
| **webhooks[].clientConfig.service.namespace** | `default` | Namespace of the webhook service |
| **webhooks[].clientConfig.service.path** | `/validate` | HTTP path on the service to call |
| **webhooks[].clientConfig.caBundle** | Base64 string | CA certificate to verify the webhook server |
| **webhooks[].rules[].operations** | `["CREATE", "UPDATE", "DELETE"]` | API operations this webhook intercepts |
| **webhooks[].rules[].apiGroups** | `[""]`, `["apps"]` | API groups to watch |
| **webhooks[].rules[].apiVersions** | `["v1"]` | API versions to watch |
| **webhooks[].rules[].resources** | `["pods"]`, `["services"]` | Resource types to watch |
| **webhooks[].namespaceSelector.matchLabels** | key-value pairs | Only watch requests in namespaces with these labels |
| **webhooks[].failurePolicy** | `Fail`, `Ignore` | What to do if webhook fails: reject (Fail) or allow (Ignore) |
| **webhooks[].sideEffects** | `None`, `Some`, `NoneOnDryRun` | Side effects of the webhook |
| **webhooks[].admissionReviewVersions** | `["v1"]` | Supported AdmissionReview API versions |

---

## 28. MutatingWebhook

A MutatingWebhook intercepts API requests and modifies them before they're stored in etcd.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: mutate-pod
webhooks:
- name: mutate.example.com
  clientConfig:
    service:
      name: webhook-service
      namespace: default
      path: "/mutate"
    caBundle: LS0tLS1CRUdJTi... # base64 encoded CA certificate
  rules:
  - operations: ["CREATE"]
    apiGroups: [""]
    apiVersions: ["v1"]
    resources: ["pods"]
  namespaceSelector:
    matchLabels:
      mutate: "true"
  failurePolicy: Fail
  sideEffects: None
  admissionReviewVersions: ["v1"]
  reinvocationPolicy: IfNeeded
```

### MutatingWebhook Key-Value Pair Explanations

| Key | Value | Explanation |
|-----|-------|-------------|
| **apiVersion** | `admissionregistration.k8s.io/v1` | API version for MutatingWebhook |
| **kind** | `MutatingWebhookConfiguration` | Type of resource |
| **metadata.name** | `mutate-pod` | Name of the webhook configuration |
| **webhooks[].name** | `mutate.example.com` | Unique name for this webhook |
| **webhooks[].clientConfig** | Webhook endpoint config | How to reach the webhook server |
| **webhooks[].clientConfig.service** | Service reference | Kubernetes service hosting the webhook |
| **webhooks[].clientConfig.caBundle** | CA certificate | Base64 encoded certificate authority |
| **webhooks[].rules[].operations** | `["CREATE", "UPDATE"]` | Operations this webhook intercepts |
| **webhooks[].rules[].apiGroups** | API group list | API groups to watch |
| **webhooks[].rules[].resources** | Resource list | Resources to watch |
| **webhooks[].namespaceSelector** | Label selector | Namespaces to apply webhook to |
| **webhooks[].failurePolicy** | `Fail`, `Ignore` | Action if webhook fails |
| **webhooks[].sideEffects** | `None`, `Some`, `NoneOnDryRun` | Whether webhook has side effects |
| **webhooks[].reinvocationPolicy** | `Never`, `IfNeeded` | If mutations can cause re-invocation of other webhooks |

---

## Summary of Common Key Patterns

| Pattern | Values | Usage |
|---------|--------|-------|
| **apiVersion** | `v1`, `apps/v1`, `batch/v1`, `networking.k8s.io/v1`, `rbac.authorization.k8s.io/v1` | Identifies API group and version |
| **kind** | Pod, Deployment, Service, ConfigMap, Secret, etc. | Identifies resource type |
| **metadata.name** | Any string | Unique identifier within namespace |
| **metadata.namespace** | Any string (default: "default") | Isolates resources |
| **metadata.labels** | key-value pairs | Used for selecting/filtering resources |
| **metadata.annotations** | key-value pairs | Non-queryable metadata |
| **spec** | Varies | Desired state for the resource |
| **spec.selector.matchLabels** | key-value pairs | Label selector for Pods/resources |
| **status** | Auto-populated | Current state of the resource (read-only) |

---

## Units Reference

| Resource | Units | Examples |
|----------|-------|----------|
| **CPU** | millicores (m) | `100m` = 0.1 CPU, `1000m` = 1 CPU |
| **Memory** | Bytes with suffix | `128Mi` = 128 Mebibytes, `1Gi` = 1 Gibibyte |
| **Storage** | Bytes with suffix | `10Gi`, `500Mi`, `1Ti` |
| **Time** | Seconds | `30s`, `60s`, `3600s` |

---

This guide covers the most common Kubernetes resource types and their key-value pairs. Each key is essential to configuring your Kubernetes resources correctly.
