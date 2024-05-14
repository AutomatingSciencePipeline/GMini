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


