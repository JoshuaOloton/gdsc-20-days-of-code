from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from api import create_app

app = create_app()

@app.route("/")
def index():
    return "Index Route"

@app.route("/hello")
def html():
    return "<p><b>Hello, GDSC</b></p>"

@app.route("/api/hello")
def json():
    return jsonify({"message": "Hello GDSC"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)