# Kubernetes Ingress Controller 

In this readme, we will see how to use ingress controller to route the traffic on different services.

### Pre-requisites to implement this project:
- Setup KIND Cluster or Minikube on a virtual machine


### What we are going to implement:
- We will create 2 deployment and services i.e nginx and apache and with the help of ingress, we will route the traffic between the services


## Steps to implement ingress:

1. Create one yaml file for apache deployment and service i.e. apache.yml.

2. Create one more yaml file for nginx deployment and service i.e. nginx.yml.

3. Enable the Ingress Controller if using Minikube:
```bash
minikube addons enable ingress
```

4. Now create an Ingress resource that routes traffic to the Apache and NGINX services based on the URL path i.e.ingress.yml.

5. Apply the Manifest:
```bash
kubectl apply -f apache.yml
kubectl apply -f nginx.yml
kubectl apply -f ingress.yml
```

6. To test the Ingress, map the hostname to the Minikube IP in your <b>etc/hosts</b> file :
```bash
echo "$(minikube ip) tws.com" | sudo tee -a /etc/hosts
```
<center>OR</center>

Open <b>/etc/hosts</b> file and add your minikube ip and domain name at the last.

7. Now, test the routing :

  - curl http://tws.com/apache to access the Apache service.
  ```bash
  curl http://tws.com/apache
  ```
  - curl http://tws.com/nginx to access the NGINX service.
  ```bash
  curl http://tws.com/nginx
  ```

<center>OR</center>

- port forward to access the Apache service on browser.
  ```bash
  kubectl port-forward svc/apache-service 8081:80 --address 0.0.0.0 &
  ```
- port forward to access the NGINX service on browser.
  ```bash
  kubectl port-forward svc/nginx-service 8082:80 --address 0.0.0.0 &
  ```
