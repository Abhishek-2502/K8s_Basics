# Kubernetes Ingress Controller

We will see how to use Kubernetes Ingress to route incoming HTTP traffic to different services.

## What is Kubernetes Ingress?

Kubernetes Ingress is an API resource that defines rules for routing incoming HTTP and HTTPS traffic to Kubernetes Services.

Instead of exposing every application separately, Ingress allows multiple applications to be accessed through a single entry point.

For example:

```text
<VM_IP>/apache → apache-service
<VM_IP>/nginx  → nginx-service
````

Ingress can route traffic based on:

* URL path
* Hostname
* HTTP/HTTPS configuration

In this project, we will use **path-based routing**.

## What is an Ingress Controller?

An Ingress resource only defines the routing rules. It does not handle the network traffic by itself.

An **Ingress Controller** is the component that watches Ingress resources and actually processes incoming HTTP/HTTPS requests.

The relationship can be understood as:

```text
Ingress Resource
      │
      │ Defines routing rules
      ▼
Ingress Controller
      │
      │ Processes incoming traffic
      ▼
Kubernetes Services
      │
      ▼
Pods
```

For this project, we will use the **NGINX Ingress Controller**.

### Ingress vs Ingress Controller

| Ingress                             | Ingress Controller                   |
| ----------------------------------- | ------------------------------------ |
| Kubernetes API resource             | Running component/controller         |
| Defines routing rules               | Implements the routing rules         |
| Describes where traffic should go   | Actually handles the traffic         |
| Example: `/apache → apache-service` | NGINX processes the incoming request |
| Defined in `ingress.yml`            | Installed separately in the cluster  |

## What We Are Going to Implement

We will create two Deployments and Services for Apache and NGINX.

Using a Kubernetes Ingress resource and the NGINX Ingress Controller, we will route incoming HTTP traffic to the appropriate Service based on the URL path.

The traffic will be routed as follows:

| URL Path  | Service          | Application |
| --------- | ---------------- | ----------- |
| `/apache` | `apache-service` | Apache      |
| `/nginx`  | `nginx-service`  | NGINX       |


### Pre-requisites to implement this project:
- Setup KIND Cluster or Minikube on a virtual machine
- Install Kubectl

## Steps to implement ingress:

**1.** Create one yaml file for apache deployment and service i.e. [apache.yml](apache.yml)

**2.** Create one more yaml file for nginx deployment and service i.e. [nginx.yml](nginx.yml)

**3.** Install Ingress-Controller using [ingress-controller.md](ingress-controller.md)

**4.** Now create an Ingress resource that routes traffic to the Apache and NGINX services based on the URL path i.e. [ingress.yml](ingress.yml)

**5.** Apply the Manifest:
```bash
kubectl apply -f apache.yml
kubectl apply -f nginx.yml
kubectl apply -f ingress.yml
```

**6.** Now, test the routing :

  - curl http://<VM_IP>/apache to access the Apache service.
  - curl http://<VM_IP>/nginx to access the NGINX service.
  
  You can also open it in a browser:
  ```
  http://<VM_IP>/apache
  http://<VM_IP>/nginx
  ```

 ## Architecture 

                           VM
                      <VM_IP>:80
                           │
                           ▼
                 NGINX Ingress Controller
                           │
              ┌────────────┴────────────┐
              │                         │
         /apache                    /nginx
              │                         │
              ▼                         ▼
      apache-service              nginx-service
           :80                         :80
              │                         │
              ▼                         ▼
        Apache Pod                  NGINX Pod


## Ingress Annotations

Annotations in Kubernetes are key-value pairs used to attach additional configuration or metadata to Kubernetes resources.

They are commonly used by Kubernetes controllers and other components to customize how a resource should behave.

Annotations are defined under the `metadata` section of a Kubernetes resource:

```yaml
metadata:
  annotations:
    key: value
````

Different controllers can define and use their own annotations. For example, the NGINX Ingress Controller provides several annotations to customize Ingress behavior.

### Example

In our Ingress configuration, we are using the following NGINX Ingress Controller annotation:

```yaml
metadata:
  name: apache-nginx-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
```

The annotation:

```yaml
nginx.ingress.kubernetes.io/rewrite-target: /
```

tells the NGINX Ingress Controller to rewrite the incoming request path to `/` before forwarding the request to the backend Service.

For example:

```text
http://<VM_IP>/apache
```

The Ingress matches `/apache` and rewrites the path to:

```text
/
```

