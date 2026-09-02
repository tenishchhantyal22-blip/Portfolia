from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Request, Match

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relief.db'
app.config['SECRET_KEY'] = 'change-this-to-anything-random-later'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = User.query.filter_by(email=request.form["email"]).first()
        if existing_user:
            flash("An account with this email already exists.")
            return redirect(url_for("register"))

        hashed_pw = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
        new_user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=hashed_pw,
            role="volunteer",
            location=request.form["location"]
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    return f"<h1>Welcome, {current_user.name}!</h1><p>Your role: {current_user.role}</p>"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)