# GMini
Mini version of Glados for onboarding purposes.

## Setup
- Docker Desktop w/ DockerHub Account
- MiniKube
- Kubernetes Python Client

```
docker image build -t <your docker hub username>/gmini-frontend:latest ./apps/frontend
```

```
docker push <your docker hub username>/gmini-frontend:latest
```

```
kubectl apply -f ./k8s/frontend/deployment.yaml
```


```
kubectl port-forward deployment/gmini-frontend 3000:3000
```

```
kubectl delete po,svc -l app=gmini
```