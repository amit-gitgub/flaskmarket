from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'

"""
To work with forms , first we need to create the secret key which will be used throughout the application development. As forms collects the user 
data through submit ( action POST) so there need to be an extra layer of security, which is achieved with below config
Note:- we can generate the key using python os module.
ex: os.urandom(12).hex()

"""
app.config['SECRET_KEY'] = '0de71ac65383ca8be1e66a17'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = "You are not authorised to access this page. Please first Log in."
login_manager.login_message_category = "danger"


from market import routes
