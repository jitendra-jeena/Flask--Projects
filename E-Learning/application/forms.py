from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,Length,ValidationError,EqualTo
from application.models import User

#Login Form
class LoginForm(FlaskForm):
    email = StringField("Email",validators =[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=8,max=20)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

#Register Form
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8,max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=8,max=20),EqualTo("password")])
    first_name =StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name",validators=[DataRequired()])
    submit = SubmitField("register")

    def validate_email(self,email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already registered")