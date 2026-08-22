## Rolling Update Deployment Strategy

- A rolling update in Kubernetes is a deployment strategy used to gradually replace the existing set of Pods with a new set of Pods one by one.
- This ensures that there is no downtime during the update process as the application continues to serve requests while the update is in progress.


### How it works ?

- <b>Pod Creation:</b> kubernetes creates one new pod of newer version.
- <b>Pod Termination:</b> It terminates existing pods.

| Pro's    | Con's |
| -------- | ------- |
| Version is slowly released across instances | Rollout/Rollback can take time    |
| Convenient for stateful applications | No control over traffic |

> Note:
> This deployment strategy is suitable for UAT,QA environment.
> For stateful applications suitable on production environment

![image](https://github.com/user-attachments/assets/ef9a9088-0f0b-4645-9c66-505481c7eb6f)

---

### Prerequisites to try this:

1. Instance with Ubuntu OS

2. Docker installed & Configured

3. Kind Installed

4. Kubectl Installed

---

### Steps to implement rolling-update deployment

- Apply all the manifest files present in the current directory.

    ```bash
    kubectl apply -f rolling-namespace.yml
    kubectl apply -f .
    ```

- Run this command to get all resources created in `rolling-ns` namespace.

    ```bash
    kubectl get all -n rolling-ns
    ```

- Forward the svc port to the instance port 3000

    ```bash
    kubectl port-forward --address 0.0.0.0 svc/rolling-update-service 3000:3000 -n rolling-ns &
    ```

- Open the inbound rule for port 3000 in that Instance and check the application at URL:

    ```bash
    http://<Your_Instance_Public_Ip>:3000
    ```

- Open a new tab of terminal and connect your instance and run the watch command to monitor the deployment

    ```bash
    watch kubectl get pods -n rolling-ns
    ```

- You have successfully accessed the `online_shop with footer` webpage. Now edit the deployment file and change the image from <b>`online_shop`</b> to <b>`online_shop_without_footer`</b> and apply.

    ```bash
    kubectl apply -f recreate-deployment.yml
    ```

- or, You can directly change image through kubectl command:

    ```bash
    kubectl set image deployment/online-shop online-shop=amitabhdevops/online_shop_without_footer -n rolling-ns
    ```

- Immediately go to second tab where ran watch command and monitor (It will delete all the pods and then create new ones).

---

## Cleanup

```bash
kubectl delete -f .
```

---

> Note:
>
> If you cannot access the web app after the update, check your terminal — you probably encountered an error like:
>
>   ```bash
>   error: lost connection to pod
>   ```
>
> Don’t worry! This happens because we’re running the cluster locally (e.g., with **Kind**), and the `kubectl port-forward` session breaks when the underlying pod is replaced during deployment (especially with `Recreate` strategy).
>
> 🔁 Just run the `kubectl port-forward` command again to re-establish the connection and access the app in your browser.
>
> ✅ This issue won't occur when deploying on managed Kubernetes services like **AWS EKS**, **GKE**, or **AKS**, because in those environments you usually expose services using `NodePort`, `LoadBalancer`, or Ingress — not `kubectl port-forward`.

