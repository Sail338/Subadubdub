from flask import Flask,render_template, request, redirect, url_for, make_response, jsonify
from threading import Thread
from .. import workflow as wf
import os
from pathlib import Path
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
@app.route("/workflow",methods=['POST'])
def workflow():
    mp4input = "input.mp4"
    script = "script.txt"
    lang_ = "de"
    thread = Thread(target = wf.begin_workflow,args = [mp4input,script,lang_]) 
    thread.start()
    data = {"resp":"final.mp4"}
    return jsonify(data)
    
@app.route("/poll")
def poll():
    my_file = Path("../final.mp4")
    if not my_file.exists():
        resp = {"resp":"Nah"}
        return jsonify(resp)
    else:
        resp = {"resp":"Yeet"}
        return jsonify(resp)
    
    


if __name__ == '__main__':
    app.run(debug = True)
