from src.models.light_fm import light_fm, evaluate, pred_i
from src.data.model_preprocessing import get_data
import os
from flask import send_from_directory
from src.app.register import register_user, update_preferences
from flask import Flask, render_template, redirect, url_for, session, g, request
from src.app.forms import RegistrationForm, LoginForm, WorkoutInformation
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import json
import pandas as pd
from src.app.recommendations import create_rec_lists, get_rec_sorted

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

    rec_engine = request.form.get("engine")
    if rec_engine is None:
        return render_template("recommendation_page.html", rec_engine=None, rec_dct=None)

    # get prediction and scores based on chosen model
    if rec_engine == "random":
        query = "SELECT workout_id, RAND() as score FROM fbworkouts_meta ORDER BY score"
        results = pd.read_sql_query(query, db.connection)
        pred, scores = list(results.iloc[:,0]), list(results.iloc[:,1])
    elif rec_engine == "toppop":
        query = """
                SELECT workout_id, COUNT(workout_id) AS score
                FROM workout.user_item_interaction
                GROUP BY workout_id
                ORDER BY 2 DESC
                """
        results = pd.read_sql_query(query, db.connection)
        pred, scores = list(results.iloc[:,0]), list(results.iloc[:,1])
    else:
        uii = pd.read_sql_query(
            "SELECT * FROM user_item_interaction", db.connection)
        data = get_data(uii)
        pred, scores = pred_i(data, 69) # TODO: replace 69 with g.user.user_id

    # dct for predictions to scores
    pred_scores = {pred[i]:scores[i] for i in range(len(pred))}

    # get fbworkouts dataframe
    query = "SELECT * FROM fbworkouts"
    results = pd.read_sql_query(query, db.connection)

    # dictionary with keys as body focus and values as filtered list of workouts
    pred_dct = create_rec_lists(results, g.user)

    # dictionary with keys as body focus and values as dataframes with
    # fb_workouts_meta schema and rows sorted by scores
    rec_dct = {}
    for body_focus in pred_dct.keys():
        query = "SELECT * FROM fbworkouts_meta WHERE workout_id IN (" + str(pred_dct[body_focus])[1:-1] + ")"
        results = get_rec_sorted(pd.read_sql_query(query, db.connection), pred_scores)
        rec_dct[body_focus.replace('_',' ').capitalize().replace('b','B')] = results
    return render_template("recommendation_page.html", rec_engine=rec_engine, rec_dct=rec_dct)

@app.route('/update', methods=['GET', 'POST'])
def update():
    form = WorkoutInformation()
    if form.validate_on_submit(): # update user table based on form inputs
        cur = db.connection.cursor()
        cur.execute(*update_preferences(form, g.user.user_id))
        db.connection.commit()
        cur.close()
        return redirect(url_for('recommendation_page'))

    # create dictionary from user series in order to prepopulate form with previous preferences
    user_dct = g.user[['equipment','training_type','min_duration','max_duration','min_calories',
                            'max_calories','min_difficulty','max_difficulty']].to_dict()
    for k,v in user_dct.items():
        if type(v)!=str:
            user_dct[k] = int(v)
    return render_template('update_workout_info.html', form=form, user=user_dct)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
