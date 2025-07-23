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

# CHOCOLATEY
https://chocolatey.org/install

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

# KUBERNETES
https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-nonstandard-package-tools

### Install
```
choco install kubernetes-cli
```
```
kubectl version --client
```

If you're using cmd.exe: 
```
cd %USERPROFILE%
```

Otherwise: 
```
cd ~
```
```
mkdir .kube
```
```
cd .kube
```
```
New-Item config -type file
```


# MINIKUBE
https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download

### Install
```
choco install minikube
```
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
minikube addons enable metrics-server
```
```
minikube start
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
minikube pause
```
```
minikube unpause
```
```
minikube stop
```

To make docker the default driver:
```
minikube config set driver docker
```


pod_name = social-media-fastapi
```
kubectl get pods -A
```
```
kubectl get pods
```
```
kubectl apply -f .\pod.yaml
```
```
kubectl delete pod pod_name
```

```
kubectl exec -it pod_name -- /bin/bash
apt update && apt install curl -y
curl http://127.0.0.1:8000
exit
```

```
kubectl port-forward pod_name 8000:8000
```
