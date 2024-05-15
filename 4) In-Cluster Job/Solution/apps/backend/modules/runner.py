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
