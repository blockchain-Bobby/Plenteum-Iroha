#very dirty code needs to be cleaned up
from flask import Flask, render_template, redirect, url_for, render_template_string
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import NewAssetForm, RegistrationForm, LoginForm
from iroha_server import create_users, create_and_issue_new_asset, set_account_detail, get_user_details, get_domain_assets, get_user_password
import json
import requests as r

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)
  
@login_manager.user_loader
def load_user(user_id):
    #return user from iroha
    return 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.account_id.data
        password_hash = get_user_password(user)
        if check_password_hash(password_hash, form.password.data):
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
        ple_key = form.ple_key.data
        iroha_pvt_key, iroha_pub_key = create_users(user_name=user_name,domain=domain,pwd_hash=hashed_password,ple_id=ple_key)
        return '<h1>New user has been created!, your private key is: '+ str(iroha_pvt_key) + '</h1>'
    
    return render_template('signup.html', form=form)

#create new asset
@app.route('/new_asset', methods=['GET', 'POST'])
def new_asset():
    form = NewAssetForm()

    if form.is_submitted():
        create_and_issue_new_asset(asset=form.asset_name.data,domain=form.domain.data,precision=form.precision.data,qty=form.qty.data,account_id=form.account_id.data,description=form.description.data)
        return '<h1>New Asset has been created!</h1>'

    return render_template('new_asset.html', form=form)

#view account keys n values
@app.route('/accounts', methods=['GET', 'POST'])
def account_details():
    user = get_user_details('biscuit@test')
    return str(user)

#view account keys n values
@app.route('/all_assets', methods=['GET', 'POST'])
def all_assets():
    assets = get_domain_assets()
    return json.dumps(assets)

'''add transfer asset, view account details'''

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