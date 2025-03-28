import uuid
from models.database import db
from sqlalchemy.dialects.postgresql import UUID

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    apikey = db.Column(db.String(50), unique=True, nullable=False)
    is_adder = db.Column(db.Boolean, nullable=False, default=False)
    requests = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {"id": str(self.id), "name": self.name, "email": self.email, "apikey": self.apikey, "requests": self.requests, "is_adder": self.is_adder}
        