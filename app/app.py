from re import template
from flask import Flask
from flask import render_template, request, url_for, redirect, Response, session
from lib.db_initializer import extract_head, init, copyOfTabSkeletons, save_datas
#from lib.main import stream
from lib.capture import stream,shot
import functions.json_tools as jt
import os

#https://flask.palletsprojects.com/en/2.0.x/quickstart/

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/streaming')
def streaming():
    return render_template('streaming.html')


@app.route('/config')
def config():
    if request.method == 'POST':
        
        #On récupère le string du dictionnaire d'affectedCommandsFigure
        dictStringCommand = request.form.getlist("possibleCommands")[0]
        dictStringFigure = request.form.getlist("possibleFigures")[0]
        dictStringAffectation = request.form.getlist("affectedCommands")[0]
        #jt.save_config(dictStringCommand, dictStringFigure, dictStringAffectation)
        
        return render_template('config.html')
    else:
        init()
        datas = extract_head()
        return render_template('config.html',datas=datas)

@app.route('/video_feed')
def video_feed():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    original_path,path,skeleton = shot()
    path = path.split("app/")[1]
    original_path = original_path.split("app/")[1]
    skeleton = copyOfTabSkeletons(skeleton)
    session["original_path"]= original_path
    session["skeleton"] = skeleton
    return render_template('addsign.html',original_path=original_path,path=path,skeleton_data=skeleton)
    #return Response(image)

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/list')
def list():
    init()
    datas = extract_head()
    print("Datas :" ,datas, "\n")
    return render_template('list.html',datas=datas)

@app.route('/save_sign',methods=['GET','POST'])
def save_sign():
    if request.method == 'POST':
        groupname = request.form.get("groupname")
        original_path = session.get("original_path")
        skeleton = session.get("skeleton")
        saved = save_datas(groupname,original_path,skeleton)
        return render_template('streaming.html',saved=saved)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000) #port > 5000 under linux to avoid sudo

