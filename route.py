import os
from flask import render_template,url_for,flash,redirect,request,abort
from MyBlog import app,db,bcrypt,mail
from MyBlog.Models import User,Post
from MyBlog.form import SignUp,Login,UpdateAccountForm,PostForm,RequsetResetForm,ResetPasswordForm
from  flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message

#index_page
@app.route('/',methods=['GET','POST'])
def index() :
    return render_template('index.htm')

#signup_page
@app.route('/signup',methods=['GET','POST'])
def signup() :
    form=SignUp()
    if form.validate_on_submit() :
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Sign Up is done , you can login to your account","success")
        return redirect(url_for('index'))
    return render_template('signup.htm',title='Sign Up',form=form)


#login_page
@app.route('/login',methods=['GET','POST'])
def login() :
    form=Login()
    if form.validate_on_submit() :
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data) :
            login_user(user,remember=form.remember.data)
            flash(' welcome {}'.format(user.username))
            return redirect(url_for('home',title=current_user.username))
        else :
            flash('login Failed , please check email and password')
            return redirect(url_for('login'))
    return render_template('login.htm',title='Login',form=form)

#home_page
@app.route('/home')
@login_required
def home() :
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.id.desc()).paginate(page=page,per_page=5)
    return render_template('home.htm',title=current_user.username+"'s Blog",posts=posts)

#User_post
@app.route('/user/<string:username>')
@login_required
def user_post(username) :
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.id.desc()).paginate(page=page,per_page=5)
    return render_template('user_post.htm',title=current_user.username+"'s Blog",posts=posts,user=user)



#account_page

@app.route('/account',methods=['GET','POST'])
@login_required
def account() :
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash(' User Info Updated ')
        return redirect(url_for('account'))
    elif request.method=='GET' :
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template('account.htm',title='Account',form=form)

#new_post
@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post() :
    form=PostForm()
    if form.validate_on_submit() :
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(' Post is Uploaded ')
        return redirect(url_for('home'))
    return render_template('create_post.htm',title='New Post',form=form,legend='New Post')

#update_post
@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user :
        abort(403)
    form=PostForm()
    if form.validate_on_submit() :
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash(' post is updated ')
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET' :
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.htm',title='Update Post',form=form,legend='Update Post')

#delete_post
@app.route('/post/<int:post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user :
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(' post is deleted ')
    return redirect(url_for('home'))



#post
@app.route('/post/<int:post_id>',methods=['GET','POST'])
@login_required
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.htm',title=post.title,post=post)


#logout_page
@app.route('/logout')
@login_required 
def logout() :
    logout_user()
    return redirect(url_for('index'))

#about_page
@app.route('/about')
def about() :
    return render_template('about.htm',title='About Us')

#contact_page
@app.route('/conntact')
def contact() :
    return render_template('contact.htm',title='Contact Us')

#moreinfo_page
@app.route('/more') 
def more() :
    return render_template('more.htm',title='More Info')

#
def send_reset_email(user) :
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender='poddarmail001@gmail.com',recipients=[user.email])
    msg.body=f'''
To Reset your password , vist the following linl : {url_for('reset_token',token=token,_external=True)}
If you did not make this request , ignore this mail
'''
    mail.send(msg)

#reset password request
@app.route('/reset_password',methods=['GET','POST'])
def reset_request () :
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RequsetResetForm()
    if form.validate_on_submit() :
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email is sent with reset link ')
        return redirect(url_for('login'))
    return render_template('reset_request.htm',title='Reset Password',form=form)

#reset password 
@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token (token) :
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user=User.verify_reset_token(token)
    if user is None :
        flash(' token expired ')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit() :
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(" password is updated ","success")
        return redirect(url_for('login'))
    return render_template('reset_token.htm',title='Reset Password',form=form)
 