from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, PostForm, LoginForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import *
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

posts = []

@app.route('/')
def index():

    return render_template("index.html",posts=posts)
    #return f"{len(posts)} posts"

@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html",slug_title=slug)
    #return f"Mostrando el post {slug}"

@app.route("/admin/post/", methods=["GET", "POST"], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=["GET", "POST"])
@login_required
def post_form(post_id):

    form_post = PostForm()
    if form_post.validate_on_submit():
        title = form_post.title.data
        title_slug = form_post.title_slug.data
        content = form_post.content.data
        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)
        return redirect(url_for('index'))
    return render_template("admin/post_form.html",form=form_post)
    #return f"posft_form {post_id}"

@app.route("/signup/",methods=["GET","POST"])
def show_signup_form():

    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User(len(users)+1,name,email,password)
        user.anonymous=False
        user.authenticated=True
        users.append(user)
        print(users)
        login_user(user, remember=True)

        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html",form=form)

@login_manager.user_loader
def load_user(user_id):

    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route("/login/",methods=["GET","POST"])
def login():

    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))
    print(users)
    form = LoginForm()
    if form.validate_on_submit():

        user = get_user(form.email.data)
        print(user)
        if user is not None and user.check_password(form.password.data):

            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':

                next_page = url_for('index')
                print(f"USUARIO LOGUEADO {user}")
            return redirect(next_page)
            
    return render_template('login.html',form=form)

@app.route('/logout/')
def logout():
    logout_user()
    print("EL USUARIO A HECHO LOGOUT.")
    return redirect(url_for('index'))

