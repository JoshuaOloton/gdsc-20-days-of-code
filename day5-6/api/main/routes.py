from . import main
from flask import jsonify

@main.route("/")
def index():
    return "Index Route"

@main.route("/hello")
def html():
    return "<p><b>Hello, GDSC</b></p>"

@main.route("/api/hello")
def json():
    return jsonify({"message": "Hello GDSC"})