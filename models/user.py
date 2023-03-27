from uuid import uuid4
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    # id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def json(self):
        return {"id": self.id, "first_name": self.first_name}

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
