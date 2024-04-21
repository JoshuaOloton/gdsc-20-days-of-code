from . import web
from flask import render_template

@web.route('/index', methods=['GET'])
def index():
    return render_template('index.html')