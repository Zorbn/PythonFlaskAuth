from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from encryption import bcrypt
from forms import LoginForm, RegisterForm
from models import Stats, User, db

routes_bp = Blueprint("routes", __name__, template_folder="templates")


@routes_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("routes.dashboard"))

    return render_template("home.html")


@routes_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@routes_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("routes.dashboard"))

    return render_template("login.html", form=form)


@routes_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))


@routes_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user_stats = Stats(money=0)
        new_user = User(username=form.username.data,
                        password=hashed_password, stats=new_user_stats)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("routes.login"))

    return render_template("register.html", form=form)
