# 4) In-Cluster Job
## 1) Create a Simple Runner App

Try creating another python app by yourself. This app will be a runner that currently runs an experiment. Since the runner does not have endpoints, there is no need to have it as a Flask app. The only thing the app.py script should do is take a json argument and print out the experiment ID. Here are the general steps I took for reference:

- create app.py script
- create Dockerfile
- create Pipfile

If you get stuck, feel free to refer to the solution. To setup pipenv, run the command:

```
pipenv install
```

Don't forget to build and push your image afterwards!

## 2) Spawning the Runner From the Backend

Now that we have a runner app, we need to spawn it every time the backend receives a request. Hence the backend needs to have the yaml file of the runner to create it, and we need a way to access cluster commands from within the backend app. Like kubectl, there is a client for python called the [Kubernetes python client](https://github.com/kubernetes-client/python). We can use this client to handle the logic for spawning a [Kubernetes job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) in-cluster. 

We can start by creating the yaml file for the runner.

```
mkdir apps/backend/runners
```

```
touch apps/backend/runners/job-experiment.yaml
```

Within the yaml file, we want to put the following logic:

```
apiVersion: batch/v1
kind: Job
metadata:
  name: runner-experiment
spec:
  template:
    metadata:
      labels:
        app: gmini
    spec:
      containers:
      - name: runner
        image: <your dockerhub username>/gmini-runner:latest
        command: []
      restartPolicy: Never
  backoffLimit: 4
  ttlSecondsAfterFinished: 60
```

Note that ttl stands for "time to live". Hence it will persist for a full minute after completion. Feel free to change this if you want more time to debug.

Next, we need to create a new module that will handle spawning k8s objects for us. 

```
mkdir apps/backend/modules
```

```
touch apps/backend/modules/runner.py
```

Separating the logic into a module will allow for cleaner code. Paste the following code into the runner.py script.

```
import time
import yaml
import json
from kubernetes import client, config

config.load_incluster_config()
BATCH_V1_API = client.BatchV1Api()

def create_job(json_data, path):
    job_body = create_runner_body(json_data, path)

    BATCH_V1_API.create_namespaced_job(
        body=job_body,
        namespace="default"
    )

def create_runner_body(json_data, path):
    job_name = 'runner-' + str(time.time())
    job_command = ["python3", "app.py", json.dumps(json_data)]

    job_body = get_yaml_file_body(path)

    job_body['metadata']['name'] = job_name
    job_body['spec']['template']['spec']['containers'][0]['command'] = job_command

    return job_body

def get_yaml_file_body(file_path):
    body = None
    with open(file_path, encoding="utf-8") as yaml_file:
        body = yaml.safe_load(yaml_file)
    return body
```

Note that the config loads the in-cluster config at the top. This config will allow us to spawn within the cluster. Its also worthwhile to mention that the use of the yaml file can be avoided and we can create a job via the Kubernetes python client. However, we found it to have less examples and more messy so we stuck with loading the yaml file as the base body. Also note the way we run the command:

```
job_command = ["python3", "app.py", json.dumps(json_data)]
```

is equivalent to

```
python3 app.py <The JSON Object>
```

Lastly we want to modify the app.py file to include the module and to spawn the runner when the /experiment endpoint is invoked. Try doing this yourself! As a hint, you might want to have an executor handle calling the spawn runner command so that the frontend doesn't timeout:

```
from concurrent.futures import ProcessPoolExecutor
```
```
executor.submit(spawn_runner_experiment, data)
```
Lastly don't forget to include te Kubernetes python client in your Pipfile!

```
cd apps/backend
```

```
pipenv install kubernetes~=29.0.0
```

Don't forget to build and push your image afterwards!

## 3) In-Cluster Spawning Permissions

Unfortunately, you're not done here. We need to setup cluster permissions to allow you to create jobs within cluster. Lets make a directory for the the permissions:

```
mkdir k8s/runner
```

```
touch cluster-role.yaml
```
```
touch rose-binding.yaml
```

A [kubernetes cluster role](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) contains the permissions you want to give. In this case, we want to give permissions to create jobs:

```
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: job-creator
rules:
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["create"]
```

A [cluster role binding](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) applies the role to a user or a group. To make things easy, let's apply it to the service account:

```
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: job-creator
  namespace: default
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: ClusterRole
  name: job-creator
  apiGroup: rbac.authorization.k8s.io
```
We're now done with setting it up! Don't forget to apply your new backend, cluster role, and role binding. We don't need to apply the runner since it will spawn via the backend.
