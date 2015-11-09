from datetime import datetime

from flask import Flask, g, render_template, request, url_for, redirect, session
from flask.ext.babel import Babel, format_datetime
import db_helper
import flask.ext.login as flask_login

app = Flask(__name__)

app.config.from_pyfile('config.py')
app.config.from_envvar('TRASHMANAGER_SETTINGS', silent=True)
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
        return redirect(url_for('report'))
    else:
        session['error'] = "Both customer and units must be chosen"
        return redirect(url_for('report'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    user = user_loader(email)
    if user:
        flask_login.login_user(user)
        return redirect(user.get_default_page())

    return render_template('login.html', error="User does not exist")


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    render_template('login.html', error="User does not exist")


class User(flask_login.UserMixin):
    role = None

    def get_default_page(self):
        if self.role == 3:
            return url_for('report')
        else:
            return url_for('protected')

    def can_administrate(self):
        return True if self.role in [0] else False

    def can_create_report(self):
        return True if self.role in [0, 3] else False

    def can_list_reports(self):
        return True if self.role in [0, 1, 2] else False

    def can_list_all_reports(self):
        return True if self.role in [0, 1] else False

    def can_list_own_reports(self):
        return True if self.role in [2] else False

    def can_collect_money(self):
        return True if self.role in [0, 4] else False

    pass


@login_manager.user_loader
def user_loader(email):
    db_user = db_helper.query('SELECT * FROM users WHERE username = ?', [email], one=True)
    if not db_user:
        return

    user = User()
    user.id = db_user.get('username')
    user.role = db_user.get('role')
    user.customer_id = db_user.get('customer_id')
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = user_loader(email)
    if not user:
        return

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = True

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
