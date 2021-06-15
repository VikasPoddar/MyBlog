from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Email,Length,ValidationError
from MyBlog.Models import User
from flask_login import current_user


class SignUp(FlaskForm) :
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')
    def validate_username(self,username) :
        user=User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError(' Opps! Username is taken , chooose other name  ')
    def validate_emali(self,email) :
        user=User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError(' Opps! Email is taken , chooose other name  ')
    
class Login(FlaskForm) :
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember field')
    submit=SubmitField('Login')

class UpdateAccountForm(FlaskForm) :
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Update')
    def validate_username(self,username) :
        if username.data!=current_user.username :
            user=User.query.filter_by(username=username.data).first()
            if user :
                raise ValidationError(' Opps! Username is taken , chooose other name  ')
    def validate_emali(self,email) :
        if email.data!=current_user.email :
            user=User.query.filter_by(email=email.data).first()
            if user :
                raise ValidationError(' Opps! Email is taken , chooose other name  ')

class PostForm(FlaskForm) :
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Post')

class RequsetResetForm(FlaskForm) :
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField(' Password reset ')
    def validate_emali(self,email) :
        if email.data!=current_user.email :
            user=User.query.filter_by(email=email.data).first()
            if user  is None  :
                raise ValidationError(' There is no account with this email ')

class ResetPasswordForm(FlaskForm) :
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField(' Reset Password ')