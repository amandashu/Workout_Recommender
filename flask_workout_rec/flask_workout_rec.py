from flask import Flask, render_template, redirect, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'djkdk33j21hkfvnd'

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
    return render_template('recommendation_page.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
