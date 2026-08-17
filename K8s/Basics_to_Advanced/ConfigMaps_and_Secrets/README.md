# ConfigMaps and Secrets in Kubernetes

This example shows how to separate configuration data and sensitive values from the application deployment.

## 1. Apply Manifest
```bash
kubectl apply -f namespace.yml -f service.yml -f statefulset.yml -f configMap.yml -f secrets.yml
```

## 2. Base64 Encode Password
```bash
echo "Your Password" | base64
```

A Secret stores sensitive information like passwords, tokens, or certificates. In Kubernetes YAML, the value is usually written as base64-encoded text, because the `data` field expects encoded values.

Example:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: mysql
data:
  MYSQL_ROOT_PASSWORD: cm9vdAo=
```

Here, `cm9vdAo=` is the base64 version of `root`.

## 3. Verify
```bash
kubectl get configmap -n mysql
kubectl get secret -n mysql
kubectl get pods -n mysql
```

You can also inspect the created resources:
```bash
kubectl describe configmap mysql-config-map -n mysql
kubectl describe secret mysql-secret -n mysql
```

## What are ConfigMaps and Secrets?

### ConfigMap
A ConfigMap is used to store non-sensitive configuration data as key-value pairs. It is commonly used for environment variables, application settings, or connection details that are not secret.


### Secret
A Secret is used for sensitive data such as passwords, API keys, TLS certificates, and tokens. Although Kubernetes stores it as base64-encoded data in the manifest, it should also be protected with proper secret management and encryption at rest in production.

## Why use them?

- ConfigMaps keep application configuration separate from the pod definition.
- Secrets protect sensitive values and prevent them from being hardcoded in the deployment file.
- This makes the application more secure, easier to manage, and cleaner to deploy across environments.

In this example, the MySQL database name comes from a ConfigMap, while the root password comes from a Secret.