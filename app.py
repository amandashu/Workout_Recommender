from flask import Flask, render_template, redirect, url_for, session, g, request
from src.app.forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import json
import pandas as pd
from src.app.recommendations import filter

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

db_config = json.load(open('./config/db_config.json'))

app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

db = MySQL(app)
bcrypt = Bcrypt(app)


@app.before_request
def before_request():
    if 'user_id' in session:
        query = "SELECT * FROM users WHERE user_id = " + str(session['user_id'])
        results = pd.read_sql_query(query , db.connection)
        g.user = results.iloc[0]
    else:
        g.user = None


from src.app.register import register_user
@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        cur = db.connection.cursor()

        # check if email already exists in database
        cur.execute("SELECT email FROM users WHERE email = %s",
                    (form.email.data,))
        result = cur.fetchone()
        if result is not None:  # display error
            return render_template('registration_page.html', form=form, email_error=True)
        else:  # insert user into database
            # hash the password
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')

            # get next user id
            cur.execute("SELECT MAX(user_id) FROM users")
            result = cur.fetchone()[0]
            if result is None:
                user_id = 5000  # fbcommenters end with id 4026, our users will start from 5000
            else:
                user_id = result + 1

            cur.execute(*register_user(form, user_id, hashed_password))
            db.connection.commit()
            return redirect(url_for('login_page'))
        cur.close()
    return render_template('registration_page.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        cur = db.connection.cursor()

        # check if login information is correct
        cur.execute("SELECT * FROM users WHERE email = %s", (form.email.data,))
        result = cur.fetchone()

        if result is None:  # display error if email doesn't exist
            return render_template('login_page.html', form=form, email_error=True)
        else:  # check password
            db_password = result[3]
            pw_match = bcrypt.check_password_hash(
                db_password, form.password.data)

            if not pw_match:  # display error if password doesn't match
                return render_template('login_page.html', form=form, password_error=True)
            else:  # login, set session to logged in user's id
                session['user_id'] = result[0]
                return redirect(url_for('recommendation_page'))
        cur.close()

    return render_template('login_page.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def recommendation_page():
    # if user is not logged in, redirect to login page
    if g.user is None:
        return redirect(url_for('login_page'))

    # # the model's predictions (list of workout_id)
    # query = "SELECT workout_id FROM fbworkouts ORDER BY RAND() LIMIT 10"
    # model_predictions = list(pd.read_sql_query(query , db.connection)['workout_id'])
    #
    # # get the workouts df for the predicted workouts
    # query = "SELECT * FROM fbworkouts WHERE workout_id in (" + str(model_predictions)[1:-1] +")"
    # workouts = pd.read_sql_query(query , db.connection)
    #
    # # filter for user preferences and split into recommentation lists for each body focus
    # dct = filter(workouts, g.user)
    # lst = [] # list of lists, where each list is recommendations for a body focuz
    # for values in dct.values():
    #     query = "SELECT * FROM fbworkouts_meta WHERE workout_id in (" + str(values)[1:-1] + ')'
    #     list.append(pd.read_sql_query(query , db.connection))

    if request.method == "POST":
        rec_engine = request.form.get("engine", "random")
    else:
        rec_engine = request.form.get("engine", "what")

    print(rec_engine)
    if rec_engine == "random":
        query = "SELECT * FROM fbworkouts_meta ORDER BY RAND() LIMIT 10"
    else:
        query = "SELECT * FROM fbworkouts_meta ORDER BY RAND() LIMIT 0"

    results = pd.read_sql_query(query, db.connection)
    return render_template("recommendation_page.html", engine = rec_engine, workouts=results)



@app.route('/logout')
def logout():
    session.pop('user_id', None)  # removes session if currently in one
    return redirect(url_for('login_page'))


@app.route('/about')
def about_page():
    return render_template('about_page.html')


@app.route('/contact')
def contact_page():
    return render_template('contact_page.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

import os
from flask import send_from_directory

if __name__ == '__main__':
    app.run(debug=True)
