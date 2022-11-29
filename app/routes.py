""" Specifies routing for the application"""
from flask import render_template, request, jsonify, url_for, redirect, Flask,session,flash
from app import app
from app import database as db_helper
# from app import User as User

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)


a=0

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "password"})

    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        items = db_helper.fetch_users()
        for item in items:
            if item["username"]==username.data:
                print(username)
                raise ValidationError(
                    'That username already exists. Please choose a different one.')
       

@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """
    old_record = db_helper.find_comments(task_id)
    data = request.get_json()
    try:
        response1,response2,response3 = '','',''
        if (data["park_name"]!=old_record[0]):
            db_helper.update_park_code(task_id, data["park_name"])
            response1 = "Park Code Updated"
        if (data["rating"]!=old_record[1]):
            db_helper.update_rating(task_id, data["rating"])
            response2 = 'Rating Updated'
        if (data["comments"]!=old_record[2]):
            db_helper.update_comments(task_id, data["comments"])
            response3 = 'comments Updated'
        
        result = {'success': True, 'response': response1 + " " + response2 + " " + response3}
        if (not response1 and not response2 and not response3):
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

login1 = 0

@app.route('/', methods=['GET','POST'])
def index():
    login1 = False
    username = ''
    if 'username' in session:
        login1 = True
        username = session['username']
    items = db_helper.fetch_park('','','')
    if request.method == 'POST':
        variable1 = request.form['variable1']
        variable2 = request.form['variable2']
        variable3 = request.form['variable3']
        items = db_helper.fetch_park(variable1,variable2,variable3)
    
    # username = username
    userid = db_helper.find_user_id(username)
    items_c = db_helper.fetch_comments(userid)
    item_query1 = db_helper.advance_query1()
    item_query2 = db_helper.advance_query2()
    a = 1

    park_list = db_helper.fetch_all_parks()

    return render_template("index.html", items=items, items_comment=items_c, item_query1 = item_query1, item_query2 = item_query2,login1=login1, item_park = park_list)

@app.route('/info', methods=['GET','POST'])
def info():
    
    return render_template("info.html")


@app.route("/insert", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    login1 = False
    username = ''
    if 'username' in session:
        login1 = True
        username = session['username']
    userid = db_helper.find_user_id(username)
    data = request.get_json()
    db_helper.insert_new_task(data['park_name'], data['rating'], data['comments'],userid)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    items = db_helper.fetch_users()
    if form.validate_on_submit():
        user=0
        for item in items:
            if item["username"]==form.username.data:
                item.pop('id')
                user = item
                print(user['password'])
        if user:
            print(user['password'])
            if (user['password']==form.password.data):
                
                # login_user(user)
                print(user['password'])
                a = 0
                session['username']=user['username']
                flash('You were logged in.')
                return redirect(url_for('index'))
                a = 0

    return render_template('login.html', form=form,username=form.username.data)
a=0
@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('You were logged out.')
    # return redirect(url_for('index'))
    return render_template('logout.html')







@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data)
        # new_user = User(username=form.username.data, password=hashed_password)
        # db.session.add(new_user)
        # db.session.commit()
        db_helper.insert_new_user(form.username.data,form.password.data)
        print(form.password.data)
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


def api_response():
    from flask import jsonify
    if request.method == 'POST':
        return jsonify(**requirements.txt)
