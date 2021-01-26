from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, IntegerField, ValidationError, widgets
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])

    equipment = MultiCheckboxField('My Available Equipment', choices=[
        ('barbell','Barbell'), ('bench','Bench'), ('dumbbell','Dumbbell'),
        ('exercise_band','Exercise Band'), ('jump_rope','Jump Rope') ,
        ('Kettlebell','kettlebell'), ('mat','Mat'), ('medicine_ball','Medicine Ball'),
        ('physioball','Physioball'), ('no_equipment', 'No Equipment'),
        ('sandbag','Sandbag'), ('stationary_bike','Stationary Bike')
    ], validators=[DataRequired()])

    min_duration = IntegerField('Minimum Duration',
                    validators=[DataRequired(), NumberRange(1,120)]) # fb workout between 3-96 minutes
    max_duration = IntegerField('Maximum Duration',
                    validators=[DataRequired(), NumberRange(1,120)])

    min_calories = IntegerField('Minimum Calories',
                    validators=[DataRequired(), NumberRange(1,1300)]) # fb workouts between 12-260 calori burn
    max_calories = IntegerField('Maximum Calories',
                    validators=[DataRequired(), NumberRange(1,1300)])

    submit = SubmitField('Register')

    def validate_max_duration(form, field):
        if field.data < form.min_duration.data:
            raise ValidationError('Minimum Duration must be less than Maximum Duration')

    def validate_max_calories(form, field):
        if field.data < form.min_calories.data:
            raise ValidationError('Minimum Calories must be less than Maximum Calories')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

