from flask import Flask,render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.wrappers import Request, Response
from threading import Thread
import sys
sys.path.append("..")
import workflow as wf
import os
from pathlib import Path
app = Flask(__name__,static_folder ='static')

@app.route("/")
def hello():
    return render_template("index.html")
@app.route("/workflow",methods=['POST','GET'])
def workflow():
    mp4input = "parksandrec.mp4"
    script = "script.txt"
    lang_ = "de"
    thread = Thread(target = wf.begin_workflow,args = [script,mp4input,lang_]) 
    thread.start()
    return render_template("display.html")
    
@app.route("/poll")
def poll():
    my_file = Path("static/final.mp4")
    if not my_file.exists():
        resp = {"resp":"nah"}
        return jsonify(resp)
    else:
        resp = {"resp":"yeet"}
        return jsonify(resp)
 
@app.route('/display')
def display():
    source_1 =  "static/parksandrec.mp4"
    source_2 = "static/final.mp4"
    return render_template("display.html",iframe1 = source_1, iframe2 = source_2)

if __name__ == '__main__':
    app.run(debug = True)
