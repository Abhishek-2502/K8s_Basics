# Kubernetes HPA & VPA Controller (Horizontal/Vertical Pod Autoscaler) on Minikube/KIND Cluster

In this demo, we will see how to deploy HPA and VPA controllers.
- HPA automatically scales the number of pods based on CPU utilization.
- VPA adjusts CPU and memory requests/limits vertically within the existing pod containers.

Also we will create a deployment and a service for Apache. With HPA, the number of pods will scale automatically based on CPU utilization.

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
kubectl top nodes
kubectl top pods -n kube-system
```
Metrics should be visible


### Steps to implement HPA

1. Apply the manifests:
```bash
kubectl apply -f namespace.yml -f deployment.yml -f service.yml
```

2. Verify:
```bash
kubectl get all -n apache
kubectl port-forward svc/apache-service -n apache 8081:80 --address 0.0.0.0
```
Access the app in the browser to confirm it is working.

3. Apply the HPA manifest:
```bash
kubectl apply -f hpa.yml
```

4. Port-forward the service:
```bash
kubectl port-forward svc/apache-service -n apache 8081:80 --address 0.0.0.0 &
```

5. Verify HPA status:
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

Type `exit` when you want to leave the shell. 

This creates continuous load on the Apache service and causes HPA to scale the pods.

3. Check the result in a new terminal:
```bash
kubectl get pods -n apache
watch kubectl get hpa -n apache
```

> Wait a few minutes for the status to reflect.

## Install Vertical Pod Autoscaler (VPA)

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

### Steps to implement VPA

1. Apply the manifests:
```bash
kubectl apply -f namespace.yml -f deployment.yml -f service.yml
```

2. Apply the VPA manifest:
```bash
kubectl apply -f vpa.yml
```

3. Verify VPA status:
```bash
kubectl get vpa -n apache
```

### Stress Testing for VPA

1. Delete the load generator if it already exists:
```bash
kubectl delete pod -n apache load-generator
```

2. Run a busybox pod to generate traffic:
```bash
kubectl run -i --tty load-generator --image=busybox -n apache /bin/sh
```

3. Inside the container, generate load:
```bash
while true; do wget -q -O- http://apache-service.apache.svc.cluster.local; done
```

Type `exit` when you want to leave the shell.

This creates continuous load on the Apache service so VPA can recommend or apply changes to resource requests and limits.

> If `RecommendationProvided` is still not true, keep the load running a bit longer and check again after a few minutes. VPA needs enough usage history to produce a recommendation.

4. Check the result in a new terminal:
```bash
kubectl get pods -n apache
watch kubectl get vpa -n apache
```

> Wait a few minutes for the status to reflect.

#### How to verify VPA worked

Unlike HPA, VPA does not usually create new pods. It adjusts the CPU and memory requests/limits of the existing pod or recommends a new size.

#### Check the VPA recommendation
```bash
kubectl get vpa -n apache -o yaml
```

Look for:
```yaml
status:
  conditions:
  - type: RecommendationProvided
    status: "True"
  recommendation:
    containerRecommendations:
    - containerName: apache
      target:
        cpu: 49m
        memory: 250Mi
```

This means VPA has successfully analyzed the pod and produced a recommendation.

#### Check the pod resource values
```bash
kubectl describe pod -n apache
```

Look under the container section for:
```bash
Requests:
  cpu: 50m
  memory: 64Mi
Limits:
  cpu: 100m
  memory: 128Mi
```

If VPA has applied the recommendation, these values may change after a restart or pod recreation. If the values are still unchanged, it means the VPA recommendation is available but not yet applied to the running pod.

#### Important point
VPA focuses on resource sizing, not on scaling out the replica count. So, for VPA, we verify using:
- `kubectl get vpa -n apache -o yaml`
- `kubectl describe pod -n apache`
- pod `Requests` and `Limits` inside the container section

## Cleanup
```bash
kubectl delete ns apache
```

## Other Details
- HPA increases the number of pods.
- VPA adjusts CPU and memory requests/limits of a pod.
- VPA is often useful for workloads that need resource tuning over time, but it is not limited only to stateful applications.
- KEDA is an event-driven autoscaler and is usually used for custom metrics or event-based scaling; it is separate from VPA.
- Metrics are quantifiable numbers such as CPU usage, memory usage, and network usage.

