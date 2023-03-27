from uuid import uuid4
from db import db


class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(256), unique=True,  nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)

    transactions = db.relationship("TransactionModel", back_populates="account", cascade="all,delete", lazy="dynamic")


    def json(self):
        return {
            "id": self.id,
            "account_name": self.account_name,
            "transactions": [trans for trans in self.transactions.all()],
            "transaction_count": self.transactions.count()
        }

    @classmethod
    def find_by_name(cls, account_name):
        return cls.query.filter_by(account_name=account_name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




