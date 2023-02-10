from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/compare", methods=['POST'])
def compare():
    cand = request.form['cand']
    ref = request.form['ref']

    with open('temp/cand.txt', 'w') as f_cand:
        f_cand.write(cand)
    
    with open('temp/ref.txt', 'w') as f_ref:
        f_ref.write(ref)

    os.system(f'python charcut.py -o templates/out.html temp/cand.txt,temp/ref.txt -n')

    return render_template('out.html')
