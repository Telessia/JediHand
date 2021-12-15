from flask import Flask
from flask import render_template, request, url_for, redirect
import functions.json_tools as jt

#https://flask.palletsprojects.com/en/2.0.x/quickstart/

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/config/", methods=['GET','POST'])
def config():
    if request.method == 'POST':
        datas = request.form
        app.logger(datas)
        return jt.save_config(datas)
    else:
       # datas = jt.load_config()
        return render_template("config.html")#, datas)

