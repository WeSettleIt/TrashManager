from datetime import datetime

from flask import Flask, g, render_template, request, url_for, redirect, session
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
        'customers': db_helper.query('SELECT * FROM customers ORDER BY name'),
        'message': session.get('message'),
        'error': session.get('error')
    }

    print(context)

    return render_template('index.html', **context)


@app.route("/customers")
def get_customers():
    customers = db_helper.query('select * from customers')
    return str(customers)


@app.route("/report", methods=['POST'])
def report():
    customer_id = request.form['customer-id']
    units = request.form['units']

    if customer_id and units:
        db_helper.query('INSERT INTO reports (customer_id, units, datetime) VALUES (?, ?, CURRENT_TIMESTAMP)', [customer_id, units])
        customer_name = db_helper.query('SELECT name FROM customers WHERE id = ?', [customer_id])[0].get('name')
        session['message'] = "Added %s units to %s" % (units, customer_name)
        return redirect(url_for('index'))
    else:
        session['error'] = "Both customer and units must be chosen"
        return redirect(url_for('index'))


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
