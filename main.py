from datetime import datetime

from flask import Flask, g, render_template, request, url_for, redirect, session
from flask.ext.babel import Babel, format_datetime
import db_helper
import flask.ext.login as flask_login

users = {'foo@bar.tld': {'pw': 'secret'}}

app = Flask(__name__)

app.config.from_pyfile('trash-manager.cfg')
babel = Babel(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.jinja_env.filters['datetime'] = format_datetime


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/customers")
def get_customers():
    customers = db_helper.query('SELECT * FROM customers')
    return str(customers)


@app.route("/report", methods=['GET', 'POST'])
def report():
    if request.method == 'GET':
        context = {
            'timestamp': datetime.now(),
            'customers': db_helper.query('SELECT * FROM customers ORDER BY name'),
            'message': session.pop('message') if 'message' in session else None,
            'error': session.pop('error') if 'error' in session else None
        }

        return render_template('report-create.html', **context)

    customer_id = request.form['customer-id']
    units = request.form['units']

    if customer_id and units:
        db_helper.execute('INSERT INTO reports (customer_id, units, datetime) VALUES (?, ?, CURRENT_TIMESTAMP)', [customer_id, units])
        customer_name = db_helper.query('SELECT name FROM customers WHERE id = ?', [customer_id])[0].get('name')
        session['message'] = "Added %s units to %s" % (units, customer_name)
        return redirect(url_for('index'))
    else:
        session['error'] = "Both customer and units must be chosen"
        return redirect(url_for('index'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if users.get(email):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return render_template('login.html', error="User does not exist")


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    render_template('login.html', error="User does not exist")


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

@app.route('/reports', methods=['GET', 'POST'])
@flask_login.login_required
def protected():
    context = {
        'customers': db_helper.query('SELECT * FROM customers ORDER BY name')
    }
    if request.method == 'GET':
        return render_template('report-list.html', **context)

    customer_id = request.form['customer-id']
    context['reports'] = db_helper.query('SELECT * FROM reports WHERE customer_id = ? ORDER BY datetime DESC', [customer_id])
    meta = db_helper.query('SELECT COUNT(1) AS count, SUM(units) as total FROM reports WHERE customer_id = ?', [customer_id])[0]
    context['total'] = meta.get("total")
    context['count'] = meta.get("count")

    return render_template('report-list.html', **context)


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
