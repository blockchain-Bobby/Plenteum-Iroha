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
from iroha_ple import create_users, create_new_asset
import requests as r
#import pandas as pd

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
    ple_pub_key = Column(String(100), unique = True, nullable=False)
    iroha_pub_key = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
  
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
        user_name = form.username.data
        domain = form.domain.data
        iroha_pvt_key, iroha_pub_key = create_users(user_name=user_name,domain=domain)
        new_user = User(username=form.username.data, ple_pub_key=form.pub_key.data, iroha_pub_key=iroha_pub_key, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!, your private key is: '+ str(iroha_pvt_key) + '</h1>'
    
    return render_template('signup.html', form=form)

#create new asset
@app.route('/new_asset', methods=['GET', 'POST'])
def new_asset():
    form = NewAssetForm()

    if form.is_submitted():
        create_new_asset(username='admin@test',asset=form.asset_name.data,domain=form.domain_name.data,precision=form.precision.data)
        return '<h1>New Asset has been created!</h1>'

    return render_template('new_asset.html', form=form)

@app.route('/transfer_asset', methods=['GET', 'POST'])
def transfer_asset():
    form = NewAssetForm()

    if form.is_submitted():
        create_new_asset(username='admin@test',asset=form.asset_name.data,domain=form.domain_name.data,precision=form.precision.data,qty=form.qty.data)
        return '<h1>New Asset has been created!</h1>'

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