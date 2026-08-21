### Install AWS-CLI (on local)
```bash
sudo apt-get install unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- Goto IAM and create a user (example: eks-user). Give Admin permission.
- Click on newly created user and goto Security credentials.
- Create a Access key.
- Select Command Line Interface (CLI) in Use case.
- You will get `Access key` and `Secret Access key`

```bash
aws configure
```
It will ask for `Access key` and `Secret Access key`.

Default region name: ap-south-1

Verify:
```bash
aws s3 ls
```

### Install eksctl (on local)
```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

## Create EKS Cluster
```bash
eksctl create cluster --name=tws-cluster \
                    --region=ap-south-1 \
                    --version=1.30 \
                    --without-nodegroup
```

### Associate IAM OIDC Provider
```bash
eksctl utils associate-iam-oidc-provider \
  --region ap-south-1 \
  --cluster tws-cluster \
  --approve
```

### Create Nodegroup
Create Key pair under Network and Security called `eks-nodegroup-key`

```bash
eksctl create nodegroup --cluster=tws-cluster \
                     --region=ap-south-1 \
                     --name=tws-cluster-ng \
                     --node-type=t2.medium \
                     --nodes=2 \
                     --nodes-min=2 \
                     --nodes-max=2 \
                     --node-volume-size=29 \
                     --ssh-access \
                     --ssh-public-key=eks-nodegroup-key 
```

Verify:
```bash
kubectl get nodes
kubectl get nodes --use-context=abhi-kind-cluster
```

### Switching context
```bash
aws eks update-kubeconfig --region ap-south-1 --name tws-cluster
```