# Installation (Windows)
Install Minikube using the provided [file](Windows_Installation.md)

# Installation (Linux)
Install Minikube using the provided [file](Linux_Installation.md)

# Docker
### Build: 
```
docker build -t social-media:latest .
```

# DockerHub
```
docker tag social-media:latest abhi25022004/social-media:latest
```
```
docker push abhi25022004/social-media:latest
```

# MINIKUBE Commands

### Start
```
minikube start
```
```
minikube start --driver=docker --no-vtx-check
```
```
minikube start --driver=virtualbox
```
```
minikube start --no-vtx-check
```

### Other Basics
```
minikube version
```
```
minikube ip
```
```
minikube dashboard
```
```
minikube status
```
```
minikube delete
```
```
minikube delete --all
```
```
minikube delete --all --purge
```
```
minikube pause
```
```
minikube unpause
```
```
minikube stop
```
```
minikube tunnel
```

### Metrics Service
```
minikube addons enable metrics-server
kubectl get deployment metrics-server -n kube-system
```

### To make docker the default driver:
```
minikube config set driver docker
```

### Get Pods
```
kubectl get pods -A
```
```
kubectl get pods
```

### Delete Pod
```
kubectl delete pod pod_name
```

### Get logs
```
kubectl logs pod_name
```

### Get Pods info
```
kubectl describe pods
```




## Pod.yaml

### Apply Pod from YAML
```
kubectl apply -f .\pod.yaml
```

### Port Forward to Localhost
```
kubectl port-forward pod_name 8000:8000
```

### Test From Inside container
```
kubectl exec -it pod_name -- /bin/bash
apt update && apt install curl -y
curl http://127.0.0.1:8000
exit
```




## Deployment.yaml 

### Apply Deployment from YAML
```
kubectl apply -f deployment.yaml
```

### Get All Deployments
```
kubectl get deployments
```

### Port Forward to Deployment
```
kubectl port-forward deployment/deployment_name 8000:8000
```

### Create Deployment with Image
```
kubectl create deployment deployment_name --image=link
```

### Delete Deployment
```
kubectl delete deployment deployment_name
```

### Expose Deployment as Service
```
kubectl expose deployment deployment_name --type=LoadBalancer --port=80
```

### Update Deployment Image
```
kubectl set image deployment deployment_name container_name=new_image_name:version
```

### Check status of Rollout
```
kubectl rollout status deployment deployment_name 
```

### Rollback a Rollout
```
kubectl rollout undo deployment deployment_name 
```

### Scale
```
kubectl scale deployment deployment_name -replicas=5
```




## Service.yaml (NOTE: Require Deployment.yaml or Pod.yaml)

### Apply Service from YAML
```
kubectl apply -f service.yaml
```

### Get All Services
```
kubectl get service
```

### Delete a Service
```
kubectl delete service service_name
```

### To access it via browser (on Minikube):
```
minikube service service_name
```




## Horizontal Pod Autoscaler (HPA)

### This tells Kubernetes to:
- Monitor CPU usage.
- Keep pods between 1 and 5 replicas.
- Scale out if CPU usage > 50%.

```
kubectl autoscale deployment social-media-deployment ^
  --cpu-percent=50 ^
  --min=1 ^
  --max=5
```

### Check the HPA status:
```
kubectl get hpa
```

### Delete HPA
```
kubectl delete hpa social-media-deployment
```

### Testing:
```
kubectl run -i --tty load-generator --rm ^
  --image=busybox ^
  -- /bin/sh

while true; do wget -q -O- http://social-media-service:8000; done
```

Watch for replica count increasing:
```
kubectl get hpa -w
kubectl get pods
```

