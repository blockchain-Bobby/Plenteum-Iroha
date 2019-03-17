from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    account_id = StringField('Username @ Domain',validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    remember = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    ple_key = StringField('PLe Public Address',validators=[DataRequired])
    domain = StringField('Domain Name')
    register = SubmitField('Register')

class NewAssetForm(FlaskForm):
    asset_name = StringField('Asset Name',validators=[DataRequired])
    domain = StringField('Domain',validators=[DataRequired])
    description = StringField('Asset Description',validators=[DataRequired])
    precision = IntegerField('Decimal Points')
    qty = StringField('Total Supply')
    
class TransferAssetForm(FlaskForm):
    account_id = StringField('Username @ Domain',validators=[DataRequired])
    asset_name = StringField('Asset Name',validators=[DataRequired])
    domain = StringField('Domain',validators=[DataRequired])
    description = StringField('Asset Description',validators=[DataRequired])
    private_key = StringField('Private Key',validators=[DataRequired])
    precision = IntegerField('Decimal Points')
    qty = StringField('Total Supply')
 