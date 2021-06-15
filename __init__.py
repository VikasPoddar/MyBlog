import os
from flask import Flask
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
app=Flask(__name__)
app.config['SECRET_KEY']='e273b7023dff20b9d0374ca424227400'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_POST']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_SENDER']=os.environ.get('EMAIL_USER')
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASS')
mail=Mail(app)
from MyBlog import route