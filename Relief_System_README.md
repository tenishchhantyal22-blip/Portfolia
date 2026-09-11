# Disaster Relief & Resource Coordination System

A full-stack web application connecting disaster relief volunteers with camps and individuals reporting urgent resource needs
— food, medicine, shelter, and blankets.

## Live Demo
==>  URL https://portfolia-y45g.onrender.com

## Problem It Solves
During disasters, relief efforts are often uncoordinated — volunteers don't know where help is needed most, and camps have no
easy way to broadcast urgent requests. This system creates a simple, centralized way to match available help to actual need.

## Features
- Volunteer registration and secure login (password hashing via Flask-Bcrypt)
- Post relief requests with resource type, quantity, location, and urgency level
- Volunteer-to-request matching system
- Admin dashboard to track all requests and their fulfillment status
- Visual analytics (status breakdown chart)

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Frontend:** HTML, Bootstrap 5
- **Charts:** Chart.js
- **Deployment:** Render

## Running Locally
```bash
git clone https://github.com/tenishchhantyal22-blip/Portfolia.git
cd Portfolio/relief_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Author
Tenish Chhantyal — [GitHub](https://github.com/tenishchhantyal22-blip)
