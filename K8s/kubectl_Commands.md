# Kubectl Commands
**`NAMESPACE` [ `Container ->` `Pod ->` `Deployment ->` `Service ->` `User🙍`]**

**Note:** Use 'sudo -E' before any command if any permission issue came.

## 🌟 NODE

### Get All Services
```
kubectl get nodes
```

## 🌟 NAMESPACE
### Show all namespaces
```
kubectl get ns
```
```
kubectl get namespace
```

### Create namespace
```
kubectl create ns namespace-name
```
**Ex:** kubectl create ns nginx-ns


### Delete a namespace
```
kubectl delete ns namespace-name
```

### Setting default namespace
```
kubectl config set-context --current --namespace=namespace-name
```

### Verify the current context
```
kubectl config current-context
```

### Check the namespace configured in the current context
```
kubectl config view --minify | grep namespace:
```

## 🌟 MANIFEST FILE
### Apply a Manifest file (YAML)
```
kubectl apply -f manifest_filename
```

### Apply all Manifest file in a directory
```
kubectl apply -f .
```

### Delete a Manifest
```
kubectl delete -f manifest_filename
```

## 🌟 PODS
### Get Pods
```
kubectl get pods 
```
```
kubectl get pods -A
```
```
kubectl get pods -n namespace-name -o wide
```

### Show all Pods in a namespace 
```
kubectl get pods -n namespace-name
```
```
kubectl namespace=namespace-name get pods
```
**Ex:** kubectl get pods -n kube-system


### Create pod using a image from dockerhub
```
kubectl run pod-name --image=image-name
```
**Ex:** kubectl run nginx --image=nginx


### Create pod in a namespace
```
kubectl run pod-name --image=image-name -n namespace-name
```
**Ex:** kubectl run nginx --image=nginx -n nginx-ns


### Delete Pod
```
kubectl delete pod pod-name
```


### Delete Pod in a namespace
```
kubectl delete pod pod-name -n namespace-name
```


### Get logs
```
kubectl logs pod-name
```
```
kubectl logs pod/pod-name -n namespace-name
```

### Get Pods info
```
kubectl describe pods
```
```
kubectl describe pod/pod-name -n namespace-name
```

### Port Forward to Localhost
```
kubectl port-forward pod-name port-number(your machine):port-number(inside pod)
```

### Execute Commands inside Pod
```
kubectl exec -it pod/pod-name -n namespace-name -- bash
```
**Ex:** kubectl exec -it pod/nginx-pod -n nginx -- bash

To verify nginx:
```
curl 127.0.0.1
```

## 🌟 DEPLOYMENT

**Note:** Replace deployments with replicaset for ReplicaSet Commands

**Note:** Replace deployments with deploy. Both are same

### Get All Deployments
```
kubectl get deployments
```
```
kubectl get deployments -n namespace-name
```

### Port Forward to Deployment
```
kubectl port-forward deployment/deployment-name port-number(your machine):port-number(inside pod)
```

### Create Deployment with Image
```
kubectl create deployment deployment-name --image=link
```

### Delete Deployment
```
kubectl delete deployment deployment-name
```

### To check how deployment creates ReplicaSet & Pods
```
kubectl describe deploy deployment-name
kubectl get rs
```

### Expose Deployment as Service
```
kubectl expose deployment deployment-name --type=LoadBalancer --port=port-number
```

### ROLLING UPDATE & ROLLBACK (Supported by Deployment only)

---

### Update Deployment Image (ROLLING UPDATE)
```
kubectl set image deployment deployment-name container-name=new_image-name:version
```
**Ex:** kubectl set image deployment/nginx-deployment -n nginx nginx=nginx:1.27.3 


### Check status of Rollout
```
kubectl rollout status deployment deployment-name 
```
**Ex:** kubectl rollout status deployment nginx-deployment -n nginx 

### Rollback a Rollout (ROLLOUT)
```
kubectl rollout undo deployment deployment-name 
```
**Ex:** kubectl rollout undo deployment nginx-deployment -n nginx 

### Rollback a Rollout to specific version
```
kubectl rollout undo deployment deployment-name --to-revision=revision_number
```

###  History of your versions or about deploymnets
```
kubectl rollout history deployment deployment-name 
```

### Scale Up/Down
```
kubectl scale deployment deployment-name -replicas=number-of-replica
```
**Ex:** kubectl scale deployment/nginx-deployment -n nginx --replicas=5



## 🌟 SERVICE

### Get All Services
```
kubectl get service
```

### Delete a Service
```
kubectl delete service service-name
```

### To access it via browser (on Minikube):
```
minikube service service-name
```

### Port Forward 
```
kubectl port-forward service/service-name port-number(your machine):port-number(inside pod) --address=0.0.0.0
```
**Ex:** kubectl port-forward service/nginx-service 8081:80 --address=0.0.0.0


### Port Forward in namespace
```
kubectl port-forward service/service-name -n namespace-name port-number(your machine):port-number(inside pod) --address=0.0.0.0
```
**Ex:** kubectl port-forward service/nginx-service -n nginx-ns 8081:80 --address=0.0.0.0

### Get all Pod, Deployment, Services, Replicasets etc
```
kubectl get all
```

## 🌟 VOLUME

### Get All Volumes
```
kubectl get pv
```

### Get All Volumes Claims
```
kubectl get pvc
```

### Get All Volumes in a namespace
```
kubectl get pv -n namespace-name
```

### Get All Volumes Claims in a namespace
```
kubectl get pvc -n namespace-name
```

### Delete Volumes
```
kubectl delete pv-name
```

### Delete Volumes Claims
```
kubectl delete pvc-name
```

## 🌟 HORIZONTAL POD AUTOSCALER (HPA)

### This tells Kubernetes to:
- Monitor CPU usage.
- Keep pods between 1 and 5 replicas.
- Scale out if CPU usage > 50%.

```
kubectl autoscale deployment deployment-name ^
  --cpu-percent=50 ^
  --min=1 ^
  --max=5
```

### Check the HPA status:
```
kubectl get hpa
```
```
kubectl get hpa -w
```

### Delete HPA
```
kubectl delete hpa deployment-name
```
