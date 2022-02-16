from flask import Flask
from flask import render_template, request, url_for, redirect, Response
from lib.db_initializer import extract_head
from lib.db_initializer import init
from lib.main import stream
import functions.json_tools as jt

#https://flask.palletsprojects.com/en/2.0.x/quickstart/

app = Flask(__name__)

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
        #print("Affichage des commandes possibles : \n")
        #print(request.form.getlist("affectedCommands")[0])
        #print("\n")

        #jt.save_config("", "", "")
        jt.save_config(dictStringCommand, dictStringFigure, dictStringAffectation)
        return render_template('config.html')
    else:
        init()
        datas = extract_head()
        return render_template('config.html',datas=datas)

@app.route('/video_feed')
def video_feed():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/list')
def list():
    init()
    datas = extract_head()
    print("Datas :" ,datas, "\n")
    return render_template('list.html',datas=datas)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000) #port > 5000 under linux to avoid sudo

