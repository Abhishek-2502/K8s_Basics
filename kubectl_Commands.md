# Kubectl Commands
**`NAMESPACE` [ `Container ->` `Pod ->` `Deployment ->` `Service ->` `User🙍`]**


## NAMESPACE
### Show all namespaces
```
kubectl get ns
```
```
kubectl get namespace
```

### Create namespace
```
kubectl create ns namespace_name
```
**Ex:** kubectl create ns nginx_ns


### Delete a namespace
```
kubectl delete ns namespace_name
```


## PODS
### Get Pods
```
kubectl get pods 
```
```
kubectl get pods -A
```
```
kubectl get pods -n namespace_name -o wide
```

### Show all Pods in a namespace 
```
kubectl get pods -n namespace_name
```
**Ex:** kubectl get pods -n kube-system


### Create pod using a image from dockerhub
```
kubectl run pod_name --image=image_name
```
**Ex:** kubectl run nginx --image=nginx


### Create pod in a namespace
```
kubectl run pod_name --image=image_name -n namespace_name
```
**Ex:** kubectl run nginx --image=nginx -n nginx_ns


### Delete Pod
```
kubectl delete pod pod_name
```


### Delete Pod in a namespace
```
kubectl delete pod pod_name -n namespace_name
```


### Get logs
```
kubectl logs pod_name
```
```
kubectl logs pod/pod_name -n namespace_name
```

### Get Pods info
```
kubectl describe pods
```
```
kubectl describe pod/pod_name -n namespace_name
```

### Port Forward to Localhost
```
kubectl port-forward pod_name 8000:8000
```

### Apply a Manifest file (YAML)
```
kubectl apply -f manifest_filename
```
### Delete a Manifest
```
kubectl delete -f manifest_filename
```

### Execute Commands inside Pod
```
kubectl exec -it pod/pod_name -n namespace_name -- bash
```
**Ex:** kubectl exec -it pod/nginx-pod -n nginx -- bash

To verify nginx:
```
curl 127.0.0.1
```

## DEPLOYMENT

**Note:** Replace deployments with replicaset for ReplicaSet Commands

### Get All Deployments
```
kubectl get deployments
```
```
kubectl get deployments -n namespace_name
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

### Update Deployment Image (ROLLING UPDATE)
```
kubectl set image deployment deployment_name container_name=new_image_name:version
```
**Ex:** kubectl set image deployment/nginx-deployment -n nginx nginx=nginx:1.27.3 


### Check status of Rollout
```
kubectl rollout status deployment deployment_name 
```
**Ex:** kubectl rollout status deployment nginx-deployment -n nginx 

### Rollback a Rollout
```
kubectl rollout undo deployment deployment_name 
```
**Ex:** kubectl rollout undo deployment nginx-deployment -n nginx  

### Scale
```
kubectl scale deployment deployment_name -replicas=5
```
**Ex:** kubectl scale deployment/nginx-deployment -n nginx --replicas=5



## SERVICE

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


## HORIZONTAL POD AUTOSCALER (HPA)

### This tells Kubernetes to:
- Monitor CPU usage.
- Keep pods between 1 and 5 replicas.
- Scale out if CPU usage > 50%.

```
kubectl autoscale deployment deployment_name ^
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
kubectl delete hpa deployment_name
```
