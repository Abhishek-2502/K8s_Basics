# Minikube Installation Guide for Ubuntu
This guide provides step-by-step instructions for installing Minikube on Ubuntu. Minikube allows you to run a single-node Kubernetes cluster locally for development and testing purposes.

## Pre-requisites

* Ubuntu OS
* Docker
* sudo privileges
* Virtualization support enabled (Check with `egrep -c '(vmx|svm)' /proc/cpuinfo`, 0=disabled 1=enabled) 

---

## Step 1: Update System Packages

Update your package lists to make sure you are getting the latest version and dependencies.
```bash
sudo apt update
```


## Step 2: Install Required Packages

```bash
sudo apt install -y curl wget apt-transport-https
```

---

## Step 3: Install Minikube

First, download the Minikube binary using `curl`:
```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
```

Make it executable and move it into your path:
```bash
chmod +x minikube
sudo mv minikube /usr/local/bin/
minikube version
```

---

## Step 4: Install kubectl

Download kubectl, which is a Kubernetes command-line tool.
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
**Check above image ⬆️**
Make it executable and move it into your path:
```bash
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version
```


---

## Step 5: Start Minikube

Now, you can start Minikube with the following command:

```bash
minikube start --driver=docker --vm=true 
```

This command will start a single-node Kubernetes cluster inside a Docker container. --vm is set true to run it on Cloud instance like ec2.
