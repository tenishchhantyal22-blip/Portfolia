from app import app
from models import db, User

with app.app_context():
    user = User.query.filter_by(email="tenishchhantyal22@gmail.com").first()
    if user:
        user.role = "admin"
        db.session.commit()
        print(f"{user.name} is now an admin. Role: {user.role}")
    else:
        print("User not found — check the email address.")