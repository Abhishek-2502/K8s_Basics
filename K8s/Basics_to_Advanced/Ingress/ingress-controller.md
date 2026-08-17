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

## Accessing Ingress on a Custom Port

The Ingress Controller listens on port `80` inside the KIND cluster.

If you want to access the Ingress Controller using a custom port such as `8081`, you can use `kubectl port-forward` without changing the KIND configuration.

First, verify the Ingress Controller Service:

```bash
kubectl get svc -n ingress-nginx
```

Then forward port `8081` on the VM to port `80` of the Ingress Controller:

```bash
kubectl port-forward -n ingress-nginx \
  svc/ingress-nginx-controller 8081:80 \
  --address 0.0.0.0
```

> **Note:** `kubectl port-forward` is primarily intended for development and testing. The port-forwarding process must remain running for the application to be accessible.

The external port can also be configured directly in `kind-config.yaml` using `extraPortMappings`.

For example, to expose the Ingress Controller on port `8081`:

```yaml
extraPortMappings:
  - containerPort: 80
    hostPort: 8081
    protocol: TCP
````

Here:

* `hostPort` → Port exposed on the VM/host.
* `containerPort` → Port inside the KIND node.
* `containerPort` remains `80`.
* The Kubernetes Services and Ingress Controller continue to use port `80`.


#### Important

KIND port mappings are configured when the cluster is created. If you change the `hostPort` in `kind-config.yaml`, you need to recreate the KIND cluster:

```bash
kind delete cluster --name <cluster-name>
kind create cluster --config kind-config.yaml
```

After recreating the cluster, install the Ingress Controller again using [ingress-controller.md](ingress-controller.md).


#### Port Forwarding vs KIND Port Mapping

* **`kind-config.yaml` → `extraPortMappings`** for a persistent VM-to-KIND port mapping.
* **`kubectl port-forward`** for temporary development/testing access.

This gives the reader both approaches without confusing **external port `8081`** with the internal Kubernetes **port `80`**.
