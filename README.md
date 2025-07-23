# Docker
#### Build: 
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

# CHOCOLATEY
https://chocolatey.org/install

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

# KUBERNETES
https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-nonstandard-package-tools

#### Install
```
choco install kubernetes-cli
```
```
kubectl version --client
```

#### If you're using cmd.exe: 
```
cd %USERPROFILE%
```

#### Otherwise: 
```
cd ~
```
```
mkdir .kube
cd .kube
New-Item config -type file
```
```
kubectl config view
```

# MINIKUBE
https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download

#### Install
```
choco install minikube
```

#### Start
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

#### Other Basics
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
minikube pause
```
```
minikube unpause
```
```
minikube stop
```

#### Metrics Service
```
minikube addons enable metrics-server
kubectl get deployment metrics-server -n kube-system
```



#### To make docker the default driver:
```
minikube config set driver docker
```

#### Get Pods
```
kubectl get pods -A
```
```
kubectl get pods
```

#### Delete Pod
```
kubectl delete pod pod_name
```

## Pod.yaml
```
kubectl apply -f .\pod.yaml
```

#### Port Forward to Localhost
```
kubectl port-forward pod_name 8000:8000
```

#### Test From Inside container
```
kubectl exec -it pod_name -- /bin/bash
apt update && apt install curl -y
curl http://127.0.0.1:8000
exit
```

## Deployment.yaml 
```
kubectl apply -f deployment.yaml
```
```
kubectl get deployments
```
```
kubectl port-forward deployment/social-media-deployment 8000:8000
```

```
kubectl create deployment my-app --image=link
kubectl delete deployment my-app
kubectl expose deployment my-app --type=LoadBalancer --port=80
```

## Service.yaml (Require Deployment.yaml or Pod.yaml)
```
kubectl apply -f service.yaml
```
```
kubectl get service
```

#### To access it via browser (on Minikube):
```
minikube service service_name
```

## Horizontal Pod Autoscaler (HPA)

#### This tells Kubernetes to:
- Monitor CPU usage.
- Keep pods between 1 and 5 replicas.
- Scale out if CPU usage > 50%.

```
kubectl autoscale deployment social-media-deployment ^
  --cpu-percent=50 ^
  --min=1 ^
  --max=5
```

#### Check the HPA status:
```
kubectl get hpa
```

#### Delete HPA
```
kubectl delete hpa social-media-deployment
```

#### Testing:
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

