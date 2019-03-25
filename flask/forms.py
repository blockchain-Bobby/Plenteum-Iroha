from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    account_id = StringField('Username @ Domain',validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    remember = BooleanField('Remember Me')

class UserRegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    domain = StringField('Domain Name')
    register = SubmitField('Register')

class DomainRegistrationForm(FlaskForm):
    domain = StringField('Domain Name')
    register = SubmitField('Register')

class NewAssetForm(FlaskForm):
    asset_name = StringField('Asset Name',validators=[DataRequired])
    domain = StringField('Domain',validators=[DataRequired])
    description = StringField('Asset Description',validators=[DataRequired])
    precision = IntegerField('Decimal Points')
    qty = StringField('Total Supply')
    file_upload = FileField('File')
    ipfs_hash = StringField('IPFS Location')
    
class TransferAssetForm(FlaskForm):
    recipient = StringField('Recepient Username @ Domain',validators=[DataRequired])
    asset_id = StringField('Asset Name # Domain',validators=[DataRequired])
    description = StringField('Transaction Description',validators=[DataRequired])
    qty = StringField('Total Amount')
    private_key = StringField('Private Key To Sign Tx',validators=[DataRequired])
 
class SellAssetMarketplaceForm(FlaskForm):
    account_id = 'asset_marketplace@test'
    asset_id = StringField('Asset ID',validators=[DataRequired])
    description = StringField('Asset Description',validators=[DataRequired])
    private_key = StringField('Private Key',validators=[DataRequired])
    qty = StringField('Total Supply')
    ple_cost = StringField('Price in PLE')
 
class AssetDetailsForm(FlaskForm):
     key = StringField('Key')
     value = StringField('Value')