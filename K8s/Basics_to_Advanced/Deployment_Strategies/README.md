# Deployment Strategies in kubernetes

- **What is Deployment and Deployment strategies ?**
  
  - Deployment is a process of making a application available for use by audience.
  - Deployment strategies is a technique for changing/upgrading a running application from one version to another.

- **Why do we need it ?**

  - Zero downtime
  - Reduce time to market
  - Faster Rollback
  - More Frequency

## Types of Deployment Strategies

| Types    |  Downtime | Production |
| -------- | ------- | ------- |
| Recreate | Yes | No |
| Rolling Update | No | Yes |
| Blue-green | No | Yes |
| Canary | No | Yes |


## Other Strategies

| Types    | Downtime | Production |
| -------- | ------- | ------- |
| Progressive Delivery (ArgoCD Rollouts) | No | Yes |
| A/B Testing | No | No |
| Shadow | No | No |