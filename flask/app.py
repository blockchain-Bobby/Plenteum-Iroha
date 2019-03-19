#!/usr/bin/env python3
###############################################################################
#                                   Imports                                   #
###############################################################################

from flask import Flask, jsonify,render_template, redirect, url_for, render_template_string, session
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from forms import NewAssetForm, UserRegistrationForm, LoginForm, DomainRegistrationForm, TransferAssetForm
from iroha_server import create_users, create_and_issue_new_asset, set_account_detail, get_user_details, get_domain_assets, get_user_password
import requests as r

###############################################################################
#                                  Application Setup                          #
###############################################################################

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)


###############################################################################
#                                  Functions / API End Points                 #
###############################################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        user = form.account_id.data
        password_hash = get_user_password(user)
        if check_password_hash(password_hash, form.password.data):
            session['account_id'] = user
            return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserRegistrationForm()

    if form.is_submitted():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user_name = form.username.data
        domain = form.domain.data
        ple_key = form.ple_key.data
        iroha_pvt_key, iroha_pub_key = create_users(user_name=user_name,domain=domain,pwd_hash=hashed_password,ple_id=ple_key)
        return '<h3>New user has been created!, your private key is: '+ str(iroha_pvt_key) + '</h3>'
    
    return render_template('signup.html', form=form)

@app.route('/new_asset', methods=['GET', 'POST'])
def new_asset():
    form = NewAssetForm()

    if form.is_submitted():
        if session['account_id']:
            create_and_issue_new_asset(asset=form.asset_name.data,domain=form.domain.data,precision=form.precision.data,qty=form.qty.data,account_id=session['account_id'],description=form.description.data)
            return redirect(url_for('dashboard'))
    return render_template('new_asset.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_user_details(session['account_id'])
    return jsonify(user)

@app.route('/all_domain_assets', methods=['GET', 'POST'])
def all_domain_assets():
    assets = get_domain_assets()
    return render_template('asset_explorer.html',assets=assets,name=session['account_id'])

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', name=session['account_id'])

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)