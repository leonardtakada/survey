import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("email") or not request.form.get("password"):
        return render_template("error.html", message="Please Fill Out the Missing Fields")
    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["email", "password", "address", "address2", "city", "state", "zip", "gender", "pet"])
        writer.writerow({"email": request.form.get("email"), "password": request.form.get("password"), "address": request.form.get("address"), "address2": request.form.get("address2"), "city": request.form.get("city"), "state": request.form.get("state"), "zip": request.form.get("zip"), "gender": request.form.get("gender"), "pet": request.form.get("pet")})
    return redirect("/sheet")

@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return render_template("sheet.html", data=data)