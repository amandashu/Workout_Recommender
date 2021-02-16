from src.models.light_fm import light_fm, evaluate, pred_i
from src.data.model_preprocessing import get_data
import os
from flask import send_from_directory
from src.app.register import register_user
from flask import Flask, render_template, redirect, url_for, session, g, request
from src.app.forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import json
import pandas as pd
from src.app.recommendations import filter

import sys

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/models')


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
        query = "SELECT * FROM users WHERE user_id = " + \
            str(session['user_id'])
        results = pd.read_sql_query(query, db.connection)
        g.user = results.iloc[0]
    else:
        g.user = None


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
        rec_engine = request.form.get("engine", "random")

    all_user_interactions = pd.read_sql_query(
        "SELECT * FROM workout.user_item_interaction WHERE user_id = " + str(
            session['user_id']), db.connection
    )
    if rec_engine == "random":
        query = "SELECT * FROM fbworkouts_meta ORDER BY RAND() LIMIT 10"
    elif rec_engine == "toppop":
        query = """SELECT *
                FROM workout.fbworkouts_meta
                WHERE workout.fbworkouts_meta.workout_id IN (
                    SELECT TEMP.workout_id
                    FROM
                    (
                        SELECT workout_id, COUNT(workout_id)
                        FROM workout.user_item_interaction
                        GROUP BY workout_id
                        ORDER BY 2 DESC
                        LIMIT 10
                    ) AS TEMP
                )"""
    else:
        uii = pd.read_sql_query(
            "SELECT * FROM user_item_interaction", db.connection)
        data = get_data(uii)

        if len(all_user_interactions) != 0:
            # sort predictions, get last (most relevant) K items, resort
            pred = pred_i(data, session['user_id'])[-10:][::-1]
            query = "SELECT * FROM fbworkouts_meta WHERE workout_id IN (" + str(list(pred))[
                1:-1] + ")"
        else:
            # Cold Start, recommend randomly
            query = "SELECT * FROM fbworkouts_meta ORDER BY RAND() LIMIT 10"

    results = pd.read_sql_query(query, db.connection)
    results['liked'] = results['workout_id'].apply(
        lambda x: x in list(all_user_interactions['workout_id']))

    return render_template("recommendation_page.html", engine=rec_engine, workouts=results)


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


@app.route('/record_like/<user_id>/<workout_id>')
def record_like(user_id, workout_id):
    # "INSERT INTO user_item_interaction (user_id, workout_id) VALUES (" + user_id + ", " + workout_id + ")"
    all_user_interactions = pd.read_sql_query(
        "SELECT * FROM workout.user_item_interaction WHERE user_id = " +
        user_id + " and workout_id = " + workout_id, db.connection
    )

    if len(all_user_interactions) == 0:
        # no such interaction

        cur = db.connection.cursor()
        cur.execute(
            "INSERT INTO workout.user_item_interaction (user_id, workout_id) VALUES (%s, %s);", (int(user_id), int(workout_id)))

        print('recorded like')
    else:
        cur = db.connection.cursor()
        cur.execute(
            "DELETE FROM workout.user_item_interaction WHERE user_id = %s and workout_id = %s;", (int(user_id), int(workout_id)))

        print('already liked!')

    cur.connection.commit()
    return user_id + " " + workout_id


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
