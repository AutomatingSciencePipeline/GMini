from concurrent.futures import ProcessPoolExecutor
from flask import Flask, Response, request
from modules.runner import create_job
import sys
flaskApp = Flask(__name__)

PATH_RUNNER_EXP = './runners/job-experiment.yaml'

MAX_WORKERS = 10
executor = ProcessPoolExecutor(MAX_WORKERS)

@flaskApp.route("/")
def hello_world():
    return Response(status=200)

@flaskApp.post("/experiment")
def recv_experiment():
    data = request.get_json()
    if _check_request_integrity(data):
        print(data, file=sys.stderr)
        executor.submit(spawn_runner_experiment, data)
        return Response(status=200)
    print("ERROR: Spawning Experiment Runner Invalid Data", file=sys.stderr)
    return Response(status=400)

def spawn_runner_experiment(data):
    create_job(data, PATH_RUNNER_EXP)

def _check_request_integrity(data):
    try:
        return data['experiment']['id'] is not None
    except KeyError:
        return False
    
if __name__ == "__main__":
    flaskApp.run()