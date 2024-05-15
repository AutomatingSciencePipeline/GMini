# 4) In-Cluster Job
## 1) Create a Simple Runner App

- create app.py script
 - Make sure that the app.py script can take an argument and print it out
- create Pipfile
- create Dockerfile

```
pipenv install
```

## 2) Spawning the Runner From the Backend

- create a yaml file for the runner
- create a new python module
- modify app.py

```
pipenv install kubernetes~=29.0.0
```

## 3) In-Cluster Spawning Permissions

- cluster role
- cluster role binding
