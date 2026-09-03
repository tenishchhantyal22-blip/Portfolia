
from app import app
from models import db, Request

with app.app_context():
    sample_requests = [
        Request(posted_by="Kathmandu Relief Camp", resource_type="Food", quantity=50, location="Kathmandu", urgency="High"),
        Request(posted_by="Pokhara Shelter", resource_type="Blankets", quantity=30, location="Pokhara", urgency="Medium"),
        Request(posted_by="Chitwan Medical Post", resource_type="Medicine", quantity=100, location="Chitwan", urgency="High"),
        Request(posted_by="Biratnagar Camp", resource_type="Shelter", quantity=10, location="Biratnagar", urgency="Low"),
    ]
    db.session.bulk_save_objects(sample_requests)
    db.session.commit()
    print("Sample requests added!")