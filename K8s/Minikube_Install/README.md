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

# MINIKUBE COMMANDS

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
```
minikube start --driver=virtualbox -vm=true
```

### Other 
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

### To make docker the default driver:
```
minikube config set driver docker
```

### Metrics Service
```
minikube addons enable metrics-server
kubectl get deployment metrics-server -n kube-system
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



## Service.yaml (NOTE: Require Deployment.yaml or Pod.yaml)

### Apply Service from YAML
```
kubectl apply -f service.yaml
```

### Get All Services
```
kubectl get service
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

