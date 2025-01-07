from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length

class ToDoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Speichern')


class GradeForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    q1 = IntegerField('Q1', validators=[DataRequired()])
    q2 = IntegerField('Q2', validators=[DataRequired()])
    q3 = IntegerField('Q3', validators=[DataRequired()])
    q4 = IntegerField('Q4', validators=[DataRequired()])
    submit = SubmitField('Add Grade')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrieren')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class ThemeForm(FlaskForm):
    theme = SelectField('Select Theme', choices=[
        ('system', 'System'),
        ('dark', 'Dark'),
        ('light', 'Light')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Changes')