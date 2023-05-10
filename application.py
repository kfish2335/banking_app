from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange, DataRequired
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from datetime import datetime

application= Flask(__name__)
db = SQLAlchemy()
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
application.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(application)
bcrypt = Bcrypt(application)
csrf = CSRFProtect(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    deposit = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.now)

class Transaction(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref = db.backref("user", uselist=False))
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.now)
    
class RegisterForm(FlaskForm):
    username = StringField( validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField( validators=[
                             InputRequired(), Length(min=8, max=20)],render_kw={"placeholder": "Password"})
    
    deposit = IntegerField(validators=[
                             InputRequired(), NumberRange(min=0, max=1000000)],render_kw={"placeholder": "Amount"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                            InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
    

class AddForm(FlaskForm):
    amountadd = IntegerField(validators=[
                             InputRequired(), NumberRange(min=0, max=100000)],render_kw={"placeholder": "Amount"})
    submit = SubmitField('Save changes')

class SubForm(FlaskForm):
    amountsub = IntegerField(validators=[
                             InputRequired(), NumberRange(min=0, max=100000)],render_kw={"placeholder": "Amount"})
    submit = SubmitField('Save changes')

@application.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate():
        
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have login successfully.")
                return redirect(url_for('dashboard'))
        flash("Username or Password is incorrect. ")
    return render_template("login.html", form=form)

@ application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        
        new_user = User(username=form.username.data, password=hashed_password , deposit=form.deposit.data )
        db.session.add(new_user)
        db.session.commit()
        flash("Account Created")
        return redirect('login')
        
    
    return render_template('register.html', form=form)

@application.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form_add = AddForm()
    form_sub = SubForm()
    user = User.query.get(current_user.id)

    if form_add.submit.data and form_add.validate_on_submit():
        user.deposit = form_add.amountadd.data + int(user.deposit)
        db.session.commit()
        flash("Transaction completed", 'info')
    if form_sub.submit.data and form_sub.validate_on_submit():
        amount = int(user.deposit) - form_sub.amountsub.data
        if amount >= 0:
            user.deposit = amount
            db.session.commit()
            flash("Transaction completed", 'info')
        else:
            flash("Insufficient Funds")
    return render_template('dashboard.html', form_add=form_add, form_sub= form_sub)


@application.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have log out successfully.", 'info')
    return redirect(url_for('login'))



if __name__ == '__main__':
    application.run(debug=True
                    )