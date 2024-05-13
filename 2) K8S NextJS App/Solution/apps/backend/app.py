from flask import Flask, Response
flaskApp = Flask(__name__)

@flaskApp.route("/")
def hello_world():
    return Response(status=200)
    
if __name__ == "__main__":
    flaskApp.run()