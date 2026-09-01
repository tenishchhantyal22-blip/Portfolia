from flask import Flask, render_template
from models import db, User, Request, Match

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relief.db'
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)