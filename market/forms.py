from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired, EqualTo, Regexp, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    """
     For form fields related validation ( example the  below one related to username getting from form and checking
     against db if it already exists) Flask Form class allow us to create the validation method like below, but we need
     to follow the syntax validate_{form field} otherwise flask will not call this method.
     So, if we follow this syntax , flask will automatically call this validation method internally for that field

    """

    def validate_username(self, user_to_validate):
        userfromdb = User.query.filter_by(username=user_to_validate.data).first()
        if userfromdb:
            raise ValidationError(f'username {user_to_validate.data} already exists')

    def validate_email_address(self, email_to_validate):
        emailfromdb = User.query.filter_by(email_add=email_to_validate.data).first()
        if emailfromdb:
            raise ValidationError(f' Email address {email_to_validate.data} already exists')

    username = StringField(label='User Name:',
                           validators=[Length(min=2, max=30, message="length is short"), DataRequired()])
    """
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$', message=("Username should be one word, letters, "
                                             "numbers and underscores only")
            )
        ])
        """
    email_address = StringField(label='Email Address:', validators=[Email("Invalid email address"), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=3), DataRequired()])
    password2 = PasswordField(label='Confirm Password:',
                              validators=[EqualTo("password1", message="Password must match"), DataRequired()])
    submit = SubmitField(label='Create Account ')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])

    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item")


class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item")
