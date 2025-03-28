import uuid
from models.database import db
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Shoti(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    url = db.Column(db.String(1000))
    img_urls = db.Column(JSONB)
    title = db.Column(db.String(1000))
    duration = db.Column(db.String(20))
    usr_region = db.Column(db.String(10))
    usr_nickname = db.Column(db.String(100))
    usr_username = db.Column(db.String(100))
    usr_instagram = db.Column(db.String(100))
    usr_signature = db.Column(db.String(100))
    usr_twitter = db.Column(db.String(100))
    is_video = db.Column(db.Boolean, nullable=False, default=False)
    adder_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    shoti_score = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": str(self.id),
            "url": self.url,
            "img_urls": self.img_urls,
            "title": self.title,
            "duration": self.duration,
            "usr_region": self.usr_region,
            "usr_nickname": self.usr_nickname,
            "usr_username": self.usr_username, 
            "usr_instagram": self.usr_instagram,
            "usr_twitter": self.usr_twitter,
            "usr_signature": self.usr_signature,
            "is_video": self.is_video,
            "adder_id": str(self.adder_id),
            "shoti_score": self.shoti_score
        }
