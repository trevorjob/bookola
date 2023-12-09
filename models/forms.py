from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class ResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    # password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm  Password', validators=[DataRequired()])
    submit = SubmitField(label='Change Password')