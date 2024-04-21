from flask import jsonify, send_from_directory, render_template
from app.api import create_app, db
from app.api.models import Book, User, Role


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

@app.route("/static/<path:filename>")
def send_static_file(filename):
    return send_from_directory('static', filename)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Book=Book, User=User, Role=Role)

@app.cli.command("db_create")
def db_create():
    db.create_all()
    Role.insert_roles()

@app.cli.command("db_drop")
def db_create():
    db.drop_all()


if __name__ == "__main__":
    app.run(debug=True, port=3000)