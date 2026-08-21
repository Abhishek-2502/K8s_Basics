# Run the Chat App on Minikube

## Tech Stack
- Backend: Node
- Frontend: React
- DB: Mongo

## Prerequisites

- Install and start Minikube using the [Minikube installation guide](../../../../../Minikube_Install/README.md).
- Docker Hub account

Log in to Docker Hub:

```bash
docker login
```

## Build and Push Images

Run these commands from the project root:

```bash
cd backend
docker build --no-cache -t abhi25022004/chatapp-backend:latest .
docker push abhi25022004/chatapp-backend:latest

cd ../frontend
docker build --no-cache -t abhi25022004/chatapp-frontend:latest .
docker push abhi25022004/chatapp-frontend:latest

cd ../k8s
```

## Deploy to Kubernetes

```bash
minikube addons enable ingress
kubectl apply -f namespace.yml
kubectl get ns

kubectl apply -f mongodb-pv.yml
kubectl get pv -n chat-app

kubectl apply -f mongodb-pvc.yml
kubectl get pvc -n chat-app

kubectl apply -f secrets.yml

kubectl apply -f mongodb-deployment.yml
kubectl apply -f backend-deployment.yml
kubectl get pods -n chat-app

kubectl apply -f backend-service.yml
kubectl apply -f frontend-service.yml
kubectl apply -f mongodb-service.yml
kubectl get svc -n chat-app

kubectl apply -f frontend-deployment.yml
kubectl get pods -n chat-app

kubectl apply -f ingress.yml
kubectl get ing -n chat-app

```

## Restart the Backend Deployment

Because the backend uses the reusable `:latest` image tag, restart the deployment after pushing a new backend image:

```bash
kubectl rollout restart deployment/backend-deployment -n chat-app
kubectl rollout status deployment/backend-deployment -n chat-app
```

## Open the App

Add the ingress hostname to the hosts file.

**Windows:** Edit `C:\Windows\System32\drivers\etc\hosts` as Administrator (Open Notepade as Admin and open this file) and add:

```text
127.0.0.1 chat-tws.com
```

Start the ingress port-forward in a separate terminal and keep it running:

```bash
kubectl port-forward service/ingress-nginx-controller -n ingress-nginx 80:80
```

Open the app at <http://chat-tws.com>.

Backend at <http://chat-tws.com/api>.

## Stop and Remove the App

```bash
kubectl delete -f .
minikube stop
```