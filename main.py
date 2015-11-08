from datetime import datetime

from flask import Flask, render_template
from flask.ext.babel import Babel, format_datetime

app = Flask(__name__)
app.config.from_pyfile('trash-manager.cfg')
babel = Babel(app)

app.jinja_env.filters['datetime'] = format_datetime


@app.route("/")
def index():
    context = {
        'timestamp': datetime.now()
    }

    return render_template('index.html', **context)


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
