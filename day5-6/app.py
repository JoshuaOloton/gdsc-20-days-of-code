from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from api import create_app, db
from api.models import Book


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

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Book=Book)

@app.cli.command("db_create")
def db_create():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=3000)