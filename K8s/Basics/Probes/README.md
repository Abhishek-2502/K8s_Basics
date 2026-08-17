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

Example output from the pod description:
```bash
Ready:          True
Liveness:       http-get http://:80/ delay=10s timeout=1s period=10s #success=1 #failure=3
Readiness:      http-get http://:80/ delay=3s timeout=1s period=5s #success=1 #failure=3
Startup:        http-get http://:80/ delay=0s timeout=1s period=5s #success=1 #failure=30
```

This indicates:
- the container is currently `Ready: True`
- liveness checks are configured and passing
- readiness checks are configured and passing
- startup checks are configured and passing

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

## 7. Interview Question
### Why is the failure threshold 3 for readiness and liveness, and 30 for startup?
Because the threshold value depends on the purpose of the probe:

- `readinessProbe` checks whether the application is ready to receive traffic.
  - If the app is not ready, Kubernetes should remove it from service endpoints quickly.
  - Therefore, the failure threshold is usually lower, such as `3`.

- `livenessProbe` checks whether the application is still alive.
  - If the app is unhealthy, Kubernetes should restart it quickly.
  - Therefore, the failure threshold is also usually lower, such as `3`.

- `startupProbe` checks whether the application is still starting up.
  - A slow app may take longer to initialize.
  - Therefore, Kubernetes gives it more time before considering it failed.
  - That is why the threshold can be higher, such as `30`.

In short:
- `readinessProbe` = app not ready for traffic
- `livenessProbe` = app is unhealthy, restart it
- `startupProbe` = app is still initializing, allow more time

**Note:** In a real-world app, probes are often based on HTTP endpoints, TCP checks, or command execution depending on the application behavior.