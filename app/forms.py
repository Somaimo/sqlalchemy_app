# app/forms.py
from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class NewGameForm(FlaskForm):
    homeTeam = SelectField('Home Team', validate_choice=False)
    visitorTeam = SelectField('Visitor Team', validate_choice=False)
    date = DateTimeField('Game date', format='%Y-%m-%d')
    result = StringField('Result (Format Home:Visitor)', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_homeTeam(form, self):
        if self.data == form.visitorTeam.data:
            raise ValidationError('Visitor and Home Teams cannot be the same.')


