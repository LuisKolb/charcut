from flask import Flask, render_template
from datetime import datetime
import re

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/result")
def hello_there(charcut_output):

    return 'test'

if __name__ == '__main__':
	app.run()