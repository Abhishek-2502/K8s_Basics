# Kubernetes Ingress Controller 

We will see how to use ingress controller to route the traffic on different services.

### Pre-requisites to implement this project:
- Setup KIND Cluster or Minikube on a virtual machine
- Install Kubectl

### What we are going to implement:
We will create two Deployments and Services for Apache and NGINX. Using a Kubernetes Ingress resource, we will route incoming HTTP traffic to the appropriate Service based on the URL path.

The traffic will be routed as follows:

| URL Path | Service | Application |
|----------|---------|-------------|
| `/apache` | `apache-service` | Apache |
| `/nginx` | `nginx-service` | NGINX |

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
  
  You can also open it in a browser:
  ```bash
  http://<VM_IP>/apache
  ```
  - curl http://<VM_IP>/nginx to access the NGINX service.

  You can also open it in a browser:
  ```bash
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
