from flask import render_template

from map_mason import app


@app.route('/')
def index():
    # app.logger.warning('Hit index')
    return render_template('index.html')
