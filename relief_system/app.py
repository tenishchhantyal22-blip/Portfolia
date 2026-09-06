
#It's the main file that runs the whole website. It sets up Flask, connects to the SQLite database, 
#and handles user accounts through Flask-Login and Flask-Bcrypt (so passwords get hashed, not stored as plain text). 
#Beyond that, it defines every route — the URLs someone can visit and what happens when they do: the home page, 
#registration, login/logout, the volunteer dashboard, posting a new relief request, and matching a volunteer to a request. 
#Each route either shows a page or processes a form, then talks to the database through the models we defined separately 
#in models.py
#In short: app.py is the control center — every click on the site eventually routes through this file 

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Request, Match

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relief.db'
app.config['SECRET_KEY'] = 'wsedrftgyhujikrtgyhuj'

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
    open_requests = Request.query.filter_by(status="open").all()
    return render_template("dashboard.html", requests=open_requests)

@app.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return "Access denied — admin only.", 403

    all_requests = Request.query.all()
    all_matches = Match.query.all()

    # Build a lookup: request_id -> volunteer name
    helper_map = {}
    for m in all_matches:
        volunteer = User.query.get(m.volunteer_id)
        helper_map[m.request_id] = volunteer.name if volunteer else "Unknown"
    
    open_count = Request.query.filter_by(status="open").count()
    matched_count = Request.query.filter_by(status="matched").count()
    fulfilled_count = Request.query.filter_by(status="fulfilled").count()

    return render_template("admin.html", requests=all_requests, matches=all_matches,
                           helper_map=helper_map, open_count=open_count,
                           matched_count=matched_count, fulfilled_count=fulfilled_count)

@app.route("/fulfill/<int:request_id>")
@login_required
def fulfill(request_id):
    if current_user.role != "admin":
        return "Access denied — admin only.", 403

    req = Request.query.get(request_id)
    if req:
        req.status = "fulfilled"
        db.session.commit()
        flash(f"Request from {req.posted_by} marked as fulfilled!")
    return redirect(url_for("admin_dashboard"))

@app.route("/post-request", methods=["GET", "POST"])
@login_required
def post_request():
    if request.method == "POST":
        qty = int(request.form["quantity"])
        if qty <= 0:
            flash("Quantity must be greater than zero.")
            return redirect(url_for("post_request"))

        new_req = Request(
            posted_by=request.form["posted_by"],
            resource_type=request.form["resource_type"],
            quantity=qty,
            location=request.form["location"],
            urgency=request.form["urgency"]
        )
        db.session.add(new_req)
        db.session.commit()
        flash("Request posted successfully!")
        return redirect(url_for("dashboard"))
    return render_template("post_request.html")
    
@app.route("/help/<int:request_id>")
@login_required
def help_request(request_id):
    req = Request.query.get(request_id)
    if req and req.status == "open":
        new_match = Match(request_id=req.id, volunteer_id=current_user.id)
        req.status = "matched"
        db.session.add(new_match)
        db.session.commit()
        flash(f"You've been matched to help {req.posted_by}!")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)