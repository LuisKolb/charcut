from flask import Flask, render_template, render_template_string, request
import argparse
from charcut import run_on, load_input_files

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

    with open('/tmp/cand.txt', 'w') as f_cand:
        f_cand.write(cand)
    
    with open('/tmp/ref.txt', 'w') as f_ref:
        f_ref.write(ref)

    args = argparse.Namespace(file_pair=['/tmp/cand.txt,/tmp/ref.txt'], src_file=None, match_size=3, alt_norm=True, echo_string ='1')
    output_string = run_on(load_input_files(args), args)

    #return render_template_string(output_string)
    return render_template('compare.html', table=output_string)
