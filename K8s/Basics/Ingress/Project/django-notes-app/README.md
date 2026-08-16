# Simple Notes App
This is a simple notes app built with React and Django.

## Requirements
1. Python 3.9
2. Node.js
3. React

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

`sudo apt-get update`
`sudo apt install nginx`

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

2. Apply Manifest to see Ingress
```
kubectl apply -f deployment.yml -f service.yml
```

Verfiy
```
kubectl get pods -n nginx-ns
```

3. Expose port 8000 in Cloud

4. Port forward
```
kubectl port-forward service/notes-app-service -n <namespace-name> 8000:8000 --address=0.0.0.0
```