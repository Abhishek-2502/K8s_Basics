## Install NGINX Ingress Controller in KIND

Install the NGINX Ingress Controller using the KIND-specific manifest:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Wait for the Ingress Controller to become ready:
```bash
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

Verify the Ingress Controller:
```bash
kubectl get pods -n ingress-nginx
```

You should see the controller pod in the `Running` state:
```text
NAME                                        READY   STATUS    RESTARTS   AGE
ingress-nginx-controller-xxxxxxxxxx-xxxxx   1/1     Running   0          1m
```

Verify the service:
```bash
kubectl get svc -n ingress-nginx
```

The NGINX Ingress Controller should be available through the ports already mapped in your KIND configuration.

## Install NGINX Ingress Controller in Minikube

Enable the built-in Ingress addon:
```bash
minikube addons enable ingress
```

Verify:
```bash
kubectl get pods -n ingress-nginx
```

## Changing the Port to access Ingress
By default, the KIND configuration may expose the Ingress Controller on port 80 in `kind-config.yaml`
```
extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
```

1. If you want to access the Ingress Controller using a custom port such as 8081, change the hostPort:
```
extraPortMappings:
  - containerPort: 80
    hostPort: 8081  # Change to desired port
    protocol: TCP
```

Here:
 - hostPort → Port exposed on the VM/host.
 - containerPort → Port inside the KIND node.
 - containerPort remains 80.
 - Only the external hostPort needs to be changed.

2. Recreate the cluster
```bash
kind delete cluster --name <cluster-name>
kind create cluster --config kind-config.yaml
```

3. Install the Ingress Controller Again