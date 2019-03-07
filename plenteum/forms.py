from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class OrderForm(FlaskForm):
    productList = SelectField('productDescription') 
    contactNo = IntegerField('Contact No')
    confirmOrder = SubmitField('confirm')
    pub_key = StringField('wallet address')

class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired])
    password = PasswordField('password', validators=[DataRequired])

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    pub_key = StringField('TRTL Public Address',validators=[DataRequired])
    register = SubmitField('Register')