from flask import Flask, render_template, request
import argparse
from charcut import run_on, load_input_files
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html", error_message=str(error)), 500


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(400)
def not_found(error):
    return render_template("400.html"), 400


@app.route("/compare", methods=["POST"])
def compare():
    if "cand" not in request.form or "ref" not in request.form:
        return render_template("error.html", error_message="Missing candidate or reference text"), 400

    # detect if /tmp directory exists, if not create a substitute
    # workaround for Windows where /tmp does not exist
    if not os.path.exists("/tmp"):
        os.makedirs("./.tmp", exist_ok=True)
        base_fp = "./.tmp"
    else:
        base_fp = "/tmp"

    if "source" in request.form:
        src_fp = os.path.join(base_fp, "source.txt")
        with open(src_fp, "w", encoding="utf-8") as f_ref:
            f_ref.write(request.form["source"])
    else:
        src_fp = None

    if "matchSize" in dict.keys(request.form):
        matchSize = int(request.form["matchSize"])
    else:
        matchSize = 3

    if "altNorm" in dict.keys(request.form):
        altNorm = request.form["altNorm"] == "on"
    else:
        altNorm = True

    # Create temporary files to hold the candidate and reference texts
    cand_fp = os.path.join(base_fp, "candidate_machine.txt")
    ref_fp = os.path.join(base_fp, "reference_human.txt")

    cand = request.form["cand"]
    ref = request.form["ref"]

    if len(ref.splitlines()) < len(cand.splitlines()):
        # extend the reference with empty lines to match the candidate
        ref += "\n" * (len(cand.splitlines()) - len(ref.splitlines()))
    elif len(cand.splitlines()) < len(ref.splitlines()):
        # extend the candidate with empty lines to match the reference
        cand += "\n" * (len(ref.splitlines()) - len(cand.splitlines()))

    with open(cand_fp, "w", encoding="utf-8") as f_cand:
        f_cand.write(cand)

    with open(ref_fp, "w", encoding="utf-8") as f_ref:
        f_ref.write(ref)

    args = argparse.Namespace(
        file_pair=[f"{cand_fp},{ref_fp}"], src_file=src_fp, echo_string=True, match_size=matchSize, alt_norm=altNorm
    )
    output_string = run_on(load_input_files(args), args)

    return render_template("compare.html", table=output_string)
