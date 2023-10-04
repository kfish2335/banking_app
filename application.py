from flask import Flask, flash, redirect, render_template, url_for
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect

from forms import AddForm, LoginForm, RegisterForm, SubForm, TransferForm
from modals import Transaction, User, db

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
application.config["SECRET_KEY"] = "thisisasecretkey"

db.init_app(application)
bcrypt = Bcrypt(application)
csrf = CSRFProtect(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@application.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have login successfully.")
                return redirect(url_for("dashboard"))
        flash("Username or Password is incorrect. ")
    return render_template("login.html", form=form)


@application.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        new_user = User(
            username=form.username.data,
            password=hashed_password,
            deposit=form.deposit.data,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account Created")
        return redirect("login")

    return render_template("register.html", form=form)


@application.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form_add = AddForm()
    form_sub = SubForm()
    form_transfer = TransferForm()
    user = User.query.get(current_user.id)

    if form_add.submit.data and form_add.validate_on_submit():
        user.deposit = form_add.amountadd.data + int(user.deposit)
        db.session.commit()
        flash("Transaction completed", "info")
    if form_sub.submit.data and form_sub.validate_on_submit():
        amount = int(user.deposit) - form_sub.amountsub.data
        if amount >= 0:
            user.deposit = amount
            db.session.commit()
            flash("Transaction completed", "info")
        else:
            flash("Insufficient Funds")
    if form_transfer.submit.data and form_transfer.validate_on_submit():
        target_user = User.query.filter_by(username=form_transfer.user.data).first()
        if target_user:
            target_user.deposit = form_transfer.transfer.data + int(target_user.deposit)
            db.session.commit()
            flash("Tranfer completed", "info")
        else:
            flash("Enter Valid User", "info")
    return render_template("dashboard.html", form_add=form_add, form_sub=form_sub, form_transfer=form_transfer)


@application.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have log out successfully.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")
