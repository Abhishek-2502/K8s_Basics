# Kubernetes HPA & VPA Controller (Horizontal/Vertical Pod Autoscaler) on Minikube/KIND Cluster

In this demo, we will see how to deploy HPA and VPA controller. HPA will automatically scale the number of pods based on CPU utilization whereas VPA scales by increasing or decreasing CPU and memory resources within the existing pod containers—thus scaling capacity vertically


## Install Metrics Server on Minikube

1. The Metrics Server enables HPA and VPA.
```bash
minikube addons enable metrics-server
```

2. Check minikube cluster status and nodes :
```bash
minikube status
kubectl get nodes
```

## Install Metrics Server on KIND Cluster

### For HPA
1. Apply Manifest
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

2. Edit the Metrics Server Deployment
```bash
kubectl -n kube-system edit deployment metrics-server
```

3. Add the security bypass to deployment under `container.args`
```bash
- --kubelet-insecure-tls
- --kubelet-preferred-address-types=InternalIP,Hostname,ExternalIP
```

4. Restart the deployment
```bash
kubectl -n kube-system rollout restart deployment metrics-server
```

5. Verify if the metrics server is running
```bash
kubectl get pods -n kube-system
kubectl top nodes
kubectl top pods -n kube-system
```

### For VPA
1. Clone and install script
```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

2. Verify the pods on VPA
```bash
kubectl get pods -n kube-system
```

## What we are going to implement:
In this demo, we will create an deployment & service files for Apache and with the help of HPA, we will automatically scale the number of pods based on CPU utilization.

### Steps to implement HPA:

1. Create [namespace.yml](namespace.yml)

2. We'll include resource requests and limits in yaml. This is required for HPA to monitor CPU usage. Create [deployment.yml](deployment.yml)

3. Create [service.yml](service.yml)

4. Apply the Manifest:
```bash
kubectl apply -f namespace.yml -f deployment.yml -f service.yml
```

5. Verify
```bash
kubectl get all -n apache
kubectl port-forward svc/apache-service -n apache 8081:80 --address 0.0.0.0 
```
Access on browser to see its working or not.

6. Create HPA Resources

We will create HPA resources for Apache deployments. The HPA will scale the number of pods based on CPU utilization. Create [hpa.yml](hpa.yml)

7. Apply the HPA resources:
```bash
kubectl apply -f hpa.yml
```

8. Port forward to access the Apache service on browser.
```bash
kubectl port-forward svc/apache-service -n apache 8081:80 --address 0.0.0.0 &
```

9. Verify HPA
```bash
kubectl get hpa -n apache
```

> This will show you the current state of the HPA, including the current and desired number of replicas.


### Stress Testing

1. To see HPA in action, you can perform a stress test on your deployments. Here is an example of how to generate load on the Apache deployment using 'BusyBox':
```bash
kubectl run -i --tty load-generator --image=busybox -n apache /bin/sh
```

2. Inside the container, use 'wget' to generate load:
```bash
while true; do wget -q -O- http://apache-service.default.svc.cluster.local; done
```

This will generate continuous load on the Apache service, causing the HPA to scale up the number of pods.


3. Now to check if HPA worked or not, open a same new terminal and run the following command
```bash
kubectl get pods -n apache
watch kubectl get hpa -n apache
```

> Note: Wait for few minutes to get the status reflected.

### Steps to implement VPA:

1. Apply the VPA resources:
```bash
kubectl apply -f vpa.yml
```

2. Verify VPA
```bash
kubectl get vpa -n apache
```

### Stress Testing

1. To see VPA in action, you can perform a stress test on your deployments. Here is an example of how to generate load on the Apache deployment using 'BusyBox':
```bash
kubectl run -i --tty load-generator --image=busybox -n apache /bin/sh
```

2. Inside the container, use 'wget' to generate load:
```bash
while true; do wget -q -O- http://apache-service.default.svc.cluster.local; done
```

This will generate continuous load on the Apache service.


3. Now to check if VPA worked or not, open a same new terminal and run the following command
```bash
kubectl get pods -n apache
watch kubectl get vpa -n apache
```

> Note: Wait for few minutes to get the status reflected.

## Other Details
- HPA increase number of Pod
- VPA increase Requests and limits of a Pod
- VPA is generally used in Statefull Application 
- KEDA decide to implement HPA or VPA based on the nature of metrics or events
- Metrics is quantifiable number like cpu usage, ram usage, network usage
