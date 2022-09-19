from crypt import methods
from flask import Flask, jsonify, make_response
from flask import request

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_from_root():
    return make_response({"message":'Hello from path!',"path":request.path },200)



@app.route("/botList", methods=['GET'])
def hello_from_root():
    return make_response({"message":'Hello from path!',"path":request.path },200)



@app.route("/createBot", methods=['POST'])
def hello():
    assert request.path == '/hello'
    assert request.method == 'POST'
    
    return make_response({"message":'Hello from path!',"path":request },200)




@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
