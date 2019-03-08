from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired])
    password = PasswordField('password', validators=[DataRequired])

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    pub_key = StringField('PLe Public Address',validators=[DataRequired])
    register = SubmitField('Register')

class NewAssetForm(FlaskForm):
    asset_name = StringField('Asset Name',validators=[DataRequired])
    domain_name = StringField('Domain',validators=[DataRequired])
    qty = IntegerField('Qty')
    
