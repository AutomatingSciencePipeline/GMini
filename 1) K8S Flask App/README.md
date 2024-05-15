# 1) Create K8S Flask App

## 1) Setup 
Within the root folder of your project, create a folder for your apps. Then create a folder within your app folder for your backend app.

```
cd <project root folder>
```

```
mkdir apps
```

```
mkdir apps/backend
```

## 2) Create a Flask Script
Create a file within your backend app folder called 'app.py'.

```
touch apps/backend/app.py
```

Within the 'app.py' file, add the following code:

```
from flask import Flask, Response
flaskApp = Flask(__name__)

@flaskApp.route("/")
def hello_world():
    return Response(status=200)
    
if __name__ == "__main__":
    flaskApp.run()
```

This is the code for a Flask app that has an endpoint '/' which returns a status of 200 when connected. 
For more info on Flask visit [GeeksForGeeks](https://www.geeksforgeeks.org/flask-tutorial/).

## 3) Create a Pipfile within your backend app folder
Pipfiles are for locking your dependencies' version. If you create an application ages ago, ideally it should work today. However, changes with dependencies might break your application. Hence we can version lock the dependency with Pipfiles and locks. 

To do so, in the command line, go into your app folder:

```
cd <your root directory>/apps/backend/
```

Then run the following to add Flask v3.0.3 as a dependency:

```
pipenv install flask~=3.0.3
```
Then to lock versions, run:

```
pipenv lock
```

## 4) Create a Docker Image
The Docker file is responsible for creating the 'template' of the application for K8S to use later. In the backend folder create a file named 'Dockerfile'. Alongside the Docker file, create a Docker ignore file called '.dockerignore'. This file is responsible for including and excluding files from the image. Within the Docker ignore file, add the following:

```
**/Dockerfile*
**/.dockerignore
```

This ignores the Docker file and the Docker ignore file. Additional files to consider ignoring are README files and things that won't be used by the app.

In the Docker file add the following:

```
FROM python:3.8-slim AS base

FROM base AS python_dependencies
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .

FROM python_dependencies AS production
RUN pipenv install --system --deploy --ignore-pipfile

WORKDIR /app
COPY . /app

USER root
ENV FLASK_ENV production
CMD flask run --host=0.0.0.0 -p 8080
```

This code sets up a 'template' that tells the app to copy all files (excluding items in the dockerignore), download the dependencies within the Pipfile, and then expose the port 8080 and then start the Flask app. Then, to sign into Docker run:

```
docker login
```

Make sure you login into your account and you have Docker desktop open. Then run the following commands in your project's *root* folder:

```
docker image build -t <your docker hub username>/gmini-backend:latest ./apps/backend
```

```
docker push <your docker hub username>/gmini-backend:latest
```

## 5) Create a Deployment
Create a new folder for your k8s objects in the root of your project. Within that folder create another folder for your backend objects. Within the backend folder, create a deployment yaml.

```
cd <project root folder>
```

```
mkdir k8s
```

```
mkdir k8s/backend
```

```
touch k8s/backend/deployment.yaml
```

Within the deployment file, add the following code:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gmini-backend
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gmini
      tier: backend
  template:
    metadata:
      labels:
        app: gmini
        tier: backend
    spec:
      containers:
        - name: gmini-backend
          image: <your dockerhub username>/gmini-backend:latest
```

The yaml files are similar to Docker files in the sense that they are like 'templates' for k8s objects.

## 6) Run your app

Within command line, run:

```
minikube start
```

This command starts up [Minikube](https://minikube.sigs.k8s.io/docs/start/), which will allow you to run Kubernetes locally. Next run the following command

```
kubectl apply -f ./k8s/backend/deployment.yaml
```

This command will create a deployment. To see if the deployment is running, use the following commands:

```
kubectl get po
```

```
kubectl logs deployment/gmini-backend
```

You should get an output similar to the following:

```
$ kubectl get po
NAME                             READY   STATUS    RESTARTS   AGE
gmini-backend-847b5c577b-g92bn   1/1     Running   0          2m28s

$ kubectl logs deployment/gmini-backend
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://<ip>:8080
 * Running on http://<ip 2>:8080
Press CTRL+C to quit
```
