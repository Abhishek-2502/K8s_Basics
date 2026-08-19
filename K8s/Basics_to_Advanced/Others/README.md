# Other Kubernetes Topics

This folder contains additional Kubernetes and container-related topics that do
not belong to a single Kubernetes resource type.

## Kubernetes Operators

A Kubernetes Operator is a controller that uses the Kubernetes API to manage an
application or service. Operators automate tasks such as installation,
configuration, upgrades, backups, and recovery.

Operators commonly run as background processes in the cluster and continuously
check the desired state against the current state.

## Kubernetes API and Kopf

The Kubernetes API is the interface used to create, read, update, and delete
Kubernetes resources. Applications and controllers can use this API to watch
resources and react to changes.

[Kopf](https://kopf.readthedocs.io/) is a Python framework for building
Kubernetes Operators. It provides Python handlers for events such as creating,
updating, or deleting Kubernetes resources.

```text
Kubernetes API -> Kopf Operator -> Application resources
```

## Image Scanning

Image scanning checks container images for known security vulnerabilities,
misconfigurations, and exposed secrets before the images are deployed.

### Trivy

[Trivy](https://github.com/aquasecurity/trivy) is an open-source security
scanner for container images, filesystems, Git repositories, and Kubernetes
configurations.

Example:

```bash
trivy image <image-name>:<tag>
```

### Docker Scout

[Docker Scout](https://docs.docker.com/scout/) analyzes container images and
provides information about vulnerabilities, software packages, and image
recommendations.

Example:

```bash
docker scout cves <image-name>:<tag>
```

Scanning images before deployment helps identify security issues early in the
build and deployment process.
