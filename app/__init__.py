import os
import sqlalchemy
from yaml import load, Loader
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


def init_connect_engine():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
    pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="mysql+pymysql",
                username=os.environ.get('MYSQL_USER'), #username
                password=os.environ.get('MYSQL_PASSWORD'), #user password
                database=os.environ.get('MYSQL_DB'), #database name
                host=os.environ.get('MYSQL_HOST') #ip
) )
    return pool
app = Flask(__name__)
db = init_connect_engine()
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)







from app import routes



