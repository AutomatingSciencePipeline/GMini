from flask import Flask, Response, request
import sys
flaskApp = Flask(__name__)

@flaskApp.route("/")
def hello_world():
    return Response(status=200)

@flaskApp.post("/experiment")
def recv_experiment():
    data = request.get_json()
    print(data, file=sys.stderr)
    return Response(status=200)
    
if __name__ == "__main__":
    flaskApp.run()