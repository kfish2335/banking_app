from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    ValidationError,
)
from modals import User
from flask import flash

class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    deposit = IntegerField(
        validators=[InputRequired(), NumberRange(min=0, max=1000000)],
        render_kw={"placeholder": "Amount"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


class AddForm(FlaskForm):
    amountadd = IntegerField(
        validators=[InputRequired(), NumberRange(min=0, max=100000)],
        render_kw={"placeholder": "Amount"},
    )
    submit = SubmitField("Save changes")


class SubForm(FlaskForm):
    amountsub = IntegerField(
        validators=[InputRequired(), NumberRange(min=0, max=100000)],
        render_kw={"placeholder": "Amount"},
    )
    submit = SubmitField("Save changes")


class TransferForm(FlaskForm):
    user = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    transfer = IntegerField(
        validators=[InputRequired(), NumberRange(min=0, max=1000000)],
        render_kw={"placeholder": "Amount"},
    )
    submit = SubmitField("Register")

    def validate_user(self, user):
        existing_user_username = User.query.filter_by(username=user.data).first()
        if existing_user_username == None:
            flash( "That username doesn't exists. Please enter a valid user.", "info")
            raise ValidationError(
                "That username doesn't exists. Please enter a valid user."
            )
            