from flask import Flask, render_template, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

db_config = json.load(open('./db_config.json'))

app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)

# dummy_data
data = [
    {
        'name': "Daniel's Upper Body...",
        #'calorie':
        #'duration': 39
        #'difficulty':,
        #'equipment':
        #'training type'
    },
    {
        'name': "HIIT Pilates Strength...",
    }

]

@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('recommendation_page'))
    return render_template('registration_page.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('recommendation_page'))
    return render_template('login_page.html', form=form)

@app.route('/')
def recommendation_page():
    fake_model_results = [1,2,3,4,5,6,7,8]

    cur = mysql.connection.cursor()
    query = cur.execute("SELECT workout_id, workout_title FROM fbworkouts_meta")
    results = cur.fetchall()
    return render_template('recommendation_page.html', workouts=results)

@app.route('/about')
def about_page():
    return render_template('about_page.html')

@app.route('/contact')
def contact_page():
    return render_template('contact_page.html')

if __name__ == '__main__':
    app.run(debug=True)
