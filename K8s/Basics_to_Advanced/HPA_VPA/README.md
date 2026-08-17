# Kubernetes HPA & VPA Controller (Horizontal/Vertical Pod Autoscaler) on Minikube/KIND Cluster

In this demo, we will see how to deploy HPA and VPA controllers.
- HPA automatically scales the number of pods based on CPU utilization.
- VPA adjusts CPU and memory requests/limits vertically within the existing pod containers.

## Install Metrics Server on Minikube

1. The Metrics Server enables HPA and provides resource metrics.
```bash
minikube addons enable metrics-server
```

2. Check the Minikube cluster status and nodes:
```bash
minikube status
kubectl get nodes
```

## Install Metrics Server on KIND Cluster

### For HPA
1. Apply the Metrics Server manifest:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

2. Edit the Metrics Server deployment:
```bash
kubectl -n kube-system edit deployment metrics-server
```

3. Add the security bypass under `container.args`:
```bash
- --kubelet-insecure-tls
- --kubelet-preferred-address-types=InternalIP,Hostname,ExternalIP
```

4. Restart the deployment:
```bash
kubectl -n kube-system rollout restart deployment metrics-server
```

5. Verify the metrics server is running:
```bash
kubectl get pods -n kube-system
kubectl top nodes
kubectl top pods -n kube-system
```

### For VPA
1. Clone and install the Vertical Pod Autoscaler:
```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

2. Verify the VPA components:
```bash
kubectl get pods -n kube-system
```

## What we are going to implement
In this demo, we will create a deployment and a service for Apache. With HPA, the number of pods will scale automatically based on CPU utilization.

### Steps to implement HPA

1. Create [namespace.yml](namespace.yml)

2. Add resource requests and limits in [deployment.yml](deployment.yml). This is required for HPA to monitor CPU usage.

3. Create [service.yml](service.yml)

4. Apply the manifests:
```bash
kubectl apply -f namespace.yml -f deployment.yml -f service.yml
```

5. Verify:
```bash
kubectl get all -n apache
kubectl port-forward svc/apache-service -n apache 8081:80 --address 0.0.0.0
```
Access the app in the browser to confirm it is working.

6. Create the HPA resource

We will create an HPA for the Apache deployment. The HPA will scale the number of pods based on CPU utilization. Create [hpa.yml](hpa.yml).

7. Apply the HPA manifest:
```bash
kubectl apply -f hpa.yml
```

8. Port-forward the service:
```bash
kubectl port-forward svc/apache-service -n apache 8081:80 --address 0.0.0.0 &
```

9. Verify HPA status:
```bash
kubectl get hpa -n apache
```

> This shows the current and desired replica counts.

### Stress Testing for HPA

1. Run a busybox pod to generate traffic:
```bash
kubectl run -i --tty load-generator --image=busybox -n apache /bin/sh
```

2. Inside the container, generate load:
```bash
while true; do wget -q -O- http://apache-service.apache.svc.cluster.local; done
```

This creates continuous load on the Apache service and causes HPA to scale the pods.

3. Check the result in a new terminal:
```bash
kubectl get pods -n apache
watch kubectl get hpa -n apache
```

> Wait a few minutes for the status to reflect.

### Steps to implement VPA

1. Apply the VPA manifest:
```bash
kubectl apply -f vpa.yml
```

2. Verify VPA status:
```bash
kubectl get vpa -n apache
```

### Stress Testing for VPA

1. Run a busybox pod to generate traffic:
```bash
kubectl run -i --tty load-generator --image=busybox -n apache /bin/sh
```

2. Inside the container, generate load:
```bash
while true; do wget -q -O- http://apache-service.apache.svc.cluster.local; done
```

This creates continuous load on the Apache service so VPA can recommend or apply changes to resource requests and limits.

3. Check the result in a new terminal:
```bash
kubectl get pods -n apache
watch kubectl get vpa -n apache
```

> Wait a few minutes for the status to reflect.

## Other Details
- HPA increases the number of pods.
- VPA adjusts CPU and memory requests/limits of a pod.
- VPA is often useful for workloads that need resource tuning over time, but it is not limited only to stateful applications.
- KEDA is an event-driven autoscaler and is usually used for custom metrics or event-based scaling; it is separate from VPA.
- Metrics are quantifiable numbers such as CPU usage, memory usage, and network usage.

