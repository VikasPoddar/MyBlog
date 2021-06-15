from flask_wtf.form import FlaskForm
from MyBlog import db , login_manager , app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id) :
    return User.query.get(int(user_id))

class User(db.Model,UserMixin) :
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=True)
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self,exprires_sec=180) :
        s=Serializer(app.config['SECRET_KEY'],exprires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token) :
        s = Serializer(app.config['SECRET_KEY'])
        try :
            user_id = s.loads(token)['user_id']
        except :
            return None
        return User.query.get(user_id)
        

    def __repr__(self) :
        return f"User('{self.username}','{self.email}')"

class Post(db.Model) :
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(120),nullable=False)
    content=db.Column(db.Text,nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self) :
        return f"Post('{self.title}',' This post')"
