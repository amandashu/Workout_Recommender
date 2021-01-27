from flask import Flask, render_template, redirect, url_for, session, g
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import json

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
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = %s",
                    (session['user_id'],))
        g.user = cur.fetchone()
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

            # insert string of available equipment, else empty string
            if form.no_equipment.data == False:
                equipment_string = str(form.equipment.data)[
                    1:-1].replace('\'', '')
            else:
                equipment_string = ''

            # insert string of preferred training types, else have all types
            if form.no_training_type.data == False:
                training_type_string = str(form.training_type.data)[
                    1:-1].replace('\'', '')
            else:
                training_type_string = str([x[0] for x in form.training_type.choices])[
                    1:-1].replace('\'', '')

            # get next user id
            cur.execute("SELECT MAX(user_id) FROM users")
            result = cur.fetchone()[0]
            if result is None:
                user_id = 5000  # fbcommenters end with id 4026, our users will start from 5000
            else:
                user_id = result + 1

            # insert into data base
            cur.execute("""
                        INSERT INTO users(user_id, name, email, password, equipment,
                        training_type, min_duration, max_duration, min_calories,
                        max_calories) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (user_id, form.name.data, form.email.data, hashed_password,
                         equipment_string, training_type_string, form.min_duration.data,
                         form.max_duration.data, form.min_calories.data,
                         form.max_calories.data)
                        )
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
            else:  # login
                # set session to logged in user's id
                session['user_id'] = result[0]
                return redirect(url_for('recommendation_page'))
        cur.close()

    return render_template('login_page.html', form=form)


@app.route('/')
def recommendation_page():
    # if user is not logged in, redirect to login page
    if g.user is None:
        # form = LoginForm()
        # return render_template('login_page.html', form=form)
        return redirect(url_for('login_page'))

    cur = db.connection.cursor()
    query = cur.execute(
        "SELECT * FROM fbworkouts_meta ORDER BY RAND() LIMIT 10")
    results = cur.fetchall()

    return render_template('recommendation_page.html', workouts=results)


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


if __name__ == '__main__':
    app.run(debug=True)
