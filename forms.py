from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    ValidationError,
)


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
