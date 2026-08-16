## Deployment VS ReplicaSet VS DaemonSet

We can do rolling update on Deployment but not on ReplicaSet.

DaemonSet ensure every node should have atleast 1 running ReplicaSet.

| Feature             | Deployment                                     | ReplicaSet                                     | DaemonSet                                               |
| ------------------- | ---------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------- |
| **Purpose**         | Manages and updates application Pods           | Ensures a specified number of Pods are running | Ensures a Pod runs on **every eligible node**           |
| **Pod Management**  | Creates/manages ReplicaSets, which manage Pods | Directly manages Pods                          | Directly manages Pods                                   |
| **Scaling**         | Easily scales Pods up/down                     | Scales Pods up/down                            | Automatically runs one Pod per node                     |
| **Rolling Updates** | ✅ Supported                                    | ❌ Not directly                                 | ✅ Supported                                             |
| **Rollback**        | ✅ Supported                                    | ❌ Not directly                                 | ✅ Supported                                             |
| **Typical Use**     | Web apps, APIs, microservices                  | Maintaining a fixed number of Pods             | Node-level services                                     |
| **Example**         | Run 5 replicas of an API                       | Keep 5 API Pods running                        | Run a logging agent on every node                       |
| **Node Dependency** | No                                             | No                                             | Yes                                                     |
| **Pod per Node**    | Not guaranteed                                 | Not guaranteed                                 | Usually **one per eligible node**                       |
| **Common Examples** | Nginx, frontend, backend                       | Backend replica management                     | Fluent Bit, Prometheus Node Exporter, monitoring agents |

### Simple relationship

```text
Deployment
    ↓
ReplicaSet
    ↓
Pods
```

```text
DaemonSet
    ↓
Pod on Node 1
Pod on Node 2
Pod on Node 3
...
```

**Easy way to remember:**

* **Deployment** → *"I want X replicas of my application."*
* **ReplicaSet** → *"Make sure X Pods are always running."*
* **DaemonSet** → *"Run this Pod on every node."*

