from flask import render_template, request,flash, redirect, url_for, session, abort
from functools import wraps
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db
from app.models import Post, User
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, EqualTo
import pyqrcode
from io import StringIO


class RegisterForm(Form):
    """Registration form."""
    name = StringField('Full Name', validators=[Required(), Length(1, 128)])
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    password_again = PasswordField('Password again',
                                   validators=[Required(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(Form):
    """Login form."""
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')
    
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated():
        # if user is logged in we get out of here
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('register'))
        # add new user to the database
        user = User(username=request.form['username'],
                                password=request.form['pass'], 
                                name=request.form['name'])
        db.session.add(user)
        db.session.commit()
    
        session['username'] = user.username
        return redirect(url_for('qr_auth'))
        
    return render_template('register.html')


@app.route('/qr')
def qr_auth():
    if 'username' not in session:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('index'))
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('qr.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = StringIO()
    url.svg(stream, scale=5)
    return stream.getvalue().encode('utf-8'), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated():
        # if user is logged in we get out of here
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not user.verify_password(request.form['pass']) or \
                not user.verify_totp(request.form['token']):
            flash('Invalid username, password or token.')
            return redirect(url_for('login'))
        # log user in
        login_user(user)
        flash('You are now logged in!')
        return redirect(url_for('index'))
        
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/' )
@login_required
def index():
    post = Post.query.filter_by(user_id=current_user.id)
    return render_template('index.html', post=post)

@app.route('/create' , methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        id = User.query.filter_by(username=current_user.name).first()
        post=Post(user_id=current_user.id, 
                    department=request.form['department'],
                    role=request.form['role'],
                    description=request.form['description'])
        db.session.add(post)
        db.session.commit()
        flash('New entry was successfully posted')

    return render_template('create.html')



@app.route('/edit/<id>' , methods=['POST', 'GET'])
@login_required
def edit (id):
    #Getting user by primary key:
    post = Post.query.get(id)
    if request.method == 'POST':
		post.name = request.form['name']
		post.department =  request.form['department']
		post.role =  request.form['role']
		db.session.commit()
		return  redirect(url_for('index'))
    return render_template('edit.html', post=post)
    

@app.route('/delete/<id>' , methods=['POST', 'GET'])
@login_required
def delete (id):
     post = Post.query.get(id)
     db.session.delete(post)
     db.session.commit()
     flash ('deleted')

     return redirect(url_for('index'))

