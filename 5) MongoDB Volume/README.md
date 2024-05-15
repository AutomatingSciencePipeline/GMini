# 5) MongoDB Volume
## 1) Create Secrets

```
mkdir k8s/secrets
```

## 2) Setting up the MongoDB Persistent Volume

You're almost done with the GLADOS architecture! The last major piece to the puzzle is the MongoDB integration. In the latest version of GLADOS, MongoDB is responsible for containing all the information on the experiments. First, try creating the service for MongoDB by yourself. I suggest you use port 25000 and name it gmini-mongodb.

```
mkdir k8s/mongodb
```

```
touch k8s/mongodb/service.yaml
```

[Storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) are similar to profiles for storage systems. Since we're running locally we need to create a local storage class.

```
touch k8s/mongodb/storage-class.yaml
```

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

Next create a [persistent volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). The persistent volume will define how the volume is accessed and the amount of storage that is delegated to the volume. 

```
touch k8s/mongodb/persistent-volume.yaml
```

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: persistent-volume
spec:
  storageClassName: local-storage
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  hostPath:
    path: "/data/mongo"
```

[Persistent volume claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) are requests for persistent volumes.

```
touch k8s/mongodb/persistent-volume-claim.yaml
```

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: persistent-volume-claim
  labels:
    app: gmini
spec:
  storageClassName: local-storage
  accessModes:
    - ReadWriteOnce 
  volumeName: persistent-volume
  resources:
    requests:
      storage: 1Gi
```

## 3) Create Secrets for the MongoDB Username and Password

[Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/) are used to pass sensitive data to pods. Ideally, we would've already used secrets on our port numbers, as the less information revealed about our network the better. Regardless, we need to hide the username and password for our MongoDB setup.

```
mkdir k8s/secrets
```

```
touch k8s/secrets/secret.yaml
```

Place the following code within the yaml file


```
apiVersion: v1
kind: Secret
metadata:
  name: secret-env
  namespace: default
  labels:
    app: gmini
data:
  MONGODB_USERNAME: YWRtaW51c2Vy
  MONGODB_PASSWORD: cGFzc3dvcmQxMjM=
```

As seen with the username and password, secrets are encoded in base64. To encode something in base64, run:

```
echo -n <insert plain text> | base64
```

## 4) Create the MongoDB Deployment

```
touch k8s/mongodb/deployment.yaml
```

We can now implement the deployment! 

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gmini-mongodb
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gmini
      tier: database
  template:
    metadata:
      labels:
        app: gmini
        tier: database
    spec:
      containers:
      - image: mongo
        name: mongo
        args: ["--dbpath","/data/db"]
        livenessProbe:
          exec:
            command:
              - mongosh
              - --norc
              - --quiet
              - --eval
              - "db.getMongo()"
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 6
        readinessProbe:
          exec:
            command:
              - mongosh
              - --norc
              - --quiet
              - --eval
              - "db.getMongo()"
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 6
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          valueFrom:
            secretKeyRef:
              name: secret-env
              key: MONGODB_USERNAME
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: secret-env
              key: MONGODB_PASSWORD
        volumeMounts:
        - name: "mongo-data-dir"
          mountPath: "/data/db"
      volumes:
      - name: "mongo-data-dir"
        persistentVolumeClaim:
          claimName: "persistent-volume-claim"
  strategy: {}
```

The base structure of the deployment remains the same. However, now extra detail about the container is added as well as references to the secrets that we have created.

## 5) Check the Connection in the Runner

The last thing we need to do is modify our runner so it can connect to MongoDB. However before we do that we must edit the runner yaml file to contain MongoDB's username and password. 

Within the backend edit runners/job-experiment.yaml to include the secrets similar to how you did it for the MongoDB deployment. Feel free to check out the solution if you get stuck.

Next, we need to add two modules for the runner. One to get environment variables (to consume the secrets) and the second one to connect to mongoDB. 

```
mkdir apps/runner/modules
```

```
touch apps/runner/modules/utils.py
```

```
import os

from dotenv import load_dotenv

# Must override so that vscode doesn't incorrectly parse another env file and have bad values
HAS_DOTENV_FILE = load_dotenv("./.env", override=True)

def _get_env(key: str):
    value = os.environ.get(key)
    if value is None:
        if HAS_DOTENV_FILE:
            raise AssertionError(f"Missing environment variable {key} in your `.env` file")
        raise AssertionError(f"Missing environment variable {key} - you need a `.env` file in this folder with it defined")
    return value

```

```
pipenv install python-dotenv~=1.0.1
```

Since we added the secrets to our runner yaml file, we can now consume them using the external package dotenv. 

```
touch apps/runner/modules/mongodb.py
```

```
import sys
import pymongo

from pymongo.errors import ConnectionFailure
from modules.utils import _get_env

ENV_MONGODB_USERNAME = "MONGODB_USERNAME"
ENV_MONGODB_PASSWORD = "MONGODB_PASSWORD"

mongoClient = pymongo.MongoClient(
    "gmini-mongodb:25000",
    username=_get_env(ENV_MONGODB_USERNAME),
    password=_get_env(ENV_MONGODB_PASSWORD),
    authMechanism='SCRAM-SHA-256',
    serverSelectionTimeoutMS=1000
)
mongoGladosDB = mongoClient["gladosdb"]
    
def verify_mongo_connection():
    global mongoClient
    try:
        mongoClient.admin.command('ping')
    except ConnectionFailure as err:
        print(err, file=sys.stderr)
```

```
pipenv install pymongo~=4.7.2
```

Note that we can format MongoDB's url with the MongoClient method. Additionally it uses the service's name and port, gmini-mongodb:25000, as the connection like we did with the frontend to backend connection. 

We can now verify the connection within the app.py file

```
import sys
import json
from modules.mongodb import verify_mongo_connection

def main(experiment_data: str):
    experiment_id = json.loads(experiment_data)['experiment']['id']
    verify_mongo_connection()
    print("Running Experiment: " + experiment_id, file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("Error: Too few arguments")
    elif len(sys.argv) > 2:
        raise ValueError("Error: Too many arguments")
    main(sys.argv[1])
```

If the runner crashes, then it is not connected.

Don't forget to build and push your backend and runner images! Also, don't forget to apply your new MongoDB and secret yaml files!
You now know the basic components of the GLADOS architecture!
