# Minikube Installation on Windows/local System

This guide provides step-by-step instructions for installing Minikube on windows with pre-requisites. Minikube allows you to run a single-node Kubernetes cluster locally for development and testing purposes.


## Pre-requisites

- Windows os
- Container manager : Docker

### Note: Run the following commands in CMD admin mode


## KUBECTL
https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-nonstandard-package-tools

### CHOCOLATEY POLICY
https://chocolatey.org/install

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Install
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

## MINIKUBE
https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download

### Install
```
choco install minikube
```