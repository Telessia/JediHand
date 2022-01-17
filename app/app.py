from re import M
from flask import Flask
from flask import render_template, request, url_for, redirect, Response
from backend.main import stream
import functions.json_tools as jt

#https://flask.palletsprojects.com/en/2.0.x/quickstart/

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
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

    return render_template("index.html")

@app.route('/streaming')
def streaming():
    return render_template('streaming.html')

@app.route('/video_feed')
def video_feed():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

