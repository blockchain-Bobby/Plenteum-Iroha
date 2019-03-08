#very dirty code needs to be cleaned up
from flask import Flask, render_template, redirect, url_for, render_template_string
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import Float, Column, Boolean, BigInteger ,Integer, String, ForeignKey, Date, DateTime 
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import NewAssetForm, RegistrationForm, LoginForm
import requests as r
import pandas as pd

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)

#tables need to be moved to seperate file
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    pub_key = Column(String(100), unique = True, nullable=False)
    password_hash = Column(String(255), nullable=False)

def create_turtle_payment():
    turtle_pay = 'https://api.turtlepay.io/v1/new'
    tx_details ={
        'address': 'TRTLuwh9Jfx4nhzmsZwaciNVPUMYxicu4XNUT4X9pwBaN5gsBTGDEHFHTVTtDrAu9A5TP3RBqAGjJTb6RC2FEsJPCogz4m7cbhw',
        'amount': 1000,
        'callback': '',
        'confirmations': 60,
        'userDefined':{}
        }
        #add in callback"
    payment_details = r.post(turtle_pay, json=tx_details)
    return payment_details
  
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.is_submitted():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, pub_key=form.pub_key.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
    
    return render_template('signup.html', form=form)

@app.route('/new_asset', methods=['GET', 'POST'])
def new_asset():
    form = NewAssetForm()

    if form.is_submitted():
        user_tx = iroha.transaction(
        [iroha.command('CreateAsset', asset_name='bitcoin',
            domain_id='test', precision=2, amount='1')],
        creator_account='bob@test'
    )
    iroha.batch(user_tx, atomic=True)
    # sign transactions only after batch meta creation
    ic.sign_transaction(alice_tx, *alice_private_keys)
    send_batch_and_print_status(alice_tx, user_tx)
    
    return '<h1>New user has been created!</h1>'
    
    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)