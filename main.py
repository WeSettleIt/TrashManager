from datetime import datetime

from flask import Flask, g, render_template
from flask.ext.babel import Babel, format_datetime
import db_helper

app = Flask(__name__)
app.config.from_pyfile('trash-manager.cfg')
babel = Babel(app)

app.jinja_env.filters['datetime'] = format_datetime


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    context = {
        'timestamp': datetime.now(),
        'customers': db_helper.query('SELECT * FROM customers ORDER BY name')
    }

    return render_template('index.html', **context)


@app.route("/customers")
def get_customers():
    customers = db_helper.query('select * from customers')
    return str(customers)


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