before forwarding the request to:

```text
apache-service:80
```

Similarly:

```text
http://<VM_IP>/nginx
```

is rewritten to:

```text
/
```

and forwarded to:

```text
nginx-service:80
```

The traffic flow is:

```text
/apache
   │
   │ Ingress matches /apache
   │
   │ rewrite-target: /
   ▼
/
   │
   ▼
apache-service:80
```

And:

```text
/nginx
   │
   │ Ingress matches /nginx
   │
   │ rewrite-target: /
   ▼
/
   │
   ▼
nginx-service:80
```

> **Note:** Annotations are controller-specific. In this example, `nginx.ingress.kubernetes.io/rewrite-target` is an annotation provided by the NGINX Ingress Controller. Other Kubernetes controllers may support different annotations.

## Advantages of Kubernetes Ingress

Kubernetes Ingress provides several advantages when exposing multiple applications or services.

### 1. Single Entry Point

Ingress allows multiple applications to be accessed through a **single external IP address and port**.

Without Ingress:

```text
<VM_IP>:8081 → Apache
<VM_IP>:8082 → NGINX
<VM_IP>:8083 → Application
```

With Ingress:

```text
                    <VM_IP>:80
                         │
                         ▼
               Ingress Controller
                         │
              ┌──────────┼──────────┐
              │          │          │
           /apache    /nginx     /app
              │          │          │
              ▼          ▼          ▼
           Apache      NGINX     Application
```

---

### 2. Path-Based Routing

Ingress can route requests to different Services based on the URL path.

```text
/apache → apache-service
/nginx  → nginx-service
/app    → app-service
```

This makes it possible to expose multiple applications through the same endpoint.

---

### 3. Host-Based Routing

Ingress can also route traffic based on the hostname.

For example:

```text
api.example.com     → api-service
app.example.com     → app-service
admin.example.com   → admin-service
```

This allows multiple applications to use the same external IP address.

---

### 4. TLS/HTTPS Support

Ingress can handle HTTPS traffic and TLS certificates.

```text
Client
  │
  │ HTTPS
  ▼
Ingress Controller
  │
  │ HTTP/HTTPS
  ▼
Kubernetes Service
```

This allows TLS termination to be handled at the Ingress layer instead of configuring certificates individually in every application.

---

### 5. Centralized Traffic Management

Ingress provides a central place to configure HTTP/HTTPS routing rules.

Instead of configuring networking separately for every application, you can manage routing through Ingress resources.

---

### 6. Reduces the Need for Multiple Load Balancers

Without Ingress, you might expose every application using a separate `LoadBalancer` Service.

For example:

```text
LoadBalancer → Apache
LoadBalancer → NGINX
LoadBalancer → Backend API
```

With Ingress:

```text
                 Load Balancer
                      │
                      ▼
              Ingress Controller
                │      │      │
                ▼      ▼      ▼
             Apache  NGINX   API
```

This can reduce infrastructure complexity and, depending on the environment, infrastructure cost.

---

### 7. URL Rewriting

Ingress Controllers can modify request paths using annotations or controller-specific configuration.

For example:

```text
/apache
   │
   ▼
/
```

Current demo uses:

```yaml
nginx.ingress.kubernetes.io/rewrite-target: /
```

---

### 8. Centralized TLS and Routing Configuration

Ingress provides a common layer for handling things such as:

* HTTP/HTTPS routing
* Host-based routing
* Path-based routing
* TLS termination
* URL rewriting
* Controller-specific traffic policies

This keeps application-level configuration simpler.

---

### Summary

The main advantages can be summarized as:

| Advantage                | Purpose                                                |
| ------------------------ | ------------------------------------------------------ |
| **Single Entry Point**   | Expose multiple applications through one endpoint      |
| **Path-Based Routing**   | Route `/api`, `/app`, `/admin`, etc.                   |
| **Host-Based Routing**   | Route different domains to different Services          |
| **HTTPS/TLS**            | Centralize TLS termination                             |
| **Centralized Routing**  | Manage HTTP/HTTPS routing in one place                 |
| **Fewer Load Balancers** | Avoid exposing every Service separately                |
| **URL Rewriting**        | Modify request paths before forwarding                 |
| **Scalability**          | Easily add additional Services behind the same Ingress |

**In short:** Kubernetes Ingress acts as an **HTTP/HTTPS entry point into the cluster**, allowing you to expose and route traffic to multiple Kubernetes Services using a single endpoint.
