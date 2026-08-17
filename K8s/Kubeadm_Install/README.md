# Kubeadm Installation Guide

This guide outlines the steps needed to set up a Kubernetes cluster using `kubeadm`.

## Prerequisites

- Ubuntu OS (Xenial or later)
- `sudo` privileges
- t2.medium instance type or higher


## AWS Setup

1. Ensure that all instances are in the same **Security Group**.
2. Expose port **6443** in the **Security Group** to allow worker nodes to join the cluster.
3. Expose port **22** in the **Security Group** to allows SSH access to manage the instance..


## Execute on Both "Master" & "Worker" Nodes
Use the provided [file](Kubeadm_Installation_Common_Using_Containerd.sh)

## Execute ONLY on the "Master" Node
Use the provided [file](Kubeadm_Installation_Master_Using_Containerd.sh)

> Copy this generated token for next command.

## Execute on ALL of your Worker Nodes
Use the provided [file](Kubeadm_Installation_Slave_Using_Containerd.sh)

## Verify Cluster Connection

**On Master Node:**

```bash
kubectl get nodes
```

## Verify Container Status on Worker Node
```bash
sudo ctr -n k8s.io containers list
sudo ctr -n k8s.io tasks list
```