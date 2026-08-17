# Kubernetes Probes

This example demonstrates the three main kubelet probes used in Kubernetes:
- `startupProbe`
- `readinessProbe`
- `livenessProbe`

## 1. Apply the manifests
```bash
kubectl apply -f namespace.yml
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

## 2. Verify the pods
```bash
kubectl get pods -n probe-demo
kubectl get deployment -n probe-demo
kubectl get svc -n probe-demo
```

## 3. Check pod events and probe status
```bash
kubectl describe pod -n probe-demo
```

Look for:
- `Startup probe failed`
- `Readiness probe failed`
- `Liveness probe failed`

## 4. Understand the probe types

### Startup Probe
The `startupProbe` checks if the application has finished starting up.
It helps prevent the liveness probe from restarting a slow-starting container too early.

```yaml
startupProbe:
  httpGet:
    path: /
    port: 80
  failureThreshold: 30
  periodSeconds: 5
```

### Readiness Probe
The `readinessProbe` decides whether the container is ready to receive traffic.
If it fails, Kubernetes removes the pod from service endpoints.

```yaml
readinessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 3
  periodSeconds: 5
```

### Liveness Probe
The `livenessProbe` checks whether the application is still alive.
If it fails repeatedly, Kubernetes restarts the container.

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 10
  periodSeconds: 10
```

## 5. Example flow
- Container starts
- `startupProbe` runs until app is ready
- `readinessProbe` marks the pod as ready for traffic
- `livenessProbe` keeps checking if the app is still alive

## 6. Why probes are important
Probes help Kubernetes keep applications healthy by:
- restarting crashed containers
- avoiding traffic before the app is ready
- handling slow startup gracefully

**Note:** In a real-world app, probes are often based on HTTP endpoints, TCP checks, or command execution depending on the application behavior.