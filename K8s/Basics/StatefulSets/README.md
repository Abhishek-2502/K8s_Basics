1. Apply Manifest
```bash
kubectl apply -f namespace.yml -f service.yml -f statefulset.yml
```

2. Verify
```bash
kubectl get pods -n mysql
```
It should display name like mysql-statefulset-0, mysql-statefulset-1,...

3. Get Inside Pod to see Database "Devops created or not
```bash
kubectl exec -it mysql-statefulset-0 -n mysql -- bash
mysql -u root -p
show databases;
exit
exit
```
Password: root

4. Delete a Pod to verify it is mainting state or not
```bash
kubectl delete pod mysql-statefulset-0 -n mysql
kubectl get pods -n mysql
```

**Note:** StatefulSets have headless service (clusterIP: None in service.yml) that means it is not a external service and cannot be accessed be external world.