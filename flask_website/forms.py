from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])

    equipment = SelectMultipleField('My Available Equipment', choices=[
        ('barbell','Barbell'), ('bench','Bench'), ('dumbbell','Dumbbell'),
        ('exercise_band','Exercise Band'), ('jump_rope','Jump Rope') ,
        ('Kettlebell','kettlebell'), ('mat','Mat'), ('medicine_ball','Medicine Ball'),
        ('physioball','Physioball'), ('no_equipment', 'No Equipment'),
        ('sandbag','Sandbag'), ('stationary_bike','Stationary Bike')
    ], validators=[DataRequired()])

    min_duration = IntegerField('Min Duration',
                    validators=[DataRequired(), NumberRange(1,120)]) # fb workout between 3-96 minutes
    max_duration = IntegerField('Max Duration',
                    validators=[DataRequired(), NumberRange(1,120)])

    min_calories = IntegerField('Min Calories',
                    validators=[DataRequired(), NumberRange(1,1300)]) # fb workouts between 12-260 calori burn
    max_calories = IntegerField('Max Calories',
                    validators=[DataRequired(), NumberRange(1,1300)])

    submit = SubmitField('Register')

    def validate_max_duration(form, field):
        if field.data < form.min_duration.data:
            raise ValidationError('Min Duration must be less than Max Duration')

    def validate_max_calories(form, field):
        if field.data < form.min_calories.data:
            raise ValidationError('Min Calories must be less than Max Calories')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
