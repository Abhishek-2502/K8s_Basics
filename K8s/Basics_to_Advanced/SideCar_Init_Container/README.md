# Init Containers and Sidecar Containers

This folder contains two Kubernetes Pod examples:

- `init-container.yml`: Demonstrates an init container that runs before the
  main application container.
- `sidecar-container.yml`: Demonstrates a sidecar container that works beside
  the main container and reads logs from a shared volume.

## Init Container

An init container runs before the application containers in a Pod. Kubernetes
waits for every init container to finish successfully before starting the main
containers.

In `init-container.yml`:

- The init container is named `init-container`.
- It prints a start message, waits for 30 seconds, and prints a completion
  message.
- The main container starts after the init container completes.

### Deploy the init container Pod

```bash
kubectl apply -f init-container.yml
kubectl get pods
```

The Pod may remain in the `Init:0/1` state while the init container is running.
After it completes, the Pod can start the main container.

View logs from the init container:

```bash
kubectl logs init-test -c init-container
```
Output:

```text
Initalization started ...
Initization completed.
```

View logs from the main container:

```bash
kubectl logs init-test -c main-container
```

Output:

```text
Main container started
```

To watch logs continuously:

```bash
watch kubectl logs init-test -c init-container
```

Delete the Pod after testing:

```bash
kubectl delete pod init-test
```

## Sidecar Container

A sidecar container runs alongside the main application container in the same
Pod. Both containers can share files, volumes, and the Pod network.

In `sidecar-container.yml`:

- `main-container` writes application messages to `/var/log/app.log`.
- `sidecar-container` runs `tail -f` and displays the same log file.
- Both containers mount the shared `emptyDir` volume named `shared-logs`.
- The sidecar continues reading the log while the main container writes to it.

### Deploy the sidecar Pod

```bash
kubectl apply -f sidecar-container.yml
kubectl get pods
```

View logs from the main container:

```bash
kubectl logs sidecar-test -c main-container
```

Output: No output. The main container writes its messages to the shared log
file instead of writing them to standard output.

View the log stream from the sidecar container:

```bash
watch kubectl logs sidecar-test -c sidecar-container
```

Example output:

```text
Hello Dosto
Hello Dosto
...
```

Delete the Pod after testing:

```bash
kubectl delete pod sidecar-test
```

## Init Container vs Sidecar Container

| Feature | Init container | Sidecar container |
| --- | --- | --- |
| Start time | Runs before the main container | Runs alongside the main container |
| Completion | Must finish successfully | Usually keeps running with the application |
| Common use | Setup, initialization, or dependency checks | Logging, monitoring, proxy, or supporting services |
| Example here | Waits 30 seconds before startup | Reads the main container's shared log file |

## Real-Life Examples

### Init Container Examples

- A database application checks that required database tables exist before the
  main application starts.
- An application downloads configuration files or certificates before startup.
- A web application waits for required setup tasks, such as creating folders
  or loading initial data, to finish.
- A service validates environment settings and stops the Pod from starting when
  the configuration is invalid.

### Sidecar Container Examples

- A log collector reads application log files and sends them to a central
  logging system.
- A service-mesh proxy handles network traffic, retries, and security while the
  main application focuses on business logic.
- A monitoring agent collects application metrics and sends them to a monitoring
  platform.
- A file synchronization helper keeps shared files updated for the main
  application.
