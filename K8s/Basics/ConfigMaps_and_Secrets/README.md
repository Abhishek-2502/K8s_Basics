1. Apply Manifest
```bash
kubectl apply -f namespace.yml -f service.yml -f statefulset.yml -f configMaps.yml -f secrets.yml
```

2. Base64 Encode Password
```bash
echo "Your Password | base64
```

3. Verify
```bash
kubectl get configmap -n mysql
kubectl get secret -n mysql
kubectl get pods -n mysql
```