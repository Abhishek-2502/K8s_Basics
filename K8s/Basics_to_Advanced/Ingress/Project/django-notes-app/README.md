# Simple Notes App
This is a simple notes app built with React and Django.

## Installation (Docker)
1. Build the app
```
docker build -t notes-app .
```

2. Run the app
```
docker run -d -p 8000:8000 notes-app:latest
```

3. Install Nginx reverse proxy to make this application available
```
sudo apt-get update
sudo apt install nginx
```

## Installation (K8s)
1. Push to Dockerhub 
```
docker image tag notes-app:latest abhi25022004/notes-app:latest

docker push abhi25022004/notes-app:latest
```

2. Apply Manifest 

Change namespace to notes-app from nginx-ns in deployment.yml and service.yml
```
kubectl apply -f namespace.yml -f deployment.yml -f service.yml
```

Verfiy
```
kubectl get pods -n notes-app
```

3. Expose port 8000 in Cloud

4. Port forward
```
kubectl port-forward service/notes-app-service -n notes-app 8000:8000 --address=0.0.0.0
```

5. Access Notes app on `<VM_IP>:8000`

## Ingress
1. Push to Dockerhub 
```
docker image tag notes-app:latest abhi25022004/notes-app:latest

docker push abhi25022004/notes-app:latest
```
2. Install Ingress-Controller using `ingress-controller.md`

3. Apply Manifest of Nginx

Goto K8s/Basics_to_Advanced
```
kubectl apply -f namespace.yml -f deployment.yml 
```

Goto K8s/Basics_to_Advanced/Volume 
```
kubectl apply -f service.yml
```

4. Apply Manifest of Notes App
```
kubectl apply -f deployment.yml -f service.yml -f ingress.yml
```

Verfiy
```
kubectl get pods -n nginx-ns
```


Verfiy
```
kubectl get pods -n nginx-ns
```

5. Expose port 8000 and 8081 in Cloud

6. Port forward (8081 will be used by ingress controller)
```
kubectl port-forward service/ingress-nginx-controller -n ingress-nginx 8081:80 --address=0.0.0.0
```

7. Access Notes app on `<VM_IP>:8081` and Nginx on `<VM_IP>:8081/nginx` 
