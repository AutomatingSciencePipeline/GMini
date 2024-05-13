# 2) Create Next.js App
## 1) Create a Next.js Image

GLADOS uses vercel to quickly setup a solid foundation for the frontend. First:

```
cd apps/
```

Then start the the project by running:

```
npx create-next-app@14.2.3
```

Respond to the prompts with the following:


```
√ What is your project named? ... frontend
√ Would you like to use TypeScript? ... Yes
√ Would you like to use ESLint? ... Yes
√ Would you like to use Tailwind CSS? ... Yes
√ Would you like to use `src/` directory? ... No
√ Would you like to use App Router? (recommended) ... Yes
√ Would you like to customize the default import alias (@/*)? ... No
```

## 2) Create a Docker Image

Try to make the docker image yourself. If you need help, refer to the solution. As a guide, here are the steps I took:
1) create a Dockerfile
2) create a .dockerignore file
3) implement the .dockerignore (don't forget to exclude the 'node_modules' folder)
4) implement the Dockerfile

Like the backend, use the following commands to create the frontend image:

```
docker image build -t <your docker hub username>/gmini-frontend:latest ./apps/frontend
```

```
docker push <your docker hub username>/gmini-frontend:latest
```

## 3) Create a Deployment

Try to make the frontend deployment yourself. If you need help, refer to the solution. Don't forget to use the port 3000.

To create a frontend k8s object, run:

```
kubectl apply -f ./k8s/frontend/deployment.yaml
```

Note that this image is larger so it might take a longer time to setup.

To check the status of the pod, run the following commands:

```
kubectl get po
```

```
kubectl logs deployment/gmini-frontend
```

To access the frontend run the following command:


```
kubectl port-forward deployment/gmini-frontend 3000:3000
```

It should be up on [localhost:3000](http://localhost:3000/) if setup the same way I did it.
